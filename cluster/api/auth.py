from flask import current_app, redirect
from flask_user import current_user

# The view server URL to redirect at the end of auth processing.

# Set up the token and db managers.
#token_manager = TokenManager(app)
#db_manager = DBManager(app, db, User, RoleClass=Role)

def auth_routes(app):

    # Handle redirect after login including username and roles.
    @app.route('/user/after-login')
    def after_login():
        print("adftere log in called")
        viewer_url = current_app.config['VIEWER_URL'] + 'auth'
        return redirect(viewer_url, code=302)


    # Handle redirect after logout including logout indicated.
    @app.route('/user/after-logout')
    def after_logout():
        viewer_url = current_app.config['VIEWER_URL'] + 'auth'
        return redirect(viewer_url + '/?u=logout', code=302)


    # Handle redirect after attempt to reach an unauth'd endpoint.
    @app.route('/user/unauthorized')
    def unauthorized():
        viewer_url = current_app.config['VIEWER_URL'] + 'auth'
        return redirect(viewer_url, code=302)


    # Handle redirect after most of the auth pages.
    @app.route('/user/home')
    def home():
        viewer_url = current_app.config['VIEWER_URL'] + 'auth'
        return redirect(viewer_url, code=302)