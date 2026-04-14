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

Plan ID       : {resp.get('PlanId')}
Execution ID  : {resp.get('ExecutionId')}
ESS Job ID    : {resp.get('ESSJobId')}
Message       : {resp.get('Message')}

"""

def format_collection_response(resp: dict) -> str:
    return f"""
Data Collection Triggered ✅

Template Name    : {resp.get('TemplateName')}
Source System    : {resp.get('SourceSystem')}
Collection Type  : {resp.get('CollectionType')}
ESS Job ID : {resp.get('ESSCollectionJobId')}
Status : {resp.get('Status')}
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


def format_items_output(resp: dict) -> dict:

    items = resp.get("items", [])

    if not items:
        return {"items": [], "message": "No items found"}

    formatted_items = []

    for item in items:
        formatted_items.append({
            "ItemName": item.get("ItemName"),
            "Organization": item.get("Organization"),
            "MakeOrBuy": item.get("MakeOrBuy"),
            "ProcessingLeadTime": item.get("ProcessingLeadTime"),
            "PostprocessingLeadTime": item.get("PostprocessingLeadTime"),
            "PreprocessingLeadTime": item.get("PreprocessingLeadTime"),
            "VariableLeadTime": item.get("VariableLeadTime"),
            "FixedLeadTime": item.get("FixedLeadTime")
        })

    return {
        # "count": len(formatted_items),
        "items": formatted_items
    }

def format_plan_details(resp: dict) -> str:

    return f"""
Supply Plan Details 📊

Plan ID            : {resp.get('Plan ID')}
Plan Name          : {resp.get('Plan Name')}
Plan Start Date    : {resp.get('PlanStartDate')}
Plan Completion    : {resp.get('PlanCompletionDate')}
Last Run Date      : {resp.get('LastRunDate')}
Plan Created On    : {resp.get('PlanCreationDate')}
"""
