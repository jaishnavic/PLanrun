import requests
from requests.auth import HTTPBasicAuth
from config import (
    FUSION_BASE_URL,
    FUSION_USERNAME,
    FUSION_PASSWORD,
    SUPPLY_PLAN_ID
)


SUPPLIER_ENDPOINT = (
    f"/fscmRestApi/resources/11.13.18.05/demandAndSupplyPlans/{SUPPLY_PLAN_ID}/child/Runs"
)

def run_supply_plan(mode: int) -> dict:
    url = f"{FUSION_BASE_URL}{SUPPLIER_ENDPOINT}"

    headers = {
        # 🔴 REQUIRED for Fusion child resources
        "Content-Type": "application/vnd.oracle.adf.resourceitem+json",
        "Accept": "application/json",
        "REST-Framework-Version": "4"
    }

    payload = {
        "Mode": int(mode)
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        auth=HTTPBasicAuth(FUSION_USERNAME, FUSION_PASSWORD),
        timeout=30
    )

    # 🔍 DEBUG (temporary – keep while testing)
    print("Fusion URL:", url)
    print("Fusion Status:", response.status_code)
    print("Fusion Headers:", response.headers)
    print("Fusion Body:", response.text)

    if response.status_code not in (200, 201):
        raise Exception(
            f"Fusion API Error | Status: {response.status_code}"
        )

    return response.json()
# SUPPLY_PLAN_ID_RELEASE = "300000291667931"


RELEASE_ENDPOINT = (
    f"/fscmRestApi/resources/11.13.18.05/supplyChainPlans/{SUPPLY_PLAN_ID}/child/Releases"
)

def create_release_plan() -> dict:
    url = f"{FUSION_BASE_URL}{RELEASE_ENDPOINT}"

    headers = {
        "Content-Type": "application/vnd.oracle.adf.resourceitem+json",
        "Accept": "application/json",
        "REST-Framework-Version": "4"
    }


    response = requests.post(
        url,
        headers=headers,
        json={},   # Empty body as per API
        auth=HTTPBasicAuth(FUSION_USERNAME, FUSION_PASSWORD),
        timeout=30
    )

    # 🔍 Debug logs (keep during testing)
    print("Fusion URL:", url)
    print("Fusion Status:", response.status_code)
    print("Fusion Body:", response.text)

    if response.status_code not in (200, 201):
        raise Exception(
            f"Fusion Release API Error | Status: {response.status_code} | Body: {response.text}"
        )

    return response.json()

#RunCollections Endpoint

Run_Collections_Endpoint = (f"/fscmRestApi/resources/11.13.18.05/dataCollections")

def run_data_collection() -> dict:
    url = f"{FUSION_BASE_URL}{Run_Collections_Endpoint}"
    headers = {
       
            "Content-Type": "application/json",
            "Accept": "application/json",
            "REST-Framework-Version": "4"
        }

    payload ={
            "TemplateName": "RFA1",
            "SourceSystem": "OPS",
            "CollectionType": "1"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,   # Empty body as per API
        auth=HTTPBasicAuth(FUSION_USERNAME, FUSION_PASSWORD),
        timeout=30
    )

    if response.status_code not in (200, 201):
        raise Exception(
            f"Fusion Release API Error | Status: {response.status_code} | Body: {response.text}"
        )

    return response.json()

collection_status_endpoint = ("/fscmRestApi/resources/11.13.18.05/dataCollections")

def get_collection_status() -> dict:

    url = f"{FUSION_BASE_URL}{collection_status_endpoint}?limit=50"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "REST-Framework-Version": "4"
    }

    response = requests.get(
        url,
        headers=headers,
        auth=HTTPBasicAuth(FUSION_USERNAME, FUSION_PASSWORD),
        timeout=30
    )

    if response.status_code not in (200, 201):
        raise Exception(
            f"Fusion Collection Status API Error | Status: {response.status_code} | Body: {response.text}"
        )

    data = response.json()

    # 🔹 Simplify response for agent
    simplified_items = []

    for item in data.get("items", []):
        simplified_items.append({
            "essJobId": str(item.get("ESSCollectionJobId")),
            "phase": item.get("ProcPhase"),
            "status": item.get("Status"),
            "startTime": item.get("StartTime"),
            "endTime": item.get("EndTime"),
            "refreshNumber": item.get("RefreshNumber"),
            "instanceId": item.get("InstanceId")
        })

    return {"items": simplified_items}
#Supply details

from pegging_services import get_transaction_ids


def get_planned_orders(limit: int = 10):

    transactions = get_transaction_ids(limit)

    planned_orders = []

    headers = {
        "Accept": "application/json",
        "REST-Framework-Version": "4"
    }

    for tx in transactions:

        endpoint = f"/fscmRestApi/resources/11.13.18.05/supplyPlans/{SUPPLY_PLAN_ID}/child/PlanningSupplies/{tx}"
        url = f"{FUSION_BASE_URL}{endpoint}"

        params = {
            "onlyData": "true"
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(FUSION_USERNAME, FUSION_PASSWORD),
            timeout=30
        )

        print("Fusion Supplies URL:", response.url)
        print("Fusion Status:", response.status_code)

        if response.status_code != 200:
            raise Exception(
                f"Fusion Supplies API Error | Status: {response.status_code} | Body: {response.text}"
            )

        item = response.json()

        planned_orders.append({

            "transactionId": tx,

            "itemDescription": item.get("ItemDescription"),
            "item": item.get("Item"),
            "organization": item.get("Organization"),
            "orderType": item.get("OrderTypeText"),
            "firmStatus": item.get("FirmStatus"),

            "orderNumber": item.get("OrderNumber"),
            "orderQuantity": item.get("OrderQuantity"),

            "planId": item.get("PlanId"),
            "makeOrBuy": item.get("MakeOrBuy"),

            "suggestedOrderDate": item.get("SuggestedOrderDate"),
            "suggestedStartDate": item.get("SuggestedStartDate"),
            "suggestedDockDate": item.get("SuggestedDockDate"),
            "suggestedDueDate": item.get("SuggestedDueDate"),

            "suggestedShipDate": item.get("SuggestedShipDate"),
            "suggestedCompletionDate": item.get("SuggestedCompletionDate"),

            "needByDate": item.get("NeedByDate"),
            "originalNeedByDate": item.get("OriginalNeedByDate"),
            "lastUpdateDate": item.get("LastUpdateDate"),

            "promisedArrivalDate": item.get("PromisedArrivalDate"),
            "promisedShipDate": item.get("PromisedShipDate"),

            "requestedArrivalDate": item.get("RequestedArrivalDate"),
            "requestedShipDate": item.get("RequestedShipDate"),

            "rescheduleDays": item.get("RescheduleDays"),
            "rescheduled": item.get("Rescheduled"),
            "compressionDays": item.get("CompressionDays"),

            "scheduledShipDate": item.get("ScheduledShipDate"),

            "reservedQuantity": item.get("ReservedQuantity"),
            "releaseStatusText": item.get("ReleaseStatusText"),
        })

    return planned_orders

item_details = f"/fscmRestApi/resources/11.13.18.05/supplyPlans/{SUPPLY_PLAN_ID}/child/Items"

def get_item_details()-> dict:

        url = f"{FUSION_BASE_URL}{item_details}"


        headers = {
            "Accept": "application/json",
            "REST-Framework-Version": "4"
        }

        response = requests.get(
            url,
            headers=headers,
            auth=HTTPBasicAuth(FUSION_USERNAME, FUSION_PASSWORD),
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(
                f"Fusion Item Details API Error | Status: {response.status_code} | Body: {response.text}"
            )

        return response.json()


PLAN_DETAILS_ENDPOINT = (
    f"/fscmRestApi/resources/11.13.18.05/plans/{SUPPLY_PLAN_ID}"
)

def get_plan_details() -> dict:
    url = f"{FUSION_BASE_URL}{PLAN_DETAILS_ENDPOINT}"

    headers = {
        "Accept": "application/json",
        "REST-Framework-Version": "4"
    }

    params = {
        "onlyData": "true"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        auth=HTTPBasicAuth(FUSION_USERNAME, FUSION_PASSWORD),
        timeout=30
    )

    print("Fusion Plan Details URL:", response.url)
    print("Fusion Status:", response.status_code)
    print("Fusion Body:", response.text)

    if response.status_code != 200:
        raise Exception(
            f"Fusion Plan Details API Error | Status: {response.status_code} | Body: {response.text}"
        )

    data = response.json()

    # 🔹 Simplified response
    return {
        "Plan ID": data.get("PlanId"),
        "Plan Name": data.get("PlanName"),
        "PlanCompletionDate": data.get("PlanCompletionDate"),
        "LastRunDate": data.get("LastRunDate"),
        "PlanCreationDate": data.get("CreationDate"),
        "PlanStartDate": data.get("PlanStartDate")
    }