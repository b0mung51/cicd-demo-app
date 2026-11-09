"""Demo Flask app for CMPE 195B CI/CD activity."""

import os

from flask import Flask, jsonify

from src.calculator import add, divide, multiply, subtract

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>CMPE 195 Demo App</h1><p>CI/CD Activity</p>"


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/calculate/<op>/<float:a>/<float:b>")
def calculate(op, a, b):
    ops = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }
    if op not in ops:
        return jsonify({"error": f"Unknown operation '{op}'"}), 400
    try:
        result = ops[op](a, b)
        return jsonify({"op": op, "a": a, "b": b, "result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
