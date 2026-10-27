from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.database import create_connection


app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    connection = create_connection()

    if connection:
        connection.close()

        return jsonify({
            "status": "success",
            "message": "Flask API and LOCAL MySQL are connected"
        }), 200

    return jsonify({
        "status": "error",
        "message": "LOCAL MySQL connection failed"
    }), 500


@app.route("/api/login", methods=["POST"])
def login():

    connection = None
    cursor = None

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No login data received"
            }), 400

        username = data.get("username")
        password = data.get("password")
        role = data.get("role")

        if not username or not password:
            return jsonify({
                "success": False,
                "message": "Username and password are required"
            }), 400

        connection = create_connection()

        if connection is None:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            }), 500

        cursor = connection.cursor(dictionary=True)

        if role:
            query = """
                SELECT *
                FROM users
                WHERE username = %s
                AND password = %s
                AND role = %s
                LIMIT 1
            """

            cursor.execute(
                query,
                (username, password, role)
            )

        else:
            query = """
                SELECT *
                FROM users
                WHERE username = %s
                AND password = %s
                LIMIT 1
            """

            cursor.execute(
                query,
                (username, password)
            )

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid username, password, or role"
            }), 401

        if "status" in user:

            status = str(user["status"]).lower()

            if status not in ["active", "1", "enabled"]:
                return jsonify({
                    "success": False,
                    "message": "Your account is not active"
                }), 403

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": user
        }), 200

    except Exception as e:

        print("Login error:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":

    print("----------------------------------------")
    print("Student Management System API")
    print("Using LOCAL MySQL")
    print("Database: student_management1")
    print("Host: 127.0.0.1")
    print("Port: 3306")
    print("----------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )