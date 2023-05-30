from flask import Flask, jsonify, request
from flask_mysqldb import MySQL


app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vignesh@123'
app.config['MYSQL_DB'] = 'student_management'


mysql = MySQL(app)

# 1.API endpoint to list details of all students
@app.route('/api/students/', methods=['GET'])
def get_all_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    student_list = []
    for student in students:
        student_data = {
            'Roll Number': student[0],
            'Name': student[1],
            'Date of Birth': str(student[2])
        }
        student_list.append(student_data)
    return jsonify(student_list)

#2. API endpoint to add a new student
@app.route('/api/student/add/', methods=['POST'])
def add_student():
    student_data = request.get_json()
    roll_number = student_data['Roll Number']
    name = student_data['Name']
    dob = student_data['Date of Birth']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO students (roll_number, name, dob) VALUES (%s, %s, %s)", (roll_number, name, dob))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Student added successfully'})

# 3.API endpoint to get a single student detail by roll number
@app.route('/api/student/<pk>/', methods=['GET'])
def get_student(pk):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE roll_number = %s", [pk])
    student = cur.fetchone()
    cur.close()
    if student:
        student_data = {
            'Roll Number': student[0],
            'Name': student[1],
            'Date of Birth': str(student[2])
        }
        return jsonify(student_data)
    else:
        return jsonify({'message': 'Student not found'})

#4.API endpoint to add a mark to a single student
@app.route('/api/student/<pk>/add-mark/', methods=['POST'])
def add_mark(pk):
    mark_data = request.get_json()
    mark = mark_data['Mark']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE students SET mark = %s WHERE roll_number = %s", (mark, pk))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Mark added successfully'})

#5. API endpoint to get a single student's mark by roll number
@app.route('/api/student/<pk>/mark/', methods=['GET'])
def get_mark(pk):
    cur = mysql.connection.cursor()
    cur.execute("SELECT mark FROM students WHERE roll_number = %s", [pk])
    mark = cur.fetchone()
    cur.close()
    if mark:
        return jsonify({'Mark': mark[0]})
    else:
        return jsonify({'message': 'Mark not found'})

# 6.API endpoint to get analyzed report for students
@app.route('/api/student/results/', methods=['GET'])
def get_results():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM students WHERE mark >= 50")
    students_with_marks = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM students WHERE mark >= 91")
    s_grade = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM
        students WHERE mark >= 81 AND mark <= 90")
    a_grade = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM students WHERE mark >= 71 AND mark <= 80")
    b_grade = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM students WHERE mark >= 61 AND mark <= 70")
    c_grade = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM students WHERE mark >= 51 AND mark <= 60")
    d_grade = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM students WHERE mark >= 50 AND mark <= 55")
    e_grade = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM students WHERE mark < 50")
    f_grade = cur.fetchone()[0]

    pass_percentage = (students_with_marks - f_grade) / students_with_marks * 100

    results = {
        'S Grade': s_grade,
        'A Grade': a_grade,
        'B Grade': b_grade,
        'C Grade': c_grade,
        'D Grade': d_grade,
        'E Grade': e_grade,
        'F Grade': f_grade,
        'Pass Percentage': pass_percentage
    }

    cur.close()
    return jsonify(results)


if __name__ == '__main__':
    app.run()
