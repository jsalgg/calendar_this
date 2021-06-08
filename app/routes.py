from flask import Flask, Blueprint

bp = Blueprint("main", __name__, "/")


@bp.route("/")
def main_page():
    return "Calendar Working"
