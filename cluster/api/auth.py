"""
auth routes pointing to the cell-atlas view server
"""
from flask import current_app, redirect, render_template
from flask_user import current_user


def auth_routes(app):
    @app.route('/user/after-login')
    def after_login():
        viewer_url = current_app.config['VIEWER_URL'] + 'auth'
        return redirect(viewer_url + \
                 '/?u=' + current_user.email + \
                 '&r=' + ','.join(map(str, current_user.roles)), \
                 code=302)

    @app.route('/user/after-logout')
    def after_logout():
        viewer_url = current_app.config['VIEWER_URL'] + 'auth'
        return redirect(viewer_url + '/?u=logout', code=302)

    @app.route('/user/unauthorized')
    def unauthorized():
        viewer_url = current_app.config['VIEWER_URL'] + 'auth'
        return redirect(viewer_url, code=302)

    @app.route('/user/home')
    def home():
        viewer_url = current_app.config['VIEWER_URL'] + 'auth'
        return redirect(viewer_url, code=302)

    @app.route('/user/after-register')
    def after_reg():
        return render_template("email_sent.html")

