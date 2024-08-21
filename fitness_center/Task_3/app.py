from flask import request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/fitness_center'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class WorkoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

class WorkoutSessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutSession

db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

# Initialize schemas
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# Route to add a member
@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    email = request.json['email']
    new_member = Member(name=name, email=email)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member)

# Route to get all members
@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)

# Route to get a single member
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    if member is None:
        return jsonify({"message": "Member not found"}), 404
    return member_schema.jsonify(member)

# Route to update a member
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get(id)
    if member is None:
        return jsonify({"message": "Member not found"}), 404
    member.name = request.json['name']
    member.email = request.json['email']
    db.session.commit()
    return member_schema.jsonify(member)

# Route to delete a member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if member is None:
        return jsonify({"message": "Member not found"}), 404
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted"})

if __name__ == '__main__':
    app.run(debug=True)

# Route to add a workout session
@app.route('/workouts', methods=['POST'])
def add_workout():
    member_id = request.json['member_id']
    date = request.json['date']
    duration = request.json['duration']
    new_workout = WorkoutSession(member_id=member_id, date=date, duration=duration)
    db.session.add(new_workout)
    db.session.commit()
    return workout_session_schema.jsonify(new_workout)

# Route to get all workout sessions
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = WorkoutSession.query.all()
    return workout_sessions_schema.jsonify(workouts)

# Route to get all workout sessions for a specific member
@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_member_workouts(member_id):
    workouts = WorkoutSession.query.filter_by(member_id=member_id).all()
    return workout_sessions_schema.jsonify(workouts)

# Route to update a workout session
@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    workout = WorkoutSession.query.get(id)
    if workout is None:
        return jsonify({"message": "Workout not found"}), 404
    workout.member_id = request.json['member_id']
    workout.date = request.json['date']
    workout.duration = request.json['duration']
    db.session.commit()
    return workout_session_schema.jsonify(workout)

# Route to delete a workout session
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = WorkoutSession.query.get(id)
    if workout is None:
        return jsonify({"message": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"})

if __name__ == '__main__':
    app.run(debug=True)
