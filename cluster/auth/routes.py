# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

# flask-user templates & config
# https://flask-user.readthedocs.io/en/latest/unused.html#customizingformtemplates
# https://flask-user.readthedocs.io/en/latest/configuring_settings.html
from flask import current_app, render_template, redirect
from flask_user import current_user, login_required, roles_required, \
    TokenManager
from cluster.auth.accounts import default_accounts


def auth_routes(app, db):

    default_accounts(app, db)

    viewer_url = current_app.config['VIEWER_URL']

    # Set up the token manager
    token_manager = TokenManager(app)

    # The Home page is accessible to anyone
    @app.route('/login')
    def home_page():
        return render_template('auth/auth.html')

    # The Members page is only accessible to authenticated users
    @app.route('/members')
    @login_required    # Use of @login_required decorator
    def member_page():
        return render_template('auth/members.html')

    # The Admin page requires an 'Admin' role.
    @app.route('/admin')
    @roles_required('Admin')    # Use of @roles_required decorator
    def admin_page():
        return render_template('auth/admin.html')

    # Handle redirect after login to the cellAtlas home page.
    @app.route('/cell-help')
    def cell_help():
        return redirect(viewer_url + 'help', code=302)

    # Handle redirect after login to the cellAtlas home page.
    @app.route('/after-login')
    def after_login():
        return redirect(viewer_url + \
            '?t=' + token_manager.generate_token(current_user.id) + \
            '&u=' + current_user.email, code=302)

    # Handle redirect after logout to the cellAtlas home page.
    @app.route('/after-logout')
    def after_logout():
        return redirect(viewer_url + \
            '?t=logout', code=302)
