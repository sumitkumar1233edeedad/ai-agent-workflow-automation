# 🤖 AI Agent Workflow Automation System

An enterprise-grade, autonomous workflow routing and execution engine powered by **LangGraph**, **LangChain (`langchain-openai`)**, and **Pydantic**.

The system dynamically parses business workflow specifications from [`data/workflows.xlsx`](file:///c:/Users/sumit/Downloads/ai-agent-workflow-automation/data/workflows.xlsx), routes natural language queries to discrete multi-step pipelines via LangChain's **`ChatOpenAI`** (supporting both OpenAI and OpenRouter) with intelligent semantic fallback, executes registered modular tools, enforces business rules and guardrails, and renders structured audit reports.

---

## 📁 Project Architecture & Layout

```
ai-agent-workflow-automation/
├── README.md                       # Comprehensive system documentation
├── requirements.txt                # Production & testing dependencies
├── pytest.ini                      # Pytest configuration with pythonpath
├── .env.example                    # Sample environment variables
├── .env                            # Active environment configuration
├── data/
│   ├── workflows.xlsx              # Master workflow specification file
│   ├── sample_inventory.csv        # Inventory levels and reorder batch sizes (WF001)
│   ├── sample_products.csv         # Product catalog with attributes and pricing (WF002, WF004, WF006)
│   ├── sample_vendor_prices.csv    # Vendor price lists with price variances (WF002)
│   ├── sample_vendor_products.csv  # Vendor spreadsheet with valid & invalid rows (WF003)
│   ├── sample_orders.json          # Customer order & carrier tracking records (WF005)
│   ├── sample_employees.json       # Employee competencies, workloads, and ratings (WF009)
│   ├── sample_keywords.csv         # SEO search queries with search volume & CPC (WF008)
│   ├── sample_workflow_logs.csv    # Historical execution logs and SLA telemetry (WF010)
│   ├── cleaned_vendor_products.csv # Cleaned vendor dataset output (WF003)
│   └── classified_keywords_export.csv # Exported keyword intent matrix (WF008)
├── src/
│   ├── __init__.py
│   ├── config.py                   # Excel parser & robust get_data_path path resolution
│   ├── llm.py                      # Centralized LangChain ChatOpenAI initialization
│   ├── models.py                   # Pydantic schemas: WorkflowSpec, AgentState
│   ├── selector.py                 # LangChain ChatOpenAI router with semantic rule fallback
│   ├── executor.py                 # LangGraph StateGraph orchestration pipeline
│   ├── tools/
│   │   ├── __init__.py             # Unified tool exports & registry lookup
│   │   ├── registry.py             # @tool decorator & lookup registry
│   │   ├── csv_tools.py            # Path-safe CSV/Excel parsing and validation
│   │   ├── calc_tools.py           # Mathematical evaluation & threshold checks
│   │   ├── llm_tools.py            # LangChain ChatOpenAI generative tool
│   │   ├── db_tools.py             # JSON database lookups (orders, employees)
│   │   └── report_tools.py         # Aggregators, threshold flaggers, ranking & formatting
│   ├── workflows/
│   │   ├── __init__.py             # Workflow handlers exports
│   │   └── handlers.py             # Modular business logic handlers for WF001–WF010
│   └── cli.py                      # Multi-flag CLI entrypoint
├── tests/
│   └── test_all_workflows.py       # End-to-end pytest suite running all 10 test questions
└── examples/
    └── outputs.md                  # Comprehensive execution traces, reports & audit logs
```

---

## 📊 Configured Business Workflows

All 10 workflows are dynamically ingested from `data/workflows.xlsx`:

| ID | Workflow Name | Trigger Intent | Tools Used | Business Logic Rule / Guardrail | Expected Output |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WF001** | Inventory Restock Check | *"Which products need restocking?"* | CSV reader, calculator | If `current_stock < minimum_stock`, mark for restock | Restock list with threshold & suggested reorder |
| **WF002** | Product Price Validation | *"Find products where vendor price differs by more than 10%."* | CSV reader, calculator | Flag when price difference exceeds `10%` | Price validation table with exceptions flagged |
| **WF003** | Vendor File Processing | *"Process this vendor spreadsheet and show invalid rows."* | Excel/CSV parser, data validator | Rows missing SKU or product name are invalid | Cleaned dataset file + invalid-row report |
| **WF004** | Product Description Generator | *"Generate SEO content for this product."* | LLM (`ChatOpenAI`), text validation | Do not invent missing attributes; explicitly mark missing | Product copy, short teaser, SEO title, meta desc |
| **WF005** | Customer Order Status | *"Where is order ORD-1001?"* | Order DB/API, shipment lookup | If no order found, ask for another identifier | Live order status, line items, carrier tracking |
| **WF006** | Duplicate Product Detection | *"Find likely duplicate products in the catalog."* | CSV reader, text similarity | Exact SKU match is definite; high similarity is possible | Deduplication clusters with confidence scoring |
| **WF007** | Marketing Campaign Brief | *"Create a campaign brief for the new collection."* | LLM (`ChatOpenAI`), catalog reader | If campaign goal or dates missing, request them | Strategic brief with channels & rollout checklist |
| **WF008** | SEO Keyword Classification | *"Classify these keywords and map them to pages."* | CSV reader, LLM/classifier | 4-way classification: informational, commercial, etc. | Deduplicated keyword matrix mapped to pages |
| **WF009** | Employee Task Assignment | *"Assign this urgent task to the best available developer."* | Employee DB, ranking logic | Prefer skills & capacity; escalate if no candidate fits | Recommended assignee, score, reasoning, summary |
| **WF010** | Workflow Performance Report | *"Which workflows are failing most often?"* | Log reader, calculator, reporting| Flag workflows with failure rate > 10% or slow steps | Aggregated metrics, error signatures, suggestions |

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12.9)
- Git

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create or edit your `.env` file in the project root:
```env
# Option A: OpenRouter API Key (LangChain ChatOpenAI)
openrouter_api_key=sk-or-v1-your-key-here
# OPENAI_MODEL=openai/gpt-4o-mini

# Option B: Standard OpenAI API Key
# OPENAI_API_KEY=sk-proj-your-key-here
# OPENAI_MODEL=gpt-4o-mini

# System Data Path (Optional override)
WORKFLOWS_DATA_DIR=data
WORKFLOWS_EXCEL_PATH=data/workflows.xlsx
LOG_LEVEL=INFO
```

> **Note on Zero-Failure Offline Resilience**: If no API key is set, the system seamlessly uses precision semantic trigger rules and local generative templates with 100% test pass rate.

---

## 🚀 Command-Line Interface (CLI)

Run requests directly from your terminal:

```bash
# List all configured business workflows
python -m src.cli --list

# WF001: Inventory restock check
python -m src.cli "Which products need restocking?"

# WF002: Product price validation
python -m src.cli "Find products where vendor price differs by more than 10%."

# WF003: Vendor spreadsheet validation
python -m src.cli "Process this vendor spreadsheet and show invalid rows."

# WF005: Order status lookup
python -m src.cli "Where is order ORD-1001?"

# WF008: Search intent classification (JSON format)
python -m src.cli "Classify these keywords and map them to pages." --json

# WF009: Employee task assignment
python -m src.cli "Assign this urgent task to the best available developer."

# WF010: System reliability & SLA performance report
python -m src.cli "Which workflows are failing most often?"
```

### CLI Options & Flags
- `--list` / `-l`: Displays catalog of all 10 business workflows from `workflows.xlsx`.
- `--json` / `-j`: Outputs state machine execution state in formatted JSON.
- `--workflow` / `-w`: Force execution of a specific workflow ID (e.g. `-w WF001`).
- `--verbose` / `-v`: Displays detailed execution logs.

---

## 🧪 Running the Test Suite

The test suite validates all 10 workflow queries from the `Test_Questions` sheet of `workflows.xlsx`:

```bash
pytest -v
```

### Test Coverage Highlights:
- ✅ **Dynamic Config Ingestion**: Automatically loads `data/workflows.xlsx` and handles Excel column shifts safely.
- ✅ **LangChain ChatOpenAI Routing**: Routes requests via `ChatOpenAI` (`langchain_openai`) with deterministic fallback.
- ✅ **Path Safety**: `get_data_path()` resolves files in `data/` whether invoked from project root, subfolders, or pytest.
- ✅ **10/10 Workflow Execution**:
  - Restock threshold validation (`current_stock < minimum_stock`)
  - Price variance threshold alerting (`>10%`)
  - Vendor data hygiene (missing SKU or product name flags)
  - Missing-data guardrails (no hallucinated attributes)
  - Order lookup recovery and missing identifier prompts
  - Multi-candidate ranking and capacity validation
  - SLA breach alerting (>10% failure rate)
- ✅ **State Graph Execution**: State transitions managed by LangGraph StateGraph engine.

---

## 📖 Evaluation Examples & Traces

Detailed execution outputs, traces, and audit reports for all 10 workflows are documented in [`examples/outputs.md`](file:///c:/Users/sumit/Downloads/ai-agent-workflow-automation/examples/outputs.md).
