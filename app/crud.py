from .database import get_db_connection


def get_all_students():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students;")
        students = cur.fetchall()
    conn.close()
    return students


def get_student_by_id(student_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students WHERE id = %s;", (student_id,))
        student = cur.fetchone()
    conn.close()
    return student


def create_student(name, age):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO students (name, age) VALUES (%s, %s) RETURNING *;", (name, age))
        new_student = cur.fetchone()
    conn.commit()
    conn.close()
    return new_student


def update_student(student_id, name, age):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE students SET name = %s, age = %s WHERE id = %s RETURNING *;", (name, age, student_id))
        updated_student = cur.fetchone()
    conn.commit()
    conn.close()
    return updated_student


def delete_student(student_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM students WHERE id = %s RETURNING *;", (student_id,))
        deleted_student = cur.fetchone()
    conn.commit()
    conn.close()
    return deleted_student
