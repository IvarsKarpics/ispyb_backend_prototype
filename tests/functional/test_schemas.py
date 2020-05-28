def test_schemas_route(test_app):
    client = test_app.test_client()
    api_root = test_app.config["API_ROOT"]

    response = client.get(
        api_root + "/auth/login", headers={"username": "user", "password": "pass"}
    )
    token = response.json["token"]
    assert token, "User not authenticated. No token returned"

    headers = {"Authorization": "Bearer " + token}
    response = client.get(api_root + "/schemas/available_names", headers=headers)
    assert response.status_code == 200, "Wrong status code"
    assert len(response.json) > 0, "No schemas returned"

    schema_name = response.json[0]
    response = client.get(api_root + "/schemas/%s" % schema_name, headers=headers)
    assert response.status_code == 200, "Wrong status code"
