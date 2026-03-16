import requests
from requests.auth import HTTPBasicAuth

from config import (
    FUSION_BASE_URL,
    FUSION_USERNAME,
    FUSION_PASSWORD,
    SUPPLY_PLAN_ID
)

TRANSACTION_ENDPOINT = (
    f"/fscmRestApi/resources/11.13.18.05/supplyPlans/{SUPPLY_PLAN_ID}/child/PlanningSupplies"
)


def get_transaction_ids(limit: int = 20) -> list:

    url = f"{FUSION_BASE_URL}{TRANSACTION_ENDPOINT}"

    headers = {
        "Accept": "application/json",
        "REST-Framework-Version": "4"
    }

    params = {
        "q": "OrderType=5",   # filter planned orders
        "limit": limit,
        "onlyData": "true"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        auth=HTTPBasicAuth(FUSION_USERNAME, FUSION_PASSWORD),
        timeout=30
    )

    print("Fusion Transaction URL:", response.url)
    print("Fusion Status:", response.status_code)

    if response.status_code != 200:
        raise Exception(
            f"Fusion Transaction API Error | Status: {response.status_code} | Body: {response.text}"
        )

    data = response.json()

    transactions = [
        item["TransactionId"]
        for item in data.get("items", [])
        if item.get("TransactionId")
    ]

    return transactions



def get_pegged_demands(transaction_id: int) -> dict:

    endpoint = f"/fscmRestApi/resources/11.13.18.05/supplyPlans/{SUPPLY_PLAN_ID}/child/PlanningSupplies/{transaction_id}/child/PeggedDemands"

    url = f"{FUSION_BASE_URL}{endpoint}"

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

    print("Fusion Pegging URL:", response.url)
    print("Fusion Status:", response.status_code)

    if response.status_code != 200:
        raise Exception(
            f"Fusion Pegging API Error | Status: {response.status_code} | Body: {response.text}"
        )

    return response.json()


def extract_pegged_details(data: dict):

    results = []

    for item in data.get("items", []):

        results.append({
            "peggingId": item.get("PeggingId"),
            "item": item.get("Item"),
            "organization": item.get("Organization"),
            "orderType": item.get("OrderTypeText"),
            "orderNumber": item.get("OrderNumber"),
            "orderQuantity": item.get("OrderQuantity"),
            "peggedQuantity": item.get("PeggedQuantity"),
            "dueDate": item.get("SuggestedDueDate")
        })

    return results


def get_all_pegged_details():

    transactions = get_transaction_ids(limit=3)

    all_results = []

    for tx in transactions:

        pegged_data = get_pegged_demands(tx)

        extracted = extract_pegged_details(pegged_data)

        if extracted:
            all_results.append({
                "transactionId": tx,
                "demands": extracted
            })

    return all_results