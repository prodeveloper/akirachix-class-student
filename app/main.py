#!/usr/bin/env python
from flask import (Flask, render_template, request, jsonify)
import bootstrap
from models.classes import Classes
from models.student import Student
from models.student_class import Studentclass
app_start_config = {'debug': True, 'port': 8080, 'host': '0.0.0.0'}
app = Flask(__name__)


bootstrap.initialize()


@app.route('/')
def index():
    return "Success"

@app.route('/course/registration')
def course_registration():
    all_classes = Classes.select()
    all_students = Student.select()
    return render_template('course_registration.html',all_classes=all_classes,all_students=all_students)


@app.route('/course/registration/save', methods=['POST'])
def course_registration_save():
    data = dict(request.form.items())
    Studentclass.create(
        student_id=data.get('student_id'),
        classes_id=data.get('classes_id')
    )

    return jsonify(data)

@app.route('/classes/registered/<classes>')
def students_registered_class(classes):
    active_class = Classes.select().where(Classes.title ** classes).get()
    student_ids = Studentclass.select().where(Studentclass.classes_id==active_class.id)
    results = []
    for student_id in student_ids:
        student = Student.select().where(Student.id==student_id).get()
        results.append(
            {
                'name': student.name,
                'email': student.email
            }
        )
    return jsonify(results)


@app.route('/students/registered/<email>')
def classes_student_registered(email):
    student_id = Student.select().where(Student.email**email).get().id
    student_classes = Studentclass.select().where(Studentclass.student_id == student_id)
    results = []
    for student_class in student_classes:
        cls_result = Classes.select().where(Classes.id == student_class.classes_id).get()
        results.append(
            {
                'title': cls_result.title,
                'description': cls_result.description
            }
        )
    return jsonify(results)


if __name__ == '__main__':
    app.run(**app_start_config)
