from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

response = client.get("/api/analytics/infrastructure/status")
print(json.dumps(response.json(), indent=2))
