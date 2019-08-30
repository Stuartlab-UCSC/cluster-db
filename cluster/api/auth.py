"""
auth routes pointing to the cell-atlas view server
"""
from flask import current_app, redirect, render_template
from flask_user import current_user

def viewer_url():
    return current_app.config['VIEWER_URL'] + 'auth'

def auth_routes(app):
    @app.route('/user/after-login')
    def after_login():
        return redirect(viewer_url() + \
                 '/?u=' + current_user.email + \
                 '&r=' + ','.join(map(str, current_user.roles)), \
                 code=302)

    @app.route('/user/after-logout')
    def after_logout():
        return redirect(viewer_url() + '/?u=logout', code=302)

    @app.route('/user/check-email')
    def check_email():
        return redirect(viewer_url() + '/?u=check-email', code=302)

    @app.route('/user/unauthorized')
    def unauthorized():
        return redirect(viewer_url(), code=302)
