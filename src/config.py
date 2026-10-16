import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from .models import WorkflowSpec

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("WORKFLOWS_DATA_DIR", PROJECT_ROOT / "data"))

def get_data_path(filename: str | Path) -> Path:
    """Resolve a file path relative to data directory, project root, or absolute path."""
    p = Path(filename)
    if p.is_absolute() and p.exists():
        return p
    # Check within DATA_DIR
    if (DATA_DIR / p.name).exists():
        return DATA_DIR / p.name
    # Check relative to cwd
    if p.exists():
        return p.resolve()
    # Check relative to PROJECT_ROOT
    if (PROJECT_ROOT / p).exists():
        return (PROJECT_ROOT / p).resolve()
    # Default to DATA_DIR / name
    return DATA_DIR / p.name

EXCEL = Path(os.getenv("WORKFLOWS_EXCEL_PATH", get_data_path("workflows.xlsx")))

def load_workflows() -> dict[str, WorkflowSpec]:
    target_excel = get_data_path(EXCEL)
    df = pd.read_excel(target_excel, sheet_name="Workflows")
    df.columns = [str(c).strip() for c in df.columns]
    
    # Handle steps and expected_output columns safely
    steps_col = "Steps" if "Steps" in df.columns else df.columns[4]
    cond_col = "Steps.1" if "Steps.1" in df.columns else (df.columns[5] if len(df.columns) > 5 else "")
    tools_col = "Tools_Required" if "Tools_Required" in df.columns else (df.columns[6] if len(df.columns) > 6 else "")
    
    specs = {}
    for _, row in df.iterrows():
        steps_raw = str(row[steps_col]) if steps_col and pd.notna(row.get(steps_col)) else ""
        steps = [s.strip() for s in steps_raw.split("→") if s.strip()]
        condition = str(row[cond_col]).strip() if cond_col and pd.notna(row.get(cond_col)) else ""
        tools = [t.strip() for t in str(row[tools_col]).split(";") if t.strip()] if tools_col and pd.notna(row.get(tools_col)) else []
        
        # Expected output column resolution (handles Excel offset where Unnamed: 7 holds values)
        expected_out = ""
        if "Unnamed: 7" in row and pd.notna(row["Unnamed: 7"]):
            expected_out = str(row["Unnamed: 7"]).strip()
        elif "Expected_Output" in row and pd.notna(row["Expected_Output"]):
            expected_out = str(row["Expected_Output"]).strip()
        
        wid = str(row["Workflow_ID"]).strip()
        specs[wid] = WorkflowSpec(
            id=wid,
            name=str(row["Workflow_Name"]).strip(),
            trigger=str(row["Trigger"]).strip(),
            inputs=[i.strip() for i in str(row["Inputs"]).split(";") if i.strip()] if pd.notna(row.get("Inputs")) else [],
            steps=steps,
            condition=condition,
            tools=tools,
            expected_output=expected_out,
        )
    return specs