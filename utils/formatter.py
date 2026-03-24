def format_run_response(plan_id: int, mode: int, data: dict) -> str:
    return f"""
Supply Plan Execution Triggered ✅

Plan ID       : {plan_id}
Execution Mode: {mode}
Execution ID  : {data.get('ExecutionId')}
Job ID        : {data.get('JobId')}

The supply plan has been submitted for execution.
"""

def format_release_response(resp):

    return f"""
Supply Plan Release Triggered ✅

Plan ID       : {resp.get('PlanId')}
Execution ID  : {resp.get('ExecutionId')}
ESS Job ID    : {resp.get('ESSJobId')}

The release process has been successfully submitted.
"""

def format_collection_response(resp: dict) -> str:
    return f"""
Data Collection Triggered ✅

Template Name    : {resp.get('TemplateName')}
Source System    : {resp.get('SourceSystem')}
Collection Type  : {resp.get('CollectionType')}
ESS Job ID : {resp.get('ESSCollectionJobId')}
Status : {resp.get('Status')}

The data collection process has been successfully submitted.
"""

def format_collection_status_response(resp: dict) -> str:

    items = resp.get("items", [])

    if not items:
        return "No collection status records found."

    message = "Data Collection Status (Latest Records) ✅\n\n"

    for item in items[:50]:  # limit display
        message += f"""
        ESS Job ID : {item.get('essJobId')}
        Phase      : {item.get('phase')}
        Status     : {item.get('status')}
        Start Time : {item.get('startTime')}
        End Time   : {item.get('endTime')}
    
        """

    return message