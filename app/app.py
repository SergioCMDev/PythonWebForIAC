from flask import Flask, send_from_directory, jsonify
import os


app = Flask(__name__)

@app.route("/")
def hello():
    hostname = os.uname().nodename
    node_name = os.getenv("NODE_NAME", "unknown-node")
    return f"Hello World! from {hostname} - {node_name} - Test Flujos 212"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route('/health.html')
def health_html():
    return "OK", 200

    # base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # health_path = os.path.join(base_dir, "health.html")

    # if os.path.exists(health_path):
    #     return send_from_directory(base_dir, "health.html")
    # else:
    #     return "File not found", 404
    
@app.route('/version')
def version():
    return jsonify({
        'version': os.getenv('APP_VERSION', 'unknown'),
        'git_sha': os.getenv('GIT_SHA', 'unknown'),
        'build_date': os.getenv('BUILD_DATE', 'unknown')
    })

