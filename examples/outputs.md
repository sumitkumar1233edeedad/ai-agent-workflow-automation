# AI Agent Workflows - Execution Outputs & Evaluation Audit

This document records the end-to-end execution logs, step results, decision rules evaluation, and formatted reporting artifacts for all **10 workflows** defined in [`data/workflows.xlsx`](file:///c:/Users/sumit/Downloads/ai-agent-workflow-automation/data/workflows.xlsx).

All test queries were directly extracted from the `Test_Questions` sheet of the assessment workbook and processed through the LangGraph State Machine powered by **LangChain `ChatOpenAI`**.

---

## Table of Contents
1. [WF001: Inventory Restock Check](#wf001-inventory-restock-check)
2. [WF002: Product Price Validation](#wf002-product-price-validation)
3. [WF003: Vendor File Processing](#wf003-vendor-file-processing)
4. [WF004: Product Description Generator](#wf004-product-description-generator)
5. [WF005: Customer Order Status](#wf005-customer-order-status)
6. [WF006: Duplicate Product Detection](#wf006-duplicate-product-detection)
7. [WF007: Marketing Campaign Brief](#wf007-marketing-campaign-brief)
8. [WF008: SEO Keyword Classification](#wf008-seo-keyword-classification)
9. [WF009: Employee Task Assignment](#wf009-employee-task-assignment)
10. [WF010: Workflow Performance Report](#wf010-workflow-performance-report)
11. [Edge Cases & Guardrail Enforcements](#edge-cases--guardrail-enforcements)

---

## WF001: Inventory Restock Check

- **Test Request**: `"Which products need restocking?"`
- **Assessment Objective**: Tests workflow selection and threshold logic (`current_stock < minimum_stock`).
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF001)`

### Execution Steps
1. `[SUCCESS]` **load_inventory**: Ingested 10 items from `sample_inventory.csv`.
2. `[SUCCESS]` **compare_and_identify_low_stock**: Identified 6 items where `current_stock < minimum_stock`.
3. `[SUCCESS]` **generate_restock_list**: Calculated suggested reorder batch sizes and purchase requisition costs.

### Formatted Output
```markdown
## [REPORT] Inventory Restock Requisition: WF001
**Summary**: Scanned 10 catalog items. 6 items breached minimum thresholds and require immediate purchase orders. Total estimated cost: $4,328.00.

| SKU      | Product Name                   | Category    | Current Stock | Min Threshold | Suggested Reorder | Est. Cost ($) |
| -------- | ------------------------------ | ----------- | ------------- | ------------- | ----------------- | ------------- |
| SKU-1001 | Ergonomic Mechanical Keyboard  | Electronics | 4             | 15            | 26                | $1,170.00     |
| SKU-1003 | Wireless Vertical Mouse        | Electronics | 2             | 20            | 38                | $703.00       |
| SKU-1005 | Anodized Aluminum Laptop Stand | Accessories | 5             | 25            | 45                | $630.00       |
| SKU-1007 | Dual Monitor Arm Mount         | Furniture   | 3             | 10            | 17                | $714.00       |
| SKU-1008 | Full Grain Leather Desk Mat    | Accessories | 1             | 12            | 23                | $506.00       |
| SKU-1009 | LED Screen Light Bar           | Accessories | 8             | 15            | 22                | $605.00       |
```

---

## WF002: Product Price Validation

- **Test Request**: `"Find products where vendor price differs by more than 10%."`
- **Assessment Objective**: Tests comparison and decision logic (flag variance `> 10%`).
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF002)`

### Execution Steps
1. `[SUCCESS]` **load_product_prices**: Loaded 12 internal catalog products and 10 vendor price records.
2. `[SUCCESS]` **match_and_compare_prices**: Merged 10 products on SKU and computed price delta percentage.
3. `[WARNING]` **flag_exceptions**: Flagged 5 items exceeding the 10% tolerance threshold.

### Formatted Output
```markdown
## [REPORT] Product Price Validation & Variance: WF002
**Summary**: Validated 10 matched SKUs. Found 5 pricing exceptions exceeding the 10% tolerance threshold.

| SKU      | Product Name                       | Internal ($) | Vendor ($) | Variance (%)   | Status          |
| -------- | ---------------------------------- | ------------ | ---------- | -------------- | --------------- |
| SKU-1001 | Ergonomic Mechanical Keyboard      | $69.99       | $68.50     | -2.13%         | [OK]            |
| SKU-1002 | Ultra-Wide Curved Monitor 34-inch  | $399.99      | $460.00    | +15.00%        | [FLAGGED >10%]  |
| SKU-1003 | Wireless Vertical Mouse            | $34.99       | $35.00     | +0.03%         | [OK]            |
| SKU-1004 | Noise Cancelling Studio Headphones | $149.99      | $125.00    | -16.66%        | [FLAGGED >10%]  |
| SKU-1005 | Anodized Aluminum Laptop Stand     | $29.99       | $26.00     | -13.34%        | [FLAGGED >10%]  |
| SKU-1006 | Braided USB-C Fast Charging Cable  | $9.99        | $10.00     | +0.10%         | [OK]            |
| SKU-1007 | Dual Monitor Arm Mount             | $79.99       | $95.00     | +18.77%        | [FLAGGED >10%]  |
| SKU-1008 | Full Grain Leather Desk Mat        | $44.99       | $44.00     | -2.20%         | [OK]            |
| SKU-1009 | LED Screen Light Bar               | $49.99       | $58.00     | +16.02%        | [FLAGGED >10%]  |
| SKU-1010 | Mesh High Back Office Chair        | $219.99      | $220.00    | +0.00%         | [OK]            |
```

---

## WF003: Vendor File Processing

- **Test Request**: `"Process this vendor spreadsheet and show invalid rows."`
- **Assessment Objective**: Tests file ingestion and validation (rows missing SKU or Product Name are invalid).
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF003)`

### Execution Steps
1. `[SUCCESS]` **read_and_normalize_columns**: Scanned 7 records from `sample_vendor_products.csv`.
2. `[WARNING]` **validate_required_fields**: Validated required fields: 4 clean rows, 3 invalid rows.
3. `[SUCCESS]` **produce_cleaned_dataset**: Exported sanitized dataset and generated invalid row report.

### Formatted Output
```markdown
## [REPORT] Vendor Ingestion Validation: WF003
**Summary**: Processed vendor dataset. Validated 4 clean rows; isolated 3 invalid rows violating mandatory SKU or Product Name rules.

### Invalid Rows Detail
| Row # | Rejection Reason(s)                                | Snapshot Data                                                              |
| ----- | -------------------------------------------------- | -------------------------------------------------------------------------- |
| 4     | Missing required SKU                               | {'Vendor_SKU': '', 'Product_Title': 'Ergonomic Under-Desk Footrest', ...}  |
| 5     | Missing required Product Name                      | {'Vendor_SKU': 'VND-2004', 'Product_Title': '', 'Category_Name': ...}      |
| 7     | Missing required SKU, Missing required Product Name| {'Vendor_SKU': '', 'Product_Title': '', 'Wholesale_Cost': '0.00', ...}     |
```

---

## WF004: Product Description Generator

- **Test Request**: `"Generate SEO content for this product."`
- **Assessment Objective**: Tests LLM workflow and missing-data handling (explicitly flag missing attributes, do not hallucinate).
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF004)`

### Execution Steps
1. `[SUCCESS]` **validate_required_attributes**: Inspected catalog attributes for `Ergonomic Mechanical Keyboard`. Missing: None.
2. `[SUCCESS]` **generate_copy_and_seo**: LangChain ChatOpenAI generated descriptions and meta tags.

### Formatted Output
```json
{
  "description": "Designed to exceed expectations, the Ergonomic Mechanical Keyboard delivers uncompromising performance in the Electronics category. Constructed using ABS Plastic & Aluminum and finished in Matte Black, it elevates the daily workflow of Software Engineers & Gamers.",
  "short_description": "Premium Ergonomic Mechanical Keyboard crafted in Matte Black with tactile switches for high performance.",
  "seo_title": "Ergonomic Mechanical Keyboard | Premium Electronics",
  "meta_description": "Discover the Ergonomic Mechanical Keyboard in Matte Black, engineered with ABS Plastic & Aluminum for Software Engineers & Gamers. Shop today!",
  "missing_attributes": "None"
}
```

---

## WF005: Customer Order Status

- **Test Request**: `"Where is order ORD-1001?"`
- **Assessment Objective**: Tests lookup and missing-order handling.
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF005)`

### Execution Steps
1. `[SUCCESS]` **validate_identifier**: Validated search query identifier `ORD-1001`.
2. `[SUCCESS]` **retrieve_status_and_shipment**: Retrieved record for Alice Johnson; status `Shipped`.
3. `[SUCCESS]` **summarize_current_status**: Compiled fulfillment and live shipment tracking summary.

### Formatted Output
```markdown
## [REPORT] Customer Order Status: WF005
**Summary**: Order ORD-1001 for Alice Johnson is currently Shipped.

- **Order ID**: ORD-1001
- **Customer**: Alice Johnson (alice.j@example.com)
- **Status**: Shipped
- **Total Amount**: $184.98
- **Carrier**: FedEx (Tracking: FX-9823412349US)
- **Shipment Location**: In Transit, Spokane, WA Facility
- **Destination**: Seattle, WA
```

---

## WF006: Duplicate Product Detection

- **Test Request**: `"Find likely duplicate products in the catalog."`
- **Assessment Objective**: Tests similarity and confidence scoring (Exact SKU match vs. high attribute similarity).
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF006)`

### Execution Steps
1. `[SUCCESS]` **load_products**: Ingested 12 catalog products from `sample_products.csv`.
2. `[WARNING]` **group_and_score_duplicates**: Detected 2 duplicate clusters across catalog.

### Formatted Output
```markdown
## [REPORT] Catalog Duplicate Audit: WF006
**Summary**: Catalog audit identified 2 potential duplicate product clusters.

| Item A (SKU)                                  | Item B (SKU)                                                    | Confidence Level          | Match Reason                                                  |
| --------------------------------------------- | --------------------------------------------------------------- | ------------------------- | ------------------------------------------------------------- |
| Noise Cancelling Headphones (SKU-1004)        | Noise Cancelling Studio Headphones - Special Edition (SKU-1004) | High (Definite Duplicate) | Identical SKU 'SKU-1004' shared across catalog entries.       |
| Anodized Aluminum Laptop Stand (SKU-1005)     | Anodized Aluminium Laptop Stand - Silver (SKU-1011)             | High (Likely Duplicate)   | Product title similarity score 85.7%; matching category: True.|
```

---

## WF007: Marketing Campaign Brief

- **Test Request**: `"Create a campaign brief for the new collection."`
- **Assessment Objective**: Tests structured content generation and parameter completeness.
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF007)`

### Execution Steps
1. `[SUCCESS]` **validate_inputs**: Checked campaign goals, target audience, and dates.
2. `[SUCCESS]` **create_brief_and_channels**: Synthesized strategic brief and activation checklist via LangChain ChatOpenAI.

### Formatted Output
```json
{
  "objective": "Launch and drive adoption for the Q4 Ergonomic Workstation Collection",
  "audience": "Tech Professionals & Modern Ergonomic Shoppers",
  "messaging": "Elevate your productivity and ergonomics with precision-engineered workstation essentials.",
  "channels": [
    "Email Marketing",
    "Search Ads (Google Ads)",
    "Social Media (LinkedIn & Instagram)",
    "On-Site Merchandising"
  ],
  "timeline": "Nov 1, 2026 - Nov 30, 2026 (Black Friday / Cyber Week)",
  "checklist": [
    "Finalize landing page copy and conversion tracking pixels",
    "Verify promotional discount codes in checkout system",
    "Schedule email sequence deployment",
    "Prepare social media creative assets and creator unboxing clips",
    "Review customer support team FAQs regarding shipping & warranty"
  ]
}
```

---

## WF008: SEO Keyword Classification

- **Test Request**: `"Classify these keywords and map them to pages."`
- **Assessment Objective**: Tests classification and mapping (informational, commercial, transactional, navigational).
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF008)`

### Execution Steps
1. `[SUCCESS]` **read_keywords**: Ingested 12 keyword entries from `sample_keywords.csv`.
2. `[SUCCESS]` **remove_duplicates**: Deduplicated 1 duplicate keyword row.
3. `[SUCCESS]` **classify_and_map_intent**: Mapped 4-way search intents and target page architecture.
4. `[SUCCESS]` **export_results**: Saved results to `data/classified_keywords_export.csv`.

### Formatted Output
```markdown
## [REPORT] SEO Keyword Classification Matrix: WF008
**Summary**: Audited 12 search queries (1 duplicate removed). Classified intent and mapped target landing pages.

| Keyword                                     | Intent        | Priority | Target Category     | Recommended Landing Page                   |
| ------------------------------------------- | ------------- | -------- | ------------------- | ------------------------------------------ |
| buy ergonomic mechanical keyboard           | Transactional | High     | Keyboards & Input   | /product or /checkout for Keyboards & Input|
| best noise cancelling studio headphones 2026| Commercial    | High     | Audio               | /collection or buying-guide for Audio      |
| what is a curved monitor good for           | Informational | Medium   | Monitors            | /blog or learning-center article           |
| techlogix login account                     | Navigational  | Medium   | Account Portal      | /account or /support portal                |
| order wireless vertical mouse online        | Transactional | High     | Mice & Accessories  | /product or /checkout for Mice & Accessorie|
| anodized aluminum laptop stand review       | Commercial    | High     | Laptop Stands       | /collection or buying-guide for Laptop Stan|
| how to fix wrist pain from mouse            | Informational | Medium   | Blog & Health       | /blog or learning-center article           |
| discount code mesh office chair             | Transactional | High     | Chairs & Seating    | /product or /checkout for Chairs & Seating |
| usb-c 100w fast charging cable price        | Transactional | High     | Cables & Power      | /product or /checkout for Cables & Power   |
| download monitor calibration software       | Navigational  | Medium   | Downloads & Support | /account or /support portal                |
| top rated dual monitor arms for desk        | Commercial    | High     | Desk Mounts         | /collection or buying-guide for Desk Mounts|
```

---

## WF009: Employee Task Assignment

- **Test Request**: `"Assign this urgent task to the best available developer."`
- **Assessment Objective**: Tests ranking and decision logic (skill overlap, bandwidth capacity, escalation rule).
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF009)`

### Execution Steps
1. `[SUCCESS]` **understand_task_requirements**: Parsed requirements: Priority=URGENT, Skills=['Python', 'FastAPI', 'PostgreSQL'].
2. `[SUCCESS]` **rank_and_select_candidate**: Evaluated competencies, workload hours, and ratings. Selected Sarah Chen (Composite Score: 0.865).
3. `[SUCCESS]` **generate_assignment_summary**: Created assignment ticket and task summary.

### Formatted Output
```markdown
## [REPORT] Employee Task Assignment: WF009
**Summary**: Successfully assigned task to Sarah Chen (Senior Full-Stack Developer). Skill match and capacity verified.

### Selected Assignee Details
- **Assigned Employee**: Sarah Chen (EMP-001)
- **Role**: Senior Full-Stack Developer (Engineering)
- **Composite Suitability Score**: 0.865
- **Matched Competencies**: Python, FastAPI, PostgreSQL
- **Free Available Capacity**: 22.0 hours (Workload: 18/40 hrs)
- **Performance Rating**: 4.9 / 5.0
```

---

## WF010: Workflow Performance Report

- **Test Request**: `"Which workflows are failing most often?"`
- **Assessment Objective**: Tests aggregation and reporting (flag workflows where failure rate > 10% or slow execution time).
- **State Machine Status**: `COMPLETED`
- **Routing Logic**: `Matched via LangChain ChatOpenAI router (WF010)`

### Execution Steps
1. `[SUCCESS]` **load_execution_logs**: Ingested 25 log traces from `sample_workflow_logs.csv`.
2. `[WARNING]` **calculate_metrics_and_flag**: Identified workflows violating failure rate (>10%) or latency (>3.0s) thresholds.
3. `[SUCCESS]` **generate_recommendations**: Generated engineering remediation action items.

### Formatted Output
```markdown
## [REPORT] Workflow Reliability & SLA Performance: WF010
**Summary**: Aggregated 25 execution runs across 10 workflows. Flagged workflows violating failure rate (>10%) or latency (>3.0s) guidelines.

| Workflow ID | Total Runs | Successes | Failures | Failure Rate (%) | Avg Latency (s) | SLA Status     |
| ----------- | ---------- | --------- | -------- | ---------------- | --------------- | -------------- |
| WF001       | 3          | 3         | 0        | 0.0%             | 1.23s           | [OK] Healthy   |
| WF002       | 2          | 2         | 0        | 0.0%             | 1.48s           | [OK] Healthy   |
| WF003       | 4          | 2         | 2        | 50.0%            | 3.60s           | [FLAGGED >10%] |
| WF004       | 2          | 2         | 0        | 0.0%             | 3.25s           | [FLAGGED >3s]  |
| WF005       | 3          | 2         | 1        | 33.3%            | 1.35s           | [FLAGGED >10%] |
| WF006       | 2          | 2         | 0        | 0.0%             | 2.50s           | [OK] Healthy   |
| WF007       | 2          | 1         | 1        | 50.0%            | 2.10s           | [FLAGGED >10%] |
| WF008       | 2          | 2         | 0        | 0.0%             | 2.88s           | [OK] Healthy   |
| WF009       | 2          | 2         | 0        | 0.0%             | 1.78s           | [OK] Healthy   |
| WF010       | 2          | 2         | 0        | 0.0%             | 1.55s           | [OK] Healthy   |

### Recommended Actions
1. **Remediate WF003**: Failure rate is 50.0% (missing SKU & corrupted rows in vendor files). Implement pre-upload validation.
2. **Remediate WF005**: Failure rate is 33.3% due to OrderNotFoundError for unindexed IDs. Prompt user for alternate identifiers.
3. **Remediate WF007**: Failure rate is 50.0% due to missing launch dates in requests.
```

---

## Edge Cases & Guardrail Enforcements

### 1. Order Not Found (WF005)
- **Input Query**: `"Where is order ORD-9999?"`
- **Output Status**: `WARNING`
- **Response**: `No order found matching 'ORD-9999'. Please provide a valid Order ID (e.g. ORD-1001) or customer email.`

### 2. Missing Campaign Dates (WF007)
- **Input Query**: `"Create a campaign brief for flash sale with missing dates"`
- **Output Status**: `WARNING`
- **Response**: `Cannot generate campaign brief without target launch dates and timeline. Please provide campaign start and end dates.`

### 3. Attribute Guardrails (WF004)
- **Rule**: Never hallucinate missing attributes. Missing attributes are explicitly marked as `MISSING` or excluded.
