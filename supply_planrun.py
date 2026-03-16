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

#Supply details

SUPPLIES_ENDPOINT = (
    f"/fscmRestApi/resources/11.13.18.05/supplyPlans/{SUPPLY_PLAN_ID}/child/PlanningSupplies"
)


def get_planned_orders(limit: int = 10):

    url = f"{FUSION_BASE_URL}{SUPPLIES_ENDPOINT}"

    headers = {
        "Accept": "application/json",
        "REST-Framework-Version": "4"
    }

    params = {
        "onlyData": "true",
        "limit": limit
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

    data = response.json()

    planned_orders = []

    for item in data.get("items", []):

        # if item.get("OrderTypeText") == "Planned order":

        planned_orders.append({
            "itemDescription": item.get("ItemDescription"),
            "item": item.get("Item"),
            "organization": item.get("Organization"),
            "orderType": item.get("OrderTypeText"),
            "firmStatus": item.get("FirmStatus"),

            "orderNumber": item.get("OrderNumber"),
            "orderQuantity": item.get("OrderQuantity"),

            "planId": item.get("PlanId"),
            "makeOrBuy": item.get("MakeOrBuy"),

            # Suggested planning dates (the four main planning dates)
            "suggestedOrderDate": item.get("SuggestedOrderDate"),
            "suggestedStartDate": item.get("SuggestedStartDate"),
            "suggestedDockDate": item.get("SuggestedDockDate"),
            "suggestedDueDate": item.get("SuggestedDueDate"),

            "suggestedShipDate": item.get("SuggestedShipDate"),

            # Need-by dates
            "needByDate": item.get("NeedByDate"),
            "originalNeedByDate": item.get("OriginalNeedByDate"),

            # Promised dates
            "promisedArrivalDate": item.get("PromisedArrivalDate"),
            "promisedShipDate": item.get("PromisedShipDate"),

            # Requested dates
            "requestedArrivalDate": item.get("RequestedArrivalDate"),
            "requestedShipDate": item.get("RequestedShipDate"),

            # Scheduling adjustments
            "rescheduleDays": item.get("RescheduleDays"),
            "rescheduled": item.get("Rescheduled"),
            "compressionDays": item.get("CompressionDays"),

            # Shipment scheduling
            "scheduledShipDate": item.get("ScheduledShipDate"),

            # Additional useful context
            "planner": item.get("Planner"),
            "releaseStatus": item.get("ReleaseStatusText")
        })

    return planned_orders


