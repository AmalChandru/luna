from flask import render_template

def page_not_found(e):
    return render_template('errors/404.html'), 404

def internal_server_error(e):
    return render_template('errors/500.html'), 500


def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_404(e):
        return page_not_found(e)

    @app.errorhandler(500)
    def handle_500(e):
        return internal_server_error(e)
