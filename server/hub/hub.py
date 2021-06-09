from flask import Blueprint, render_template

hub = Blueprint('hub', __name__, template_folder='templates', static_folder='static')
hub.secret_key = "lhsgff90873wkljdfg3754jkgasdf53"


@hub.route("/")
def hub_index():
    return render_template("hub_index.html")


@hub.route("/roadmap")
def hub_roadmap():
    return render_template("roadmap.html")
