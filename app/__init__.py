import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
    PROMETHEUS_ENABLED = True
except ImportError:
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"
    PROMETHEUS_ENABLED = False

    class _NoopMetric:
        def labels(self, *args, **kwargs):
            return self

        def inc(self, amount=1):
            return None

        def observe(self, value):
            return None

        def set(self, value):
            return None

    def Counter(*args, **kwargs):
        return _NoopMetric()

    def Histogram(*args, **kwargs):
        return _NoopMetric()

    def Gauge(*args, **kwargs):
        return _NoopMetric()

    def generate_latest():
        return b"# Prometheus client not installed\n"

db = SQLAlchemy()
login_manager = LoginManager()
REQUEST_COUNT = Counter(
    "api_monitor_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "api_monitor_http_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)
MONITORED_APIS = Gauge(
    "api_monitor_configured_apis_total",
    "Number of APIs configured by users",
)


def create_app(test_config=None):
    """Create and initialize Flask app."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        instance_relative_config=True,
    )

    os.makedirs(app.instance_path, exist_ok=True)

    default_db_path = os.path.join(app.instance_path, "database.db")
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "your-secret-key-change-in-production"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", f"sqlite:///{default_db_path}"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        START_MONITOR=os.environ.get("START_MONITOR", "1").lower() in {"1", "true", "yes"},
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.routes import auth_bp, main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        print("Database initialized")

        if app.config.get("START_MONITOR", True) and not app.config.get("TESTING", False):
            from app.monitor import start_monitor
            start_monitor(app)

    @app.before_request
    def before_request():
        from flask import g, request
        import time
        from app.models import API

        g._request_started_at = time.perf_counter()
        MONITORED_APIS.set(API.query.count())
        REQUEST_COUNT.labels(request.method, request.endpoint or "unknown", "in_progress").inc(0)

    @app.after_request
    def after_request(response):
        from flask import g, request
        import time

        endpoint = request.endpoint or "unknown"
        started_at = getattr(g, "_request_started_at", None)
        if started_at is not None:
            REQUEST_LATENCY.labels(request.method, endpoint).observe(time.perf_counter() - started_at)
        REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
        return response

    @app.get("/metrics")
    def metrics():
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User

    return User.query.get(int(user_id))
