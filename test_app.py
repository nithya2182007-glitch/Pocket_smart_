import os
os.environ["MOCK_AI"]="true"
from fastapi.testclient import TestClient
from app.main import app
from app.services.store import init_db
import uuid
init_db()
client=TestClient(app)

def login():
    u="u"+uuid.uuid4().hex[:8]
    assert client.post("/register",json={"username":u,"password":"password123"}).status_code==200
    assert client.post("/login",json={"username":u,"password":"password123"}).status_code==200

def test_health(): assert client.get("/health").json()["status"]=="ok"
def test_home():
    login(); r=client.post("/generate-home",json={"budget":50000,"rooms":["Living Room"],"items":{"lights":4},"style":"Modern","notes":""}); assert r.status_code==200
def test_party():
    login(); r=client.post("/generate-party",json={"budget":60000,"guests":30,"event_type":"Birthday","venue":"Home","city":"","notes":""}); assert r.status_code==200
def test_travel():
    login(); r=client.post("/generate-travel",json={"budget":50000,"destination":"Chennai","days":3,"travelers":2}); assert r.status_code==200; assert r.json()["planner"]=="travel"
def test_meal():
    login(); r=client.post("/generate-meal",json={"budget":10000,"people":4,"days":7}); assert r.status_code==200; assert r.json()["planner"]=="meal"
def test_shopping():
    login(); r=client.post("/generate-shopping",json={"budget":15000,"category":"Home","items":["Desk","Chair"]}); assert r.status_code==200; assert r.json()["planner"]=="shopping"
def test_jewelry():
    login(); r=client.post("/generate-jewelry",data={"budget":"25000","occasion":"Wedding","style":"Elegant","outfit_color":"red","notes":""}); assert r.status_code==200
