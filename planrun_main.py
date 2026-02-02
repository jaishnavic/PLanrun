import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, HTTPException, Depends

from llm_client import call_llm
from supply_planrun import run_supply_plan
from utils.formatter import format_run_response
from config import SUPPLY_PLAN_ID

app = FastAPI(title="Supply Plan Runs Agent")

# ---------------- AUTH ----------------
security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if (
        credentials.username == os.getenv("PLAN_USERNAME")
        and credentials.password == os.getenv("PLAN_PASSWORD")
    ):
        return credentials.username
    raise HTTPException(status_code=401, detail="Unauthorized")


class UserQuery(BaseModel):
    query: str

def run_supply_plan_agent(user_input: str) -> str:
    llm_output = call_llm(user_input)

    if llm_output.get("intent") != "RUN_SUPPLY_PLAN":
        return "❌ Unable to identify a supply plan run request."

    # 🔒 Fixed mode for now (FULL)
    mode = 3

    fusion_response = run_supply_plan(mode)

    return format_run_response(
        plan_id=SUPPLY_PLAN_ID,
        mode=mode,
        data=fusion_response
    )

@app.get("/")
def read_root():
    return {"message": "Supply Plan Runs Agent is running."}

@app.post("/run-plan")
def run_plan(payload: UserQuery,username: str = Depends(authenticate_user)):
    return {
        "response": run_supply_plan_agent(payload.query)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("planrun_main:app", host="0.0.0.0", port=8004, reload=True)
