from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Créer l'application Flask
app = Flask(__name__)

# Config MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/students_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle étudiant
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Crée toutes les tables si elles n'existent pas
with app.app_context():
    db.create_all()

# Routes API
@app.route('/')
def home():
    return "Bienvenue dans l'API des étudiants"

@app.route('/students', methods=['GET'])
def get_students():
    all_students = Student.query.all()
    result = [{"id": s.id, "name": s.name, "age": s.age} for s in all_students]
    return jsonify(result)

@app.route('/addstudent', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(name=data['name'], age=data['age'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"id": new_student.id, "name": new_student.name, "age": new_student.age}), 201

@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if student:
        return jsonify({"id": student.id, "name": student.name, "age": student.age})
    return jsonify({"error": "L'étudiant n'existe pas !"}), 404

@app.route('/updatestudent/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "L'étudiant n'existe pas !"}), 404
    data = request.get_json()
    student.name = data.get('name', student.name)
    student.age = data.get('age', student.age)
    db.session.commit()
    return jsonify({"id": student.id, "name": student.name, "age": student.age})

@app.route('/deletestudent/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "L'étudiant n'existe pas !"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": f"Étudiant {id} supprimé avec succès."})

if __name__ == '__main__':
    app.run(debug=True)
