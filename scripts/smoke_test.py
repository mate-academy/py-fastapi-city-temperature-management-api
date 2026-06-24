from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
resp = client.post('/cities/', json={'name': 'London'})
print('POST /cities/ status', resp.status_code)
print(resp.json())
resp2 = client.get('/cities/')
print('GET /cities/ status', resp2.status_code)
print(resp2.json())
resp3 = client.post('/temperatures/update')
print('POST /temperatures/update status', resp3.status_code)
try:
    print(resp3.json())
except Exception:
    print('No JSON response')
resp4 = client.get('/temperatures/')
print('GET /temperatures/ status', resp4.status_code)
print(resp4.json())