from flask import Flask, render_template
from smarthome.smarthome import sh
from hub.hub import hub


# Die App wird erstellt, gesichert und komprimiert.
app = Flask(__name__)
app.register_blueprint(sh, url_prefix='/smarthome')
app.register_blueprint(hub, url_prefix='/')
app.secret_key = "lhsgff90873wkljdfg3754jkgasdf53"


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
def page_not_found(e):
    return render_template('405.html'), 405


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# Die App wird gestartet.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5010", debug=True)
