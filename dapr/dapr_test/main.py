from contextlib import asynccontextmanager
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp, DaprActor
from pydantic import BaseModel

# Lifespan handler for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Register Dapr actor
    await actor.register_actor(DemoActor, DemoActorInterface)
    yield
    # Shutdown: Cleanup if needed
    print("Shutting down FastAPI with Dapr")

# FastAPI app with lifespan
app = FastAPI(title="FastAPI with Dapr", lifespan=lifespan)

# Dapr FastAPI extension
dapr_app = DaprApp(app)

# Pydantic models for structured data
class User(BaseModel):
    id: int
    name: str = "Jane Doe"

class CloudEventModel(BaseModel):
    data: User
    datacontenttype: str
    id: str
    pubsubname: str
    source: str
    specversion: str
    topic: str
    traceid: str
    traceparent: str
    tracestate: str
    type: str

# Basic FastAPI route
@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI with Dapr!"}

# Dapr pub/sub subscription for CloudEvents
@dapr_app.subscribe(pubsub="pubsub", topic="user_topic")
def user_event_handler(event_data: CloudEventModel):
    print(f"Received user event: {event_data}")
    return {"status": "Event received", "user": event_data.data}

# Dapr actor example
from dapr.actor import ActorInterface, actormethod

class DemoActorInterface(ActorInterface):
    @actormethod(name="GetMyData")
    async def get_my_data(self) -> dict:
        pass

class DemoActor:
    async def get_my_data(self) -> dict:
        return {"message": "Data from DemoActor"}

# Initialize Dapr actor
actor = DaprActor(app)