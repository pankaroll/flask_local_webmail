def test_app_starts_and_returns_404_on_unknown_path(client):
    r = client.get("/__definitely_not_existing__")
    assert r.status_code == 404
