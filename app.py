from flask import Flask, send_from_directory
import os


app = Flask(__name__)

@app.route("/")
def hello():
    hostname = os.uname().nodename
    node_name = os.getenv("NODE_NAME", "unknown-node")
    return f"Hello World! from {hostname} - {node_name} 2"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route('/health.html')
def health_html():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    health_path = os.path.join(base_dir, "health.html")

    if os.path.exists(health_path):
        return send_from_directory(base_dir, "health.html")
    else:
        return "File not found", 404