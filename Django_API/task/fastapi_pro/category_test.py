from main import client


# <---------- ADD TEST ---------->
def test_add_category():
    data = {
        "name" : "refrigerator"
    }
    response = client.post("/categories/add", json=data)
    assert response.status_code == 200


# <---------- Display TEST ---------->
def test_get_category(): 
    response = client.get("/categories/get")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# <---------- UPDATE TEST ---------->
def test_update_category():
    update_category = {
        "name" : "Refrigerator"
    }
    response = client.put("/categories/update/4", json=update_category)
    assert response.status_code == 200


# <---------- DELETE TEST ---------->
def test_delete_category():
    response = client.delete("/categories/delete/5")

    assert response.status_code == 200

