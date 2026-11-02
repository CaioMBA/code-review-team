from flask import Flask, request
from flask_easy_ratelimit import limit

from reset import create_reset_token, use_reset_token

app = Flask(__name__)


@app.post("/password-reset")
@limit("5/minute")
def request_reset():
    token = create_reset_token(request.json["email"])
    return {"ok": True, "token": token}


@app.post("/password-reset/confirm")
def confirm_reset():
    ok = use_reset_token(request.json["token"], request.json["password"])
    return {"ok": ok}
