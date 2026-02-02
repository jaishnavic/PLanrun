def format_run_response(plan_id: int, mode: int, data: dict) -> str:
    return f"""
Supply Plan Execution Triggered ✅

Plan ID       : {plan_id}
Execution Mode: {mode}
Execution ID  : {data.get('ExecutionId')}
Job ID        : {data.get('JobId')}

The supply plan has been submitted for execution.
"""
