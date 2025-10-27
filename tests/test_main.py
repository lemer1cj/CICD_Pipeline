from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

 def test_read_root():
     response = client.get("/")
     assert response.status_code == 200
     assert "message" in response.json()

 def test_health_check():
     response = client.get("/health")
     assert response.status_code == 200
     assert response.json()["status"] == "healthy"

 def test_create_product():
     response = client.post(
         "/products",
         json={"name": "Test Product", "price": 99.99}
     )
     assert response.status_code == 201
     data = response.json()
     assert data["name"] == "Test Product"
     assert data["price"] == 99.99
     assert "id" in data

 def test_get_products():
     # Create a product first
     client.post(
         "/products",
         json={"name": "Product 1", "price": 50.0}
     )
     
     response = client.get("/products")
     assert response.status_code == 200
     assert isinstance(response.json(), list)

 def test_get_product():
     # Create a product
     create_response = client.post(
         "/products",
         json={"name": "Product 2", "price": 75.0}
     )
     product_id = create_response.json()["id"]
     
     # Get the product
     response = client.get(f"/products/{product_id}")
     assert response.status_code == 200
     assert response.json()["name"] == "Product 2"

 def test_get_nonexistent_product():
     response = client.get("/products/9999")
     assert response.status_code == 404

 def test_update_product():
     # Create a product
     create_response = client.post(
         "/products",
         json={"name": "Old Name", "price": 100.0}
     )
     product_id = create_response.json()["id"]
     
     # Update the product
     response = client.put(
         f"/products/{product_id}",
         json={"name": "New Name", "price": 150.0}
     )
     assert response.status_code == 200
     assert response.json()["name"] == "New Name"
     assert response.json()["price"] == 150.0

 def test_delete_product():
     # Create a product
     create_response = client.post(
         "/products",
         json={"name": "To Delete", "price": 25.0}
     )
     product_id = create_response.json()["id"]
     
     # Delete the product
     response = client.delete(f"/products/{product_id}")
     assert response.status_code == 200
     
     # Verify it's deleted
     get_response = client.get(f"/products/{product_id}")
     assert get_response.status_code == 404