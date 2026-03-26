import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, HTTPException, Depends

from llm_client import call_llm
from supply_planrun import run_supply_plan,create_release_plan,run_data_collection,get_collection_status
from utils.formatter import format_run_response,format_release_response, format_collection_response,format_collection_status_response
from config import SUPPLY_PLAN_ID
from pegging_services import get_transaction_ids
from pegging_services import get_all_pegged_details
from supply_planrun import get_planned_orders



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

import asyncio
from fastapi import Depends

@app.post("/run-plan")
async def run_plan(
    payload: UserQuery,
    username: str = Depends(authenticate_user)
):
    print("🔥 RUN PLAN endpoint triggered")
    print("Incoming payload:", payload)


    loop = asyncio.get_running_loop()

    response = await loop.run_in_executor(
        None,
        run_supply_plan_agent,
        payload.query
    )

    return {"response": response}



@app.post("/release-plan")
async def release_plan(username: str = Depends(authenticate_user)):

    print("🔥 RELEASE PLAN ENDPOINT HIT")

    loop = asyncio.get_running_loop()

    fusion_response = await loop.run_in_executor(
        None, create_release_plan
    )

    formatted = format_release_response(fusion_response)

    return {"response": formatted}


@app.get("/transactions")
async def get_transactions(username: str = Depends(authenticate_user)):

    print("🔥 TRANSACTION ENDPOINT HIT")

    loop = asyncio.get_running_loop()

    transactions = await loop.run_in_executor(
        None,
        get_transaction_ids
    )

    return {
        "planId": SUPPLY_PLAN_ID,
        "transactionIds": transactions
    }

@app.get("/pegged-details")
async def pegged_details(username: str = Depends(authenticate_user)):

    print("🔥 PEGGED DETAILS ENDPOINT HIT")

    loop = asyncio.get_running_loop()

    results = await loop.run_in_executor(
        None,
        get_all_pegged_details
    )

    return {
        "planId": SUPPLY_PLAN_ID,
        "peggedDemands": results
    }

@app.get("/planned-orders")
async def planned_orders(username: str = Depends(authenticate_user)):

    print("🔥 PLANNED ORDERS ENDPOINT HIT")

    loop = asyncio.get_running_loop()

    results = await loop.run_in_executor(
        None,
        get_planned_orders
    )

    return {
        "planId": SUPPLY_PLAN_ID,
        "plannedOrders": results
    }
from OTBI_report import call_fusion, extract_report_bytes, extract_fault, excel_to_json
from fastapi import Query
import base64
# -----------------------------
# API
# -----------------------------
@app.get("/getReport")
def get_report(
    reportXDOpath: str = Query(None),
    limit: int = Query(1000)   # 👈 ADD THIS
):
    try:
        # ✅ TEMP: Hardcoded path (for testing)
        if not reportXDOpath:
            reportXDOpath = "/Rapidflow/RF_Report2.xdo"
            print(" Using default report path:", reportXDOpath)
        else:
            print(" Using user input report path:", reportXDOpath)

        # 🔥 Call Fusion
        response = call_fusion(reportXDOpath)

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            fault = extract_fault(response.text)
            raise HTTPException(status_code=500, detail=fault)

        report_b64 = extract_report_bytes(response.text)

        if not report_b64:
            fault = extract_fault(response.text)
            raise HTTPException(status_code=500, detail=fault)

        report_bytes = base64.b64decode(report_b64.strip())

        print("Excel size:", len(report_bytes))

        # 🔥 Convert Excel → JSON
        json_data = excel_to_json(report_bytes)

        # 👇 LIMIT DATA
        limited_data = json_data[:limit]

        return {
            "data": limited_data,
            "count": len(json_data),
            "returned": len(limited_data)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/run-collection")
async def run_collections(username: str = Depends(authenticate_user)):

    print("🔥 DATA COLLECTION ENDPOINT HIT")

    loop = asyncio.get_running_loop()

    # Call the function in a thread to avoid blocking
    response = await loop.run_in_executor(
        None,
        run_data_collection
    )

    formatted = format_collection_response(response)

    return {"response": formatted}

@app.get("/collection-status")
async def collection_status(username: str = Depends(authenticate_user)):

    print("🔥 COLLECTION STATUS ENDPOINT HIT")

    loop = asyncio.get_running_loop()

    response = await loop.run_in_executor(
        None,
        get_collection_status
    )

    formatted = format_collection_status_response(response)

    return {"response": formatted}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("planrun_main:app", host="0.0.0.0", port=8006, reload=True)
