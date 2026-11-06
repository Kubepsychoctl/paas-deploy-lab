"""Small REST API (standalone version of the Lab 5 API, no Postgres/Redis needed).

Deployed to Render (free web service). Endpoints:
  GET  /            app info + version
  GET  /health      health check (used by Render healthCheckPath)
  POST /users       create a user (JSON: name, email)
  GET  /users       list users
  GET  /users/<id>  one user
"""
from flask import Flask, jsonify, request

VERSION = "v3-fixed"

app = Flask(__name__)

# In-memory storage (the free Render filesystem is ephemeral anyway)
USERS = {}
NEXT_ID = 1


@app.route("/")
def home():
    return jsonify({"app": "PaaS Lab API", "status": "running", "version": VERSION})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/users", methods=["POST"])
def create_user():
    global NEXT_ID
    data = request.get_json(silent=True) or {}
    name, email = data.get("name"), data.get("email")
    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400
    if any(u["email"] == email for u in USERS.values()):
        return jsonify({"error": "email already exists"}), 409
    user = {"id": NEXT_ID, "name": name, "email": email}
    USERS[NEXT_ID] = user
    NEXT_ID += 1
    return jsonify(user), 201


@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(list(USERS.values()))


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = USERS.get(user_id)
    if user is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
