import socket
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency", ["endpoint"]
)

@app.before_request
def start_timer():
    from flask import g
    g.start_time = time.time()

@app.after_request
def record_metrics(response):
    from flask import g, request
    latency = time.time() - g.start_time
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    REQUEST_COUNT.labels(
        method=request.method, endpoint=request.path, status=response.status_code
    ).inc()
    return response

@app.route("/")
def index():
    return jsonify({
        "message": "Hello from my DevOps platform",
        "version": os.environ.get("APP_VERSION", "1.0.0"), 
        "hostname": socket.gethostname(),
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
