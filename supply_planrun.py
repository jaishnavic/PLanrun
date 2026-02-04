import requests
from requests.auth import HTTPBasicAuth
from config import (
    FUSION_BASE_URL,
    FUSION_USERNAME,
    FUSION_PASSWORD,
    SUPPLY_PLAN_ID
)


SUPPLIER_ENDPOINT = (
    f"/fscmRestApi/resources/11.13.18.05/supplyPlans/{SUPPLY_PLAN_ID}/child/Runs"
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
SUPPLY_PLAN_ID_RELEASE = "300000320243039"

RELEASE_ENDPOINT = (
    f"/fscmRestApi/resources/11.13.18.05/supplyChainPlans/{SUPPLY_PLAN_ID_RELEASE}/child/Releases"
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

