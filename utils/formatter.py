def format_run_response(plan_id: int, mode: int, data: dict) -> str:
    return f"""
Supply Plan Execution Triggered ✅

Plan ID       : {plan_id}
Execution Mode: {mode}
Execution ID  : {data.get('ExecutionId')}
Job ID        : {data.get('JobId')}

The supply plan has been submitted for execution.
"""

def format_release_response(data: dict) -> dict:
    """
    Formats Fusion Create Release response for user consumption.
    Removes internal links and keeps business-relevant fields.
    """

    if not isinstance(data, dict):
        return {"message": "Invalid release response from Fusion"}

    return {
        "planId": data.get("PlanId"),
        "executionId": data.get("ExecutionId"),
        "releaseStatus": data.get("ReleaseStatus"),
        "essJobId": data.get("ESSJobId"),
        "startDate": data.get("StartDate"),
        "endDate": data.get("EndDate"),
        "executionUser": data.get("ExecutionUser"),
        "planAction": data.get("PlanAction"),
        "message": data.get("Message", "")
    }
