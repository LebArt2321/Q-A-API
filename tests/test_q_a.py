def test_create_question(client):
    response = client.post("/questions/", json={"text": "Как дела?"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["text"] == "Как дела?"
    assert "id" in data
    assert "created_at" in data

def test_get_question_with_answers(client):
    question = client.post("/questions/", json={"text": "Как дела?"}).json()
    question_id = question["id"]

    client.post(f"/questions/{question_id}/answers/", json={"user_id": "u1", "text": "Хорошо"})
    client.post(f"/questions/{question_id}/answers/", json={"user_id": "u2", "text": "Отлично"})

    resp = client.get(f"/questions/{question_id}")
    data = resp.json()
    assert len(data["answers"]) == 2
    assert data["answers"][0]["text"] in ["Хорошо", "Отлично"]

def test_create_answer(client):
    create_question_response =  client.post("/questions/", json={"text": "Как дела?"})
    assert create_question_response.status_code == 200
    question_id = create_question_response.json()["id"]
    
    create_answer_response = client.post(f"/questions/{question_id}/answers/", json={"user_id": "user", "text": "Хорошо!"})
    assert create_answer_response.status_code == 200

    data = create_answer_response.json()
    assert data["text"] == "Хорошо!"
    assert "id" in data
    assert "created_at" in data

def test_delete_question(client):
    create_question_response =  client.post("/questions/", json={"text": "Как дела?"})
    assert create_question_response.status_code == 200
    question_id = create_question_response.json()["id"]

    delete_response = client.delete(f"/questions/{question_id}/")
    assert delete_response.status_code == 200

    get_response = client.get(f"/questions/")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data == []