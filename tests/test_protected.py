from cluster.database.add_entries import add_entries
from tests.worksheet_entries import entries
from flask import url_for


def login(client):
    login_url = url_for("user.login")
    response = client.post(
        login_url,
        data={"email": "test@test.com", "password": "testT1234"},
        follow_redirects=True
    )
    assert response.status_code == 200


def logout(client):
    login_url = url_for("user.logout")
    response = client.post(
        login_url,
        data={"email": "test@test.com", "password": "testT1234"},
        follow_redirects=True
    )
    assert response.status_code == 200


def test_get_worksheet_redirect(client, session, user_worksheet_data):

    with client:
        add_entries(session, entries)
        logout(client)
        get_state_url = url_for(
            "api.user_worksheet", user="test@test.com", worksheet="test"
        )

        response = client.get(
            get_state_url
        )

        assert response.status_code == 302


def test_login_and_get_worksheet(client, session, user_worksheet_data):

    with client:
        add_entries(session, entries)
        login(client)
        get_state_url = url_for(
            "api.user_worksheet", user="test@test.com", worksheet="test"
        )

        response = client.get(
            get_state_url, follow_redirects=True
        )

        assert response.get_json()["simple"] == "json"


def test_login_and_save_worksheet(client, session, user_worksheet_data):

    with client:
        add_entries(session, entries)
        login(client)


        worksheet_url = url_for(
            "api.user_worksheet", user="test@test.com", worksheet="test"
        )

        response = client.post(
            worksheet_url, json={"more complex": "json"}
        )

        assert response.status_code == 200

        response = client.get(
            worksheet_url, follow_redirects=True
        )

        assert response.get_json()["more complex"] == "json"


def test_save_worksheet_redirect(client, session, user_worksheet_data):

    with client:
        add_entries(session, entries)
        logout(client)

        worksheet_url = url_for(
            "api.user_worksheet", user="test@test.com", worksheet="test"
        )

        response = client.post(
            worksheet_url, json={"more complex": "json"}
        )

        assert response.status_code == 302


def test_login_and_get_worksheet(client, session, user_worksheet_data):
    cluster_name="1.0"
    with client:
        add_entries(session, entries)
        login(client)
        get_worksheet_url = url_for(
            "api.user_gene_table", user="test@test.com", worksheet="test", cluster_name=cluster_name
        )

        response = client.get(
            get_worksheet_url, follow_redirects=True
        )
        json = response.get_json()

        assert json
        assert json["cluster_name"] == cluster_name
        assert isinstance(json["gene_table"],str)


def test_get_worksheet_redirect(client, session, user_worksheet_data):
    cluster_name="1.0"
    with client:
        add_entries(session, entries)
        logout(client)
        get_worksheet_url = url_for(
            "api.user_gene_table", user="test@test.com", worksheet="test", cluster_name=cluster_name
        )

        response = client.get(
            get_worksheet_url
        )

        assert response.status_code == 302


def test_login_and_get_add_gene(client, session, user_worksheet_data):
    size_by="size"
    color_by="color"
    gene="37.0"

    with client:
        add_entries(session, entries)
        login(client)
        get_add_gene_url = url_for(
            "api.user_add_gene", user="test@test.com", worksheet="test", gene_name=gene, size_by=size_by, color_by=color_by,
        )

        response = client.get(
            get_add_gene_url, follow_redirects=True
        )

        assert "text/tsv" in response.content_type


def test_get_add_gene_redirect(client, session, user_worksheet_data):
    size_by="size"
    color_by="color"
    gene="37.0"

    with client:
        add_entries(session, entries)
        logout(client)
        get_add_gene_url = url_for(
            "api.user_add_gene", user="test@test.com", worksheet="test", gene_name=gene, size_by=size_by, color_by=color_by,
        )

        response = client.get(
            get_add_gene_url
        )

        assert "text/tsv" not in response.content_type
        assert response.status_code == 302


def test_login_and_get_gene_scatter(client, session, user_worksheet_data):
    gene = "37"
    type_var= "unused"
    with client:
        add_entries(session, entries)
        login(client)
        get_add_gene_url = url_for(
            "api.user_gene_scatterplot", user="test@test.com", worksheet="test", gene=gene, type=type_var
        )

        response = client.get(
            get_add_gene_url, follow_redirects=True
        )

        import pandas as pd
        df = pd.read_pickle(user_worksheet_data["expression"])
        assert "image" in response.content_type


def test_get_gene_scatter_redirect(client, session, user_worksheet_data):
    gene = "37"
    type_var= "unused"
    with client:
        add_entries(session, entries)
        logout(client)
        get_add_gene_url = url_for(
            "api.user_gene_scatterplot", user="test@test.com", worksheet="test", gene=gene, type=type_var
        )

        response = client.get(
            get_add_gene_url
        )


        assert "image" not in response.content_type
        assert response.status_code == 302


def test_login_and_post_gene_categorical(client, session, user_worksheet_data):
    type_var="unused"
    n_clusters=10
    import random

    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(n_clusters)]
    cluster_names = [str(name) for name in range(n_clusters)]
    colormap = {
        "cluster-name": cluster_names,
        "colors": colors
    }

    with client:
        add_entries(session, entries)
        login(client)
        get_add_gene_url = url_for(
            "api.user_cluster_scatterplot", user="test@test.com", worksheet="test", type=type_var
        )

        response = client.post(
            get_add_gene_url, follow_redirects=True, json=colormap
        )

        assert "image" in response.content_type


def test_post_gene_categorical_redirect(client, session, user_worksheet_data):
    type_var="unused"
    n_clusters=10
    import random

    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(n_clusters)]
    cluster_names = [str(name) for name in range(n_clusters)]
    colormap = {
        "cluster-name": cluster_names,
        "colors": colors
    }

    with client:
        add_entries(session, entries)
        logout(client)
        get_scatter_url = url_for(
            "api.user_cluster_scatterplot", user="test@test.com", worksheet="test", type=type_var
        )

        response = client.post(
            get_scatter_url, json=colormap
        )

        assert response.status_code == 302
