from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import redis
import os
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# REDIS configuration
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    decode_responses=True,
)


@app.route('/')
def home():
    """
    Home endpoint that returns a welcome message.
    """
    return jsonify({"message": "Welcome to the Flask API",
                    "status": "success"}), 200


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    """
    Healthcheck endpoint to verify the service is running.
    """
    status = {
        "status": "healthy",
        "services": {
            "database": {
                "status": "connected",
                "error": None
            },
            "redis": {
                "status": "connected",
                "error": None
            }
        }
    }

    # Test PostgreSQL connection
    try:
        db.engine.connect()
    except Exception as e:
        status["status"] = "degraded"
        status["services"]["database"]["status"] = "disconnected"
        status["services"]["database"]["error"] = str(e)

    # Test Redis connection
    try:
        redis_client.ping()
    except Exception as e:
        status["status"] = "degraded"
        status["services"]["redis"]["status"] = "disconnected"
        status["services"]["redis"]["error"] = str(e)

    # If both services are down, consider the service unhealthy
    if (status["services"]["database"]["status"] == "disconnected" and
            status["services"]["redis"]["status"] == "disconnected"):
        status["status"] = "unhealthy"

    http_status = 200 if status["status"] in ["healthy", "degraded"] else 500

    return jsonify(status), http_status


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
