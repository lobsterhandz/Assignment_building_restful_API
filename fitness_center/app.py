import logging
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import mysql.connector


# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Task 1: Setting Up the Flask Environment and Database Connection
app = Flask(__name__)
ma = Marshmallow(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="fitness_center_db"
)

# Define cursor for database operations
cursor = db.cursor(dictionary=True)

# Task 2: Implementing CRUD Operations for Members

# Route to add a member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')
    
    try:
        query = "INSERT INTO Members (name, age, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, age, email))
        db.commit()
        logger.info(f"Member added: {name}")
        return jsonify({'message': 'Member added successfully'}), 201
    except Exception as e:
        logger.error(f"Error adding member: {e}")
        return jsonify({'error': str(e)}), 400

# Route to retrieve all members
@app.route('/members', methods=['GET'])
def get_members():
    try:
        query = "SELECT * FROM Members"
        cursor.execute(query)
        members = cursor.fetchall()
        logger.info("Retrieved all members")
        return jsonify(members), 200
    except Exception as e:
        logger.error(f"Error retrieving members: {e}")
        return jsonify({'error': str(e)}), 400

# Route to retrieve a specific member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        query = "SELECT * FROM Members WHERE id = %s"
        cursor.execute(query, (id,))
        member = cursor.fetchone()
        if not member:
            logger.warning(f"Member with ID {id} not found")
            return jsonify({'message': 'Member not found'}), 404
        logger.info(f"Retrieved member with ID {id}")
        return jsonify(member), 200
    except Exception as e:
        logger.error(f"Error retrieving member with ID {id}: {e}")
        return jsonify({'error': str(e)}), 400

# Route to update a member by ID
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')
    
    try:
        query = "UPDATE Members SET name = %s, age = %s, email = %s WHERE id = %s"
        cursor.execute(query, (name, age, email, id))
        db.commit()
        logger.info(f"Member with ID {id} updated")
        return jsonify({'message': 'Member updated successfully'}), 200
    except Exception as e:
        logger.error(f"Error updating member with ID {id}: {e}")
        return jsonify({'error': str(e)}), 400

# Route to delete a member by ID
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        query = "DELETE FROM Members WHERE id = %s"
        cursor.execute(query, (id,))
        db.commit()
        logger.info(f"Member with ID {id} deleted")
        return jsonify({'message': 'Member deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error deleting member with ID {id}: {e}")
        return jsonify({'error': str(e)}), 400

# Task 3: Managing Workout Sessions

# Route to schedule a workout session
@app.route('/workouts', methods=['POST'])
def add_workout():
    data = request.get_json()
    member_id = data.get('member_id')
    session_type = data.get('session_type')
    date_time = data.get('date_time')
    
    try:
        query = "INSERT INTO WorkoutSessions (member_id, session_type, date_time) VALUES (%s, %s, %s)"
        cursor.execute(query, (member_id, session_type, date_time))
        db.commit()
        logger.info(f"Workout session scheduled for member ID {member_id}")
        return jsonify({'message': 'Workout session scheduled successfully'}), 201
    except Exception as e:
        logger.error(f"Error scheduling workout session: {e}")
        return jsonify({'error': str(e)}), 400

# Route to update a workout session by ID
@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    data = request.get_json()
    session_type = data.get('session_type')
    date_time = data.get('date_time')
    
    try:
        query = "UPDATE WorkoutSessions SET session_type = %s, date_time = %s WHERE id = %s"
        cursor.execute(query, (session_type, date_time, id))
        db.commit()
        logger.info(f"Workout session with ID {id} updated")
        return jsonify({'message': 'Workout session updated successfully'}), 200
    except Exception as e:
        logger.error(f"Error updating workout session with ID {id}: {e}")
        return jsonify({'error': str(e)}), 400

# Route to view all workout sessions
@app.route('/workouts', methods=['GET'])
def get_workouts():
    try:
        query = "SELECT * FROM WorkoutSessions"
        cursor.execute(query)
        workouts = cursor.fetchall()
        logger.info("Retrieved all workout sessions")
        return jsonify(workouts), 200
    except Exception as e:
        logger.error(f"Error retrieving workout sessions: {e}")
        return jsonify({'error': str(e)}), 400

# Route to retrieve all workout sessions for a specific member
@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_workouts_for_member(member_id):
    try:
        query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"
        cursor.execute(query, (member_id,))
        workouts = cursor.fetchall()
        logger.info(f"Retrieved workout sessions for member ID {member_id}")
        return jsonify(workouts), 200
    except Exception as e:
        logger.error(f"Error retrieving workout sessions for member ID {member_id}: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
