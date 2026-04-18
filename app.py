"""
ElectraVision – Flask API Server
RDS integration is currently commented out — running in memory-only mode.

To re-enable RDS, uncomment all sections marked  # [RDS]
and set these env vars:
  DB_TYPE = mysql | postgresql
  DB_HOST = <RDS endpoint>
  DB_PORT = 3306 | 5432
  DB_NAME = electravision
  DB_USER = <username>
  DB_PASS = <password>

Install dependencies (needed when RDS is re-enabled):
  pip install flask sqlalchemy pymysql psycopg2-binary python-dotenv
"""

import os
from datetime import datetime

from flask import Flask, render_template, request, jsonify

# ── [RDS] Imports ──────────────────────────────────────────────────────────
# from sqlalchemy import create_engine, Column, Integer, Float, DateTime, text
# from sqlalchemy.orm import DeclarativeBase, Session

# ── [RDS] Optional: load a .env file if present ───────────────────────────
# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     pass

# ── [RDS] Database configuration ──────────────────────────────────────────
# DB_TYPE = os.environ.get("DB_TYPE", "mysql").lower()
# DB_HOST = os.environ.get("DB_HOST", "localhost")
# DB_USER = os.environ.get("DB_USER", "root")
# DB_PASS = os.environ.get("DB_PASS", "password")
# DB_NAME = os.environ.get("DB_NAME", "electravision")
# DB_PORT = os.environ.get("DB_PORT", "3306" if DB_TYPE == "mysql" else "5432")
#
# if DB_TYPE == "postgresql":
#     DATABASE_URL = (
#         f"postgresql+psycopg2://{DB_USER}:{DB_PASS}"
#         f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     )
# else:
#     DATABASE_URL = (
#         f"mysql+pymysql://{DB_USER}:{DB_PASS}"
#         f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     )
#
# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,
#     pool_recycle=3600,
# )

# ── [RDS] ORM model ────────────────────────────────────────────────────────
# class Base(DeclarativeBase):
#     pass
#
# class Reading(Base):
#     __tablename__ = "readings"
#     id        = Column(Integer, primary_key=True, autoincrement=True)
#     timestamp = Column(DateTime, default=datetime.utcnow, index=True)
#     voltage   = Column(Float, nullable=False)
#     current   = Column(Float, nullable=False)
#     power     = Column(Float, nullable=False)
#     frequency = Column(Float, nullable=False, default=50.0)
#     pf        = Column(Float, nullable=False, default=1.0)
#     energy    = Column(Float, nullable=False, default=0.0)
#
# Base.metadata.create_all(engine)

# ── In-memory cache of the latest reading ─────────────────────────────────
latest_data: dict = {
    "voltage":   0.0,
    "current":   0.0,
    "power":     0.0,
    "frequency": 50.0,
    "pf":        1.0,
    "energy":    0.0,
}

# ── Flask app ──────────────────────────────────────────────────────────────
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data", methods=["POST"])
def receive_data():
    """Accept a JSON payload from the simulator — stored in memory only."""
    global latest_data

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400

    # Update in-memory cache
    latest_data = {
        "voltage":   float(payload.get("voltage",   0)),
        "current":   float(payload.get("current",   0)),
        "power":     float(payload.get("power",     0)),
        "frequency": float(payload.get("frequency", 50.0)),
        "pf":        float(payload.get("pf",        1.0)),
        "energy":    float(payload.get("energy",    0.0)),
    }

    # ── [RDS] Persist to database ──────────────────────────────────────────
    # try:
    #     with Session(engine) as session:
    #         row = Reading(**latest_data)
    #         session.add(row)
    #         session.commit()
    # except Exception as exc:
    #     app.logger.error(f"DB write failed: {exc}")
    #     return jsonify({"status": "received", "db": "error", "detail": str(exc)}), 500

    return jsonify({"status": "received", "db": "disabled"}), 200


@app.route("/data", methods=["GET"])
def get_data():
    """Return the latest reading from in-memory cache."""
    return jsonify(latest_data)


# ── [RDS] History endpoint ─────────────────────────────────────────────────
# @app.route("/history")
# def get_history():
#     n = min(int(request.args.get("n", 100)), 1000)
#     try:
#         with Session(engine) as session:
#             rows = (
#                 session.query(Reading)
#                 .order_by(Reading.timestamp.desc())
#                 .limit(n)
#                 .all()
#             )
#         result = [
#             {
#                 "timestamp": r.timestamp.isoformat(),
#                 "voltage":   r.voltage,
#                 "current":   r.current,
#                 "power":     r.power,
#                 "frequency": r.frequency,
#                 "pf":        r.pf,
#                 "energy":    r.energy,
#             }
#             for r in reversed(rows)
#         ]
#         return jsonify(result)
#     except Exception as exc:
#         return jsonify({"error": str(exc)}), 500


# ── [RDS] Health check endpoint ────────────────────────────────────────────
# @app.route("/health")
# def health():
#     try:
#         with engine.connect() as conn:
#             conn.execute(text("SELECT 1"))
#         return jsonify({"status": "ok", "db": "connected"})
#     except Exception as exc:
#         return jsonify({"status": "error", "db": str(exc)}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)