import os
from tests.add_data import add_entries
from tests.worksheet_entries import entries
from cluster.database.user_models import User, CellTypeWorksheet, WorksheetUser
from flask import url_for


def test_something(user_worksheet_data, session):
    add_entries(session, entries)
    user_id = User.get_by_email("test@test.com").id
    print(user_id)
    u = list(WorksheetUser.get_user_worksheets(user_id))
    #u = list(WorksheetUser.get_user_worksheets(user_id).filter(CellTypeWorksheet.name == "test"))
    print(u)
    assert os.path.isfile(user_worksheet_data["expression"])


def login(client):
    login_url = url_for("user.login")
    response = client.post(
        login_url,
        data={"email": "test@test.com", "password": "testT1234"},
        follow_redirects=True
    )
    #print(response.data)
    assert response.status_code == 200

def test_login_and_get(app, client, session):
    from flask_user.token_manager import TokenManager
    hds = [('Authentication', TokenManager(app).generate_token())]
    with app.app_context():
        with client:
            add_entries(session, entries)
            login_url = url_for("user.login")

            response = client.post(
                login_url,
                data={"email": "test@test.com", "password": "testT1234"},
                follow_redirects=True
            )

            get_state_url = url_for(
                "api.user_worksheet", user="test@test.com", worksheet="test"
            )

            response = client.get(
                get_state_url, follow_redirects=True, headers=hds
            )

            assert response.get_json()["simple"] == "json"

"""
def test_json_after_login_for_user(app, client, url_gens):
    api_name, kwargs = url_gens
    with app.app_context():
        login_url = url_for("user.login")

        with client:
            response = client.post(
                login_url,
                data={"email": "test@test.com", "password": "testT1234"},
                follow_redirects=True
            )

            assert response.status_code == 200

            match = url_for(
                    api_name,
                    **kwargs
            )

            response = client.get(
                match, follow_redirects=False
            )

            assert response.get_json() is not None
"""