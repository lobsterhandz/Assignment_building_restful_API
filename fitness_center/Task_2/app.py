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
