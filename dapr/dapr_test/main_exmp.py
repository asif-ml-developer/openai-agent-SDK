from fastapi import FastAPI
from dapr.clients import DaprClient

app = FastAPI()

@app.get("/dapr/subscribe")
async def subscribe():
    return ["order-created"]

@app.post("/order-created")
async def handle_order(event: dict):
    order_id = event.get("data", {}).get("orderId")
    with DaprClient() as client:
        await client.save_state(store_name="statestore", key=f"order-{order_id}", value=event)
    return {"status": "Order saved"}