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