"""
Programmatic eval for MoSPI MCP 2-tool design.

Sends natural language queries to Claude API with tool definitions,
executes tools locally (no MCP server needed), and checks whether
Claude's final response contains the actual data values from the API.

Usage:
    python tests/eval_api.py                    # Quick: 2 per dataset
    python tests/eval_api.py --all              # Full: all queries
    python tests/eval_api.py --dataset PLFS     # Single dataset
    python tests/eval_api.py --query PLFS:1     # Single query
"""

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path

import anthropic

# Add project root to path so we can import mospi modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from mospi.search import search_dataset
from mospi.client import mospi

# ---------------------------------------------------------------------------
# Tool definitions (matching @mcp.tool schemas from mospi_server.py)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "describe_dataset",
        "description": (
            "Search a MoSPI dataset for indicators and filter values.\n\n"
            "Datasets: PLFS (employment), CPI (inflation), IIP (industrial production),\n"
            "ASI (factory data), NAS (GDP), WPI (wholesale prices), ENERGY.\n\n"
            "search_terms: case-insensitive search across all indicators and filters.\n"
            "Be liberal — include synonyms, abbreviations, and related terms.\n"
            "e.g., for \"unemployment in Maharashtra\":\n"
            '  search_terms=["unemployment", "UR", "maharashtra", "2022", "2023"]\n\n'
            "Returns matching codes to use in get_data(), plus any required params\n"
            "you didn't search for with their full option lists."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "dataset": {"type": "string"},
                "search_terms": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["dataset", "search_terms"],
        },
    },
    {
        "name": "get_data",
        "description": (
            "Fetch data from a MoSPI dataset. Use codes from describe_dataset().\n"
            'Pass limit (e.g., "50", "100") if you expect many records.'
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "dataset": {"type": "string"},
                "filters": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                },
            },
            "required": ["dataset", "filters"],
        },
    },
]

# ---------------------------------------------------------------------------
# Tool execution (replicates mospi_server.py routing logic)
# ---------------------------------------------------------------------------

DATASET_MAP = {
    "CPI_GROUP": "CPI_Group",
    "CPI_ITEM": "CPI_Item",
    "IIP_ANNUAL": "IIP_Annual",
    "IIP_MONTHLY": "IIP_Monthly",
    "PLFS": "PLFS",
    "ASI": "ASI",
    "NAS": "NAS",
    "WPI": "WPI",
    "ENERGY": "Energy",
}

VALID_DATASETS = ["PLFS", "CPI", "IIP", "ASI", "NAS", "WPI", "ENERGY"]


def execute_tool(name: str, args: dict) -> dict:
    """Execute a tool call by dispatching to our Python functions."""
    if name == "describe_dataset":
        return search_dataset(args["dataset"], args["search_terms"])

    elif name == "get_data":
        dataset = args["dataset"].upper()
        filters = {k: str(v) for k, v in args.get("filters", {}).items() if v is not None}

        # Auto-route CPI and IIP
        if dataset == "CPI":
            dataset = "CPI_ITEM" if "item_code" in filters else "CPI_GROUP"
        if dataset == "IIP":
            dataset = "IIP_MONTHLY" if "month_code" in filters else "IIP_ANNUAL"

        api_dataset = DATASET_MAP.get(dataset)
        if not api_dataset:
            return {"error": f"Unknown dataset: {dataset}", "valid_datasets": VALID_DATASETS}

        result = mospi.get_data(api_dataset, filters)

        if isinstance(result, dict) and result.get("msg") == "No Data Found":
            result["hint"] = (
                "No data for this filter combination. Try: "
                "1) Remove optional filters one at a time. "
                "2) Use describe_dataset() to verify your codes are correct. "
                "3) Try a broader filter (e.g., group level instead of item level)."
            )
        return result

    return {"error": f"Unknown tool: {name}"}


# ---------------------------------------------------------------------------
# Claude API tool-use loop
# ---------------------------------------------------------------------------

def run_query(client: anthropic.Anthropic, query: str, max_turns: int = 10) -> dict:
    """Send a query to Claude with tools, run the tool loop, return results."""
    # Strip "Respond in chat, not in an artifact." suffix from mcp-bench queries
    query = query.replace("Respond in chat, not in an artifact.", "").strip()

    messages = [{"role": "user", "content": query}]
    tool_calls = []

    for _ in range(max_turns):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                tools=TOOLS,
                messages=messages,
            )
        except Exception as e:
            return {"text": "", "tool_calls": tool_calls, "error": str(e)}

        # Collect any text and tool_use blocks
        assistant_text = ""
        tool_use_blocks = []
        for block in response.content:
            if block.type == "text":
                assistant_text += block.text
            elif block.type == "tool_use":
                tool_use_blocks.append(block)

        if response.stop_reason == "end_turn":
            return {"text": assistant_text, "tool_calls": tool_calls}

        if response.stop_reason == "tool_use":
            # Execute each tool call and build results
            tool_results = []
            for block in tool_use_blocks:
                print(f"      -> {block.name}({json.dumps(block.input, default=str)[:120]})")
                try:
                    result = execute_tool(block.name, block.input)
                except Exception as e:
                    result = {"error": str(e)}

                tool_calls.append({
                    "name": block.name,
                    "input": block.input,
                    "output": result,
                })
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, default=str),
                })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

    return {"text": "", "tool_calls": tool_calls, "error": "max_turns_exceeded"}


# ---------------------------------------------------------------------------
# Scoring — focused on end result
# ---------------------------------------------------------------------------

def extract_data_values(tool_calls: list) -> list[str]:
    """
    Extract the key data values from the last successful get_data call.
    Returns a list of value strings that should appear in Claude's response.
    """
    # Find the last get_data call that returned data
    for call in reversed(tool_calls):
        if call["name"] != "get_data":
            continue
        output = call.get("output", {})
        if not isinstance(output, dict):
            continue
        if output.get("msg") != "Data fetched successfully":
            continue

        data_rows = output.get("data", [])
        if not isinstance(data_rows, list) or not data_rows:
            continue

        # Extract the primary data value from the first row
        # Focus on the key metric fields — value, index, index_value, inflation
        values = []
        first_row = data_rows[0]

        # Priority keys — these are the actual data points
        data_keys = ["value", "index", "index_value", "inflation",
                     "index_number", "growth_rate"]

        for key in data_keys:
            if key in first_row:
                val_str = str(first_row[key]).strip()
                if val_str and val_str not in ("None", "null", ""):
                    try:
                        float(val_str.replace(",", ""))
                        values.append(val_str)
                    except ValueError:
                        pass

        # If no priority keys found, fall back to any numeric field
        # that isn't clearly metadata
        if not values:
            skip_keys = {
                "unit", "status", "frequency", "sector", "gender",
                "AgeGroup", "weekly_status", "religion", "socialGroup",
                "General_Education", "quarter", "month", "baseyear",
                "year", "base_year", "classification_year", "state",
                "indicator", "group", "subgroup", "majorgroup",
                "sub_subgroup", "item", "series", "revision",
            }
            for key, val in first_row.items():
                if key in skip_keys:
                    continue
                val_str = str(val).strip()
                if val_str and val_str not in ("None", "null", "", "all", "person"):
                    try:
                        f = float(val_str.replace(",", ""))
                        # Skip small integers that are likely codes
                        if abs(f) > 100 or "." in val_str:
                            values.append(val_str)
                    except ValueError:
                        pass

        return values

    return []


def normalize_number(s: str) -> str:
    """Normalize a number string for comparison (strip commas, trailing zeros)."""
    s = s.replace(",", "").strip()
    try:
        f = float(s)
        # Normalize: 3.10 -> 3.1, 205.3 -> 205.3
        if f == int(f) and "." not in s:
            return str(int(f))
        return str(f)
    except ValueError:
        return s


def check_values_in_response(response_text: str, expected_values: list[str]) -> tuple[bool, list[str], list[str]]:
    """
    Check if expected data values appear in Claude's response.
    Returns (all_found, found_values, missing_values).
    """
    if not expected_values or not response_text:
        return False, [], expected_values

    # Normalize the response text for number matching
    response_normalized = response_text.replace(",", "")

    found = []
    missing = []

    for val in expected_values:
        val_norm = normalize_number(val)
        # Check if the normalized value appears in the response
        if val_norm in response_normalized or val in response_text:
            found.append(val)
        else:
            # Try matching with % sign or other formatting
            # e.g., "3.1" matches "3.1%" or "3.10%"
            try:
                f = float(val_norm)
                # Check common formats
                formats = [
                    val_norm,
                    f"{f:.1f}",
                    f"{f:.2f}",
                    f"{f:,.0f}",
                    f"{f:,.1f}",
                    f"{f:,.2f}",
                    str(int(f)) if f == int(f) else None,
                ]
                matched = False
                for fmt in formats:
                    if fmt and fmt in response_normalized:
                        found.append(val)
                        matched = True
                        break
                if not matched:
                    missing.append(val)
            except ValueError:
                missing.append(val)

    all_found = len(missing) == 0 and len(found) > 0
    return all_found, found, missing


def score_result(result: dict, expected_dataset: str) -> dict:
    """Score a query result based on end-to-end correctness."""
    calls = result.get("tool_calls", [])
    response_text = result.get("text", "")

    # Did it get data from the API?
    got_data = any(
        c["name"] == "get_data"
        and isinstance(c.get("output"), dict)
        and c["output"].get("msg") == "Data fetched successfully"
        for c in calls
    )

    # Extract the actual data values from get_data output
    expected_values = extract_data_values(calls)

    # Check if Claude's response contains the data values
    values_match, found_vals, missing_vals = check_values_in_response(
        response_text, expected_values
    )

    # Overall pass: got data AND reported the values correctly
    passed = got_data and values_match

    return {
        "passed": passed,
        "got_data": got_data,
        "values_match": values_match,
        "expected_values": expected_values,
        "found_values": found_vals,
        "missing_values": missing_vals,
        "num_tool_calls": len(calls),
    }


# ---------------------------------------------------------------------------
# Query loading
# ---------------------------------------------------------------------------

QUERIES_DIR = Path("/tmp/mcp-bench/queries/claude/single_indicator")

FALLBACK_QUERIES = {
    "PLFS": [
        {"no": "1", "query": "What is the unemployment rate for rural males in Bihar during 2022-23?"},
        {"no": "3", "query": "worker population ratio among scheduled tribes in Rajasthan 2023-24"},
    ],
    "CPI": [
        {"no": "1", "query": "What is the CPI for food and beverages in rural India for January 2023?"},
        {"no": "4", "query": "What is the general CPI trend for All India from 2015 to 2024?"},
    ],
    "WPI": [
        {"no": "1", "query": "What is the wholesale price index for primary articles in January 2023?"},
        {"no": "9", "query": "How much did onion prices change in WPI from 2015 to 2023?"},
    ],
    "IIP": [
        {"no": "1", "query": "What is the IIP for mining sector in 2022-23?"},
        {"no": "4", "query": "index of industrial production for manufacturing base year 2011-12 in 2023?"},
    ],
    "ASI": [
        {"no": "1", "query": "How many factories were operating in Maharashtra in 2022-23?"},
        {"no": "3", "query": "total employees in food processing industry across India 2021-22"},
    ],
    "NAS": [
        {"no": "1", "query": "What was India's GDP in 2023-24 at current prices?"},
        {"no": "3", "query": "gva growth rate last 5 years agriculture"},
    ],
    "ENERGY": [
        {"no": "1", "query": "What was India's total coal production in 2023-24 in KToE?"},
        {"no": "5", "query": "Diesel consumption by transport sector in petajoules for 2022-23"},
    ],
}


def load_queries(dataset_filter=None, query_filter=None, run_all=False):
    """Load queries from CSV files or fallback."""
    queries = []

    specific_dataset = None
    specific_no = None
    if query_filter:
        parts = query_filter.split(":")
        specific_dataset = parts[0].upper()
        specific_no = parts[1] if len(parts) > 1 else None

    datasets = VALID_DATASETS
    if dataset_filter:
        datasets = [dataset_filter.upper()]
    elif specific_dataset:
        datasets = [specific_dataset]

    for ds in datasets:
        csv_path = QUERIES_DIR / f"claude_queries_{ds}.csv"

        if csv_path.exists():
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                ds_queries = list(reader)

            for q in ds_queries:
                q["_dataset"] = ds
                if specific_no and q.get("no") != specific_no:
                    continue
                queries.append(q)

            if not run_all and not query_filter:
                ds_entries = [q for q in queries if q["_dataset"] == ds]
                if len(ds_entries) > 2:
                    keep = ds_entries[:2]
                    queries = [q for q in queries if q["_dataset"] != ds] + keep
        else:
            fallback = FALLBACK_QUERIES.get(ds, [])
            for q in fallback:
                q["_dataset"] = ds
                if specific_no and q.get("no") != specific_no:
                    continue
                queries.append(q)

    return queries


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="MoSPI MCP eval via Claude API")
    parser.add_argument("--all", action="store_true", help="Run all queries (default: 2 per dataset)")
    parser.add_argument("--dataset", type=str, help="Run queries for a single dataset (e.g., PLFS)")
    parser.add_argument("--query", type=str, help="Run a single query (e.g., PLFS:1)")
    args = parser.parse_args()

    client = anthropic.Anthropic()

    queries = load_queries(
        dataset_filter=args.dataset,
        query_filter=args.query,
        run_all=args.all,
    )

    if not queries:
        print("No queries to run.")
        sys.exit(1)

    print(f"Running {len(queries)} queries against Claude API (Sonnet 4.5)")
    print(f"Scoring: PASS = got data from API AND values appear in Claude's response\n")

    results = []
    for q in queries:
        ds = q["_dataset"]
        qno = q.get("no", "?")
        query_text = q["query"]

        print(f"  [{ds} Q{qno}] {query_text[:70]}...")

        t0 = time.time()
        result = run_query(client, query_text)
        elapsed = time.time() - t0

        scores = score_result(result, ds)
        scores["dataset"] = ds
        scores["query_no"] = qno
        scores["elapsed"] = round(elapsed, 1)
        results.append(scores)

        status = "PASS" if scores["passed"] else "FAIL"
        detail = ""
        if not scores["got_data"]:
            detail = " (no data returned)"
        elif not scores["values_match"]:
            detail = f" (missing values: {scores['missing_values'][:3]})"

        print(f"    {status}{detail}  [{scores['num_tool_calls']} calls, {elapsed:.1f}s]")
        if scores["expected_values"]:
            print(f"    expected values: {scores['expected_values'][:5]}")
        if result.get("text"):
            preview = result["text"][:120].replace("\n", " ")
            print(f"    response: {preview}...")
        print()

    # Summary
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    got_data = sum(1 for r in results if r["got_data"])
    values_ok = sum(1 for r in results if r["values_match"])

    print(f"\n{'Dataset':<8} {'Q#':<4} {'Data':>6} {'Values':>8} {'Result':>8} {'Calls':>5}")
    print("-" * 45)

    for r in results:
        ck = lambda v: "Y" if v else "."
        status = "PASS" if r["passed"] else "FAIL"
        print(f"{r['dataset']:<8} {r['query_no']:<4} {ck(r['got_data']):>6} "
              f"{ck(r['values_match']):>8} {status:>8} {r['num_tool_calls']:>5}")

    print("-" * 45)
    print(f"\nGot data:     {got_data}/{total} ({100*got_data/total:.0f}%)")
    print(f"Values match: {values_ok}/{total} ({100*values_ok/total:.0f}%)")
    print(f"PASSED:       {passed}/{total} ({100*passed/total:.0f}%)")


if __name__ == "__main__":
    main()
