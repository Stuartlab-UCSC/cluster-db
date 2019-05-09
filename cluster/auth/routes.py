# The auth routes.

# flask-user templates & config
# https://flask-user.readthedocs.io/en/latest/unused.html#customizingformtemplates
# https://flask-user.readthedocs.io/en/latest/configuring_settings.html

import json
from flask import current_app, redirect
from flask_user import current_user, TokenManager
from flask_user.db_manager import DBManager
from cluster.auth.db_models import User, Role

def auth_routes(app, db):

    # The view server URL to redirect at the end of auth processing.
    viewer_url = current_app.config['VIEWER_URL'] + 'auth'

    # Set up the token and db managers.
    token_manager = TokenManager(app)
    db_manager = DBManager(app, db, User, RoleClass=Role)

    # Handle redirect after login including username and roles.
    @app.route('/user/after-login')
    def after_login():
        return redirect(viewer_url + \
            '/?u=' + current_user.email + \
            '&r=' + ','.join(map(str, current_user.roles)), \
            code=302)

    # Handle redirect after logout including logout indicated.
    @app.route('/user/after-logout')
    def after_logout():
        return redirect(viewer_url + '/?u=logout', code=302)
    
    # Handle redirect after attempt to reach an unauth'd endpoint.
    @app.route('/user/unauthorized')
    def unauthorized():
        return redirect(viewer_url, code=302)
    
    # Handle redirect after most of the auth pages.
    @app.route('/user/home')
    def home():
        return redirect(viewer_url, code=302)
