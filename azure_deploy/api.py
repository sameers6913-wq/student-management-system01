from flask import Flask, request, jsonify
from flask_cors import CORS

from database import create_connection


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)
CORS(app)


# =========================================================
# HOME
# =========================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Student Management System API is running!",
        "status": "success"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health", methods=["GET"])
def health():

    connection = create_connection()

    if connection:

        try:
            connection.close()
        except Exception:
            pass

        return jsonify({
            "status": "online",
            "database": "Azure MySQL",
            "database_connection": "successful"
        }), 200

    return jsonify({
        "status": "offline",
        "database": "Azure MySQL",
        "database_connection": "failed"
    }), 500


# =========================================================
# LOGIN
# =========================================================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json() or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")
    role = data.get("role", "").strip()

    if not username or not password or not role:

        return jsonify({
            "message": "Username, password and role are required."
        }), 400

    connection = create_connection()

    if not connection:

        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id,
                username,
                password,
                role,
                full_name,
                status,
                person_id
            FROM users
            WHERE username = %s
            AND role = %s
            LIMIT 1
        """, (username, role))

        user = cursor.fetchone()

        if not user:

            return jsonify({
                "message": "Invalid username, password or role."
            }), 401

        if user["password"] != password:

            return jsonify({
                "message": "Invalid username, password or role."
            }), 401

        if user.get("status") != "Active":

            return jsonify({
                "message": "This account is inactive."
            }), 403

        return jsonify({
            "message": "Login successful.",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
                "full_name": user["full_name"],
                "status": user["status"],
                "person_id": user["person_id"]
            }
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# STUDENTS
# =========================================================

@app.route("/api/students", methods=["GET"])
def get_students():

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id,
                student_id,
                full_name,
                email,
                phone,
                gender,
                dob,
                course,
                semester,
                address
            FROM students
            ORDER BY id DESC
        """)

        students = cursor.fetchall()

        return jsonify({
            "students": students
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/students/search", methods=["GET"])
def search_students():

    q = request.args.get("q", "").strip()

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor(dictionary=True)

    try:

        search = f"%{q}%"

        cursor.execute("""
            SELECT
                id,
                student_id,
                full_name,
                email,
                phone,
                gender,
                dob,
                course,
                semester,
                address
            FROM students
            WHERE student_id LIKE %s
               OR full_name LIKE %s
               OR email LIKE %s
               OR phone LIKE %s
               OR course LIKE %s
            ORDER BY id DESC
        """, (
            search,
            search,
            search,
            search,
            search
        ))

        students = cursor.fetchall()

        return jsonify({
            "students": students
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id,
                student_id,
                full_name,
                email,
                phone,
                gender,
                dob,
                course,
                semester,
                address
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        student = cursor.fetchone()

        if not student:

            return jsonify({
                "message": "Student not found."
            }), 404

        return jsonify({
            "student": student
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/students", methods=["POST"])
def add_student():

    data = request.get_json() or {}

    student_id = data.get("student_id", "").strip()
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    gender = data.get("gender", "").strip()
    dob = data.get("dob")
    course = data.get("course", "").strip()
    semester = data.get("semester")
    address = data.get("address", "").strip()

    if not student_id or not full_name:

        return jsonify({
            "message": "Student ID and full name are required."
        }), 400

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        if cursor.fetchone():

            return jsonify({
                "message": "Student ID already exists."
            }), 409

        cursor.execute("""
            INSERT INTO students
            (
                student_id,
                full_name,
                email,
                phone,
                gender,
                dob,
                course,
                semester,
                address
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            student_id,
            full_name,
            email,
            phone,
            gender,
            dob,
            course,
            semester,
            address
        ))

        connection.commit()

        return jsonify({
            "message": "Student added successfully."
        }), 201

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/students/<student_id>", methods=["PUT"])
def update_student(student_id):

    data = request.get_json() or {}

    new_student_id = data.get(
        "student_id",
        student_id
    ).strip()

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    gender = data.get("gender", "").strip()
    dob = data.get("dob")
    course = data.get("course", "").strip()
    semester = data.get("semester")
    address = data.get("address", "").strip()

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        if not cursor.fetchone():

            return jsonify({
                "message": "Student not found."
            }), 404

        if new_student_id != student_id:

            cursor.execute("""
                SELECT id
                FROM students
                WHERE student_id = %s
            """, (new_student_id,))

            if cursor.fetchone():

                return jsonify({
                    "message": "New student ID already exists."
                }), 409

        cursor.execute("""
            UPDATE students
            SET
                student_id = %s,
                full_name = %s,
                email = %s,
                phone = %s,
                gender = %s,
                dob = %s,
                course = %s,
                semester = %s,
                address = %s
            WHERE student_id = %s
        """, (
            new_student_id,
            full_name,
            email,
            phone,
            gender,
            dob,
            course,
            semester,
            address,
            student_id
        ))

        connection.commit()

        return jsonify({
            "message": "Student updated successfully."
        }), 200

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM students
            WHERE student_id = %s
        """, (student_id,))

        if cursor.rowcount == 0:

            return jsonify({
                "message": "Student not found."
            }), 404

        connection.commit()

        return jsonify({
            "message": "Student deleted successfully."
        }), 200

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# SUBJECTS
# =========================================================

@app.route("/api/subjects", methods=["GET"])
def get_subjects():

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                subject_code,
                subject_name,
                course_code,
                semester,
                credits,
                description,
                teacher_id
            FROM subjects
            ORDER BY subject_name
        """)

        subjects = cursor.fetchall()

        return jsonify({
            "subjects": subjects
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# TEACHERS
# =========================================================

@app.route("/api/teachers", methods=["GET"])
def get_teachers():

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id,
                teacher_id,
                full_name,
                email,
                phone,
                gender,
                department,
                designation,
                subject,
                qualification,
                address
            FROM teachers
            ORDER BY id DESC
        """)

        teachers = cursor.fetchall()

        return jsonify({
            "teachers": teachers
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/teachers/search", methods=["GET"])
def search_teachers():

    q = request.args.get("q", "").strip()
    search = f"%{q}%"

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id,
                teacher_id,
                full_name,
                email,
                phone,
                gender,
                department,
                designation,
                subject,
                qualification,
                address
            FROM teachers
            WHERE teacher_id LIKE %s
               OR full_name LIKE %s
               OR email LIKE %s
               OR subject LIKE %s
            ORDER BY id DESC
        """, (
            search,
            search,
            search,
            search
        ))

        teachers = cursor.fetchall()

        return jsonify({
            "teachers": teachers
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/teachers/<int:teacher_db_id>", methods=["GET"])
def get_teacher(teacher_db_id):

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id,
                teacher_id,
                full_name,
                email,
                phone,
                gender,
                department,
                designation,
                subject,
                qualification,
                address
            FROM teachers
            WHERE id = %s
        """, (teacher_db_id,))

        teacher = cursor.fetchone()

        if not teacher:

            return jsonify({
                "message": "Teacher not found."
            }), 404

        return jsonify({
            "teacher": teacher
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/teachers", methods=["POST"])
def add_teacher():

    data = request.get_json() or {}

    teacher_id = data.get("teacher_id", "").strip()
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    gender = data.get("gender", "").strip()
    department = data.get("department", "").strip()
    designation = data.get("designation", "").strip()
    subject = data.get("subject", "").strip()
    qualification = data.get("qualification", "").strip()
    address = data.get("address", "").strip()

    if not teacher_id or not full_name:

        return jsonify({
            "message": "Teacher ID and full name are required."
        }), 400

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM teachers
            WHERE teacher_id = %s
        """, (teacher_id,))

        if cursor.fetchone():

            return jsonify({
                "message": "Teacher ID already exists."
            }), 409

        cursor.execute("""
            INSERT INTO teachers
            (
                teacher_id,
                full_name,
                email,
                phone,
                gender,
                department,
                designation,
                subject,
                qualification,
                address
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            teacher_id,
            full_name,
            email,
            phone,
            gender,
            department,
            designation,
            subject,
            qualification,
            address
        ))

        # Assign subject to teacher
        if subject:

            cursor.execute("""
                UPDATE subjects
                SET teacher_id = %s
                WHERE subject_code = %s
            """, (
                teacher_id,
                subject
            ))

        connection.commit()

        return jsonify({
            "message": "Teacher added successfully."
        }), 201

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/teachers/<int:teacher_db_id>", methods=["PUT"])
def update_teacher(teacher_db_id):

    data = request.get_json() or {}

    teacher_id = data.get("teacher_id", "").strip()
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    gender = data.get("gender", "").strip()
    department = data.get("department", "").strip()
    designation = data.get("designation", "").strip()
    subject = data.get("subject", "").strip()
    qualification = data.get("qualification", "").strip()
    address = data.get("address", "").strip()

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT teacher_id
            FROM teachers
            WHERE id = %s
        """, (teacher_db_id,))

        old_teacher = cursor.fetchone()

        if not old_teacher:

            return jsonify({
                "message": "Teacher not found."
            }), 404

        old_teacher_id = old_teacher[0]

        cursor.execute("""
            SELECT id
            FROM teachers
            WHERE teacher_id = %s
            AND id != %s
        """, (
            teacher_id,
            teacher_db_id
        ))

        if cursor.fetchone():

            return jsonify({
                "message": "Teacher ID already exists."
            }), 409

        cursor.execute("""
            UPDATE teachers
            SET
                teacher_id = %s,
                full_name = %s,
                email = %s,
                phone = %s,
                gender = %s,
                department = %s,
                designation = %s,
                subject = %s,
                qualification = %s,
                address = %s
            WHERE id = %s
        """, (
            teacher_id,
            full_name,
            email,
            phone,
            gender,
            department,
            designation,
            subject,
            qualification,
            address,
            teacher_db_id
        ))

        # Remove old subject assignment
        cursor.execute("""
            UPDATE subjects
            SET teacher_id = NULL
            WHERE teacher_id = %s
        """, (old_teacher_id,))

        # Assign new subject
        if subject:

            cursor.execute("""
                UPDATE subjects
                SET teacher_id = %s
                WHERE subject_code = %s
            """, (
                teacher_id,
                subject
            ))

        connection.commit()

        return jsonify({
            "message": "Teacher updated successfully."
        }), 200

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/teachers/<int:teacher_db_id>", methods=["DELETE"])
def delete_teacher(teacher_db_id):

    connection = create_connection()

    if not connection:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT teacher_id
            FROM teachers
            WHERE id = %s
        """, (teacher_db_id,))

        teacher = cursor.fetchone()

        if not teacher:

            return jsonify({
                "message": "Teacher not found."
            }), 404

        teacher_id = teacher[0]

        cursor.execute("""
            UPDATE subjects
            SET teacher_id = NULL
            WHERE teacher_id = %s
        """, (teacher_id,))

        cursor.execute("""
            DELETE FROM teachers
            WHERE id = %s
        """, (teacher_db_id,))

        connection.commit()

        return jsonify({
            "message": "Teacher deleted successfully."
        }), 200

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# COURSES
# =========================================================

@app.route("/api/courses", methods=["GET"])
def get_courses():

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                course_code,
                course_name,
                duration,
                description
            FROM courses
            ORDER BY course_name
        """)

        courses = cursor.fetchall()

        return jsonify({
            "courses": courses
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/courses/search", methods=["GET"])
def search_courses():

    q = request.args.get(
        "q",
        ""
    ).strip()

    search = f"%{q}%"

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                course_code,
                course_name,
                duration,
                description
            FROM courses
            WHERE course_code LIKE %s
               OR course_name LIKE %s
               OR duration LIKE %s
               OR description LIKE %s
            ORDER BY course_name
        """, (
            search,
            search,
            search,
            search
        ))

        courses = cursor.fetchall()

        return jsonify({
            "courses": courses
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/courses/<course_code>", methods=["GET"])
def get_course(course_code):

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                course_code,
                course_name,
                duration,
                description
            FROM courses
            WHERE course_code = %s
        """, (course_code,))

        course = cursor.fetchone()

        if not course:

            return jsonify({
                "message": "Course not found."
            }), 404

        return jsonify({
            "course": course
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/courses", methods=["POST"])
def add_course():

    data = request.get_json() or {}

    course_code = data.get(
        "course_code",
        ""
    ).strip()

    course_name = data.get(
        "course_name",
        ""
    ).strip()

    duration = data.get(
        "duration",
        ""
    ).strip()

    description = data.get(
        "description",
        ""
    ).strip()

    if not course_code or not course_name:

        return jsonify({
            "message": "Course code and course name are required."
        }), 400

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT course_code
            FROM courses
            WHERE course_code = %s
        """, (course_code,))

        if cursor.fetchone():

            return jsonify({
                "message": "Course code already exists."
            }), 409

        cursor.execute("""
            INSERT INTO courses
            (
                course_code,
                course_name,
                duration,
                description
            )
            VALUES
            (%s,%s,%s,%s)
        """, (
            course_code,
            course_name,
            duration,
            description
        ))

        connection.commit()

        return jsonify({
            "message": "Course added successfully."
        }), 201

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/courses/<course_code>", methods=["PUT"])
def update_course(course_code):

    data = request.get_json() or {}

    new_course_code = data.get(
        "course_code",
        course_code
    ).strip()

    course_name = data.get(
        "course_name",
        ""
    ).strip()

    duration = data.get(
        "duration",
        ""
    ).strip()

    description = data.get(
        "description",
        ""
    ).strip()

    if not new_course_code or not course_name:

        return jsonify({
            "message": "Course code and course name are required."
        }), 400

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT course_code
            FROM courses
            WHERE course_code = %s
        """, (course_code,))

        if not cursor.fetchone():

            return jsonify({
                "message": "Course not found."
            }), 404

        if new_course_code != course_code:

            cursor.execute("""
                SELECT course_code
                FROM courses
                WHERE course_code = %s
            """, (new_course_code,))

            if cursor.fetchone():

                return jsonify({
                    "message": "New course code already exists."
                }), 409

        cursor.execute("""
            UPDATE courses
            SET
                course_code = %s,
                course_name = %s,
                duration = %s,
                description = %s
            WHERE course_code = %s
        """, (
            new_course_code,
            course_name,
            duration,
            description,
            course_code
        ))

        # Keep related records synchronized
        if new_course_code != course_code:

            cursor.execute("""
                UPDATE students
                SET course = %s
                WHERE course = %s
            """, (
                new_course_code,
                course_code
            ))

            cursor.execute("""
                UPDATE enrollments
                SET course_code = %s
                WHERE course_code = %s
            """, (
                new_course_code,
                course_code
            ))

            cursor.execute("""
                UPDATE subjects
                SET course_code = %s
                WHERE course_code = %s
            """, (
                new_course_code,
                course_code
            ))

            cursor.execute("""
                UPDATE timetable
                SET course_code = %s
                WHERE course_code = %s
            """, (
                new_course_code,
                course_code
            ))

        connection.commit()

        return jsonify({
            "message": "Course updated successfully."
        }), 200

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/courses/<course_code>", methods=["DELETE"])
def delete_course(course_code):

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT course_code
            FROM courses
            WHERE course_code = %s
        """, (course_code,))

        if not cursor.fetchone():

            return jsonify({
                "message": "Course not found."
            }), 404

        # Check related records
        cursor.execute("""
            SELECT COUNT(*)
            FROM enrollments
            WHERE course_code = %s
        """, (course_code,))

        enrollment_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM subjects
            WHERE course_code = %s
        """, (course_code,))

        subject_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM timetable
            WHERE course_code = %s
        """, (course_code,))

        timetable_count = cursor.fetchone()[0]

        if (
            enrollment_count > 0
            or subject_count > 0
            or timetable_count > 0
        ):

            return jsonify({
                "message":
                    "This course cannot be deleted because it is "
                    "being used by enrollments, subjects or timetable."
            }), 409

        cursor.execute("""
            DELETE FROM courses
            WHERE course_code = %s
        """, (course_code,))

        connection.commit()

        return jsonify({
            "message": "Course deleted successfully."
        }), 200

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# ENROLLMENTS
# =========================================================

@app.route("/api/enrollments", methods=["GET"])
def get_enrollments():

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                e.id,
                e.student_id,
                s.full_name AS student_name,
                e.course_code,
                c.course_name,
                e.enrollment_date,
                e.semester,
                e.status
            FROM enrollments e
            LEFT JOIN students s
                ON e.student_id = s.student_id
            LEFT JOIN courses c
                ON e.course_code = c.course_code
            ORDER BY e.id DESC
        """)

        enrollments = cursor.fetchall()

        return jsonify({
            "enrollments": enrollments
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# ATTENDANCE
# =========================================================

@app.route("/api/attendance", methods=["GET"])
def get_attendance():

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                a.id,
                a.student_id,
                s.full_name AS student_name,
                a.subject_code,
                a.attendance_date,
                a.status
            FROM attendance a
            LEFT JOIN students s
                ON a.student_id = s.student_id
            ORDER BY
                a.attendance_date DESC,
                a.id DESC
        """)

        attendance = cursor.fetchall()

        return jsonify({
            "attendance": attendance
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/attendance/search", methods=["GET"])
def search_attendance():

    q = request.args.get(
        "q",
        ""
    ).strip()

    search = f"%{q}%"

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                a.id,
                a.student_id,
                s.full_name AS student_name,
                a.subject_code,
                a.attendance_date,
                a.status
            FROM attendance a
            LEFT JOIN students s
                ON a.student_id = s.student_id
            WHERE a.student_id LIKE %s
               OR s.full_name LIKE %s
               OR a.subject_code LIKE %s
               OR a.status LIKE %s
            ORDER BY
                a.attendance_date DESC,
                a.id DESC
        """, (
            search,
            search,
            search,
            search
        ))

        attendance = cursor.fetchall()

        return jsonify({
            "attendance": attendance
        }), 200

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/attendance", methods=["POST"])
def add_attendance():

    data = request.get_json() or {}

    student_id = data.get(
        "student_id",
        ""
    ).strip()

    subject_code = data.get(
        "subject_code",
        ""
    ).strip()

    attendance_date = data.get(
        "attendance_date"
    )

    status = data.get(
        "status",
        ""
    ).strip()

    if (
        not student_id
        or not subject_code
        or not attendance_date
        or not status
    ):

        return jsonify({
            "message": "All attendance fields are required."
        }), 400

    if status not in (
        "Present",
        "Absent"
    ):

        return jsonify({
            "message": "Status must be Present or Absent."
        }), 400

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        # Student exists?
        cursor.execute("""
            SELECT student_id
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        if not cursor.fetchone():

            return jsonify({
                "message": "Student does not exist."
            }), 404

        # Subject exists?
        cursor.execute("""
            SELECT subject_code
            FROM subjects
            WHERE subject_code = %s
        """, (subject_code,))

        if not cursor.fetchone():

            return jsonify({
                "message": "Subject does not exist."
            }), 404

        # Duplicate check
        cursor.execute("""
            SELECT id
            FROM attendance
            WHERE student_id = %s
              AND subject_code = %s
              AND attendance_date = %s
        """, (
            student_id,
            subject_code,
            attendance_date
        ))

        if cursor.fetchone():

            return jsonify({
                "message":
                    "Attendance already exists for this "
                    "student, subject and date."
            }), 409

        cursor.execute("""
            INSERT INTO attendance
            (
                student_id,
                subject_code,
                attendance_date,
                status
            )
            VALUES
            (%s,%s,%s,%s)
        """, (
            student_id,
            subject_code,
            attendance_date,
            status
        ))

        connection.commit()

        return jsonify({
            "message": "Attendance added successfully."
        }), 201

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/attendance/<int:attendance_id>", methods=["PUT"])
def update_attendance(attendance_id):

    data = request.get_json() or {}

    student_id = data.get(
        "student_id",
        ""
    ).strip()

    subject_code = data.get(
        "subject_code",
        ""
    ).strip()

    attendance_date = data.get(
        "attendance_date"
    )

    status = data.get(
        "status",
        ""
    ).strip()

    if (
        not student_id
        or not subject_code
        or not attendance_date
        or not status
    ):

        return jsonify({
            "message": "All attendance fields are required."
        }), 400

    if status not in (
        "Present",
        "Absent"
    ):

        return jsonify({
            "message": "Status must be Present or Absent."
        }), 400

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM attendance
            WHERE id = %s
        """, (attendance_id,))

        if not cursor.fetchone():

            return jsonify({
                "message": "Attendance record not found."
            }), 404

        cursor.execute("""
            SELECT id
            FROM attendance
            WHERE student_id = %s
              AND subject_code = %s
              AND attendance_date = %s
              AND id != %s
        """, (
            student_id,
            subject_code,
            attendance_date,
            attendance_id
        ))

        if cursor.fetchone():

            return jsonify({
                "message":
                    "Another attendance record already exists "
                    "for this student, subject and date."
            }), 409

        cursor.execute("""
            UPDATE attendance
            SET
                student_id = %s,
                subject_code = %s,
                attendance_date = %s,
                status = %s
            WHERE id = %s
        """, (
            student_id,
            subject_code,
            attendance_date,
            status,
            attendance_id
        ))

        connection.commit()

        return jsonify({
            "message": "Attendance updated successfully."
        }), 200

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/attendance/<int:attendance_id>", methods=["DELETE"])
def delete_attendance(attendance_id):

    connection = create_connection()

    if not connection:
        return jsonify({
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM attendance
            WHERE id = %s
        """, (attendance_id,))

        if cursor.rowcount == 0:

            return jsonify({
                "message": "Attendance record not found."
            }), 404

        connection.commit()

        return jsonify({
            "message": "Attendance deleted successfully."
        }), 200

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


# =========================================================
# RUN LOCALLY
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )