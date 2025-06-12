from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from datetime import timedelta
import re
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
bcrypt = Bcrypt(app)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Svss@1234'
app.config['MYSQL_DB'] = 'test_api_db'

# JWT Config
app.config['JWT_SECRET_KEY'] = '1a9f2a77bde54e34b1asd87asdas876f58f4c4c99aa8e327eaf7587f6'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

mysql = MySQL(app)
jwt = JWTManager(app)

def user_exists(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE id = %s", (int(user_id),))
    user = cur.fetchone()
    cur.close()
    return user is not None

# ----------- Register -----------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    name = data.get('name')

    if not username or not password or len(password) < 8:
        return jsonify({'error': 'Username and password required (min 8 chars)'}), 400

    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify({'error': 'Invalid email'}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (username, password, name, email) VALUES (%s, %s, %s, %s)",
                    (username, hashed_pw, name, email))
        mysql.connection.commit()
        user_id = cur.lastrowid
    except:
        return jsonify({'error': 'Username already exists'}), 409
    finally:
        cur.close()

    return jsonify({'message': 'User registered successfully', 'user_id': user_id})

# ----------- Login -----------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password FROM users WHERE username=%s", (username,))
    result = cur.fetchone()
    cur.close()

    if not result:
        return jsonify({'error': 'Invalid username or password'}), 401

    user_id, hashed_pw = result

    if bcrypt.check_password_hash(hashed_pw, password):
        token = create_access_token(identity=str(user_id))
        return jsonify({'message': 'Login successful', 'token': token, 'user_id': user_id})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# ----------- Get all users -----------
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    if not user_exists(user_id):
        return jsonify({'error': 'User no longer exists'}), 403
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, name, email, created_at FROM users")
    data = cur.fetchall()
    cur.close()
    users = [
        {'id': row[0], 'username': row[1], 'name': row[2], 'email': row[3], 'created_at': row[4].isoformat()}
        for row in data
    ]
    return jsonify(users)

# ----------- Update user -----------
@app.route('/users/<int:id>', methods=['PUT', 'OPTIONS'])
def update_user(id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight OK'}), 200

    try:
        verify_jwt_in_request()
    except Exception as e:
        return jsonify({'error': str(e)}), 401

    current_user = get_jwt_identity()
    if current_user != str(id):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()

    if not user:
        cur.close()
        return jsonify({'message': 'User not found'}), 404

    fields = []
    values = []

    allowed_fields = ['username', 'password', 'name', 'email']
    for field in allowed_fields:
        if field in data:
            value = data[field]
            if field == 'password':
                value = bcrypt.generate_password_hash(value).decode('utf-8')
            fields.append(f"{field}=%s")
            values.append(value)

    if not fields:
        cur.close()
        return jsonify({'message': 'No valid fields to update'}), 400

    values.append(id)
    sql = f"UPDATE users SET {', '.join(fields)} WHERE id=%s"
    cur.execute(sql, values)
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User updated successfully'})

# ----------- Delete user -----------
@app.route('/users/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete_user(id):
    # Handle preflight request
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight OK'}), 200

    # Manually verify JWT before using get_jwt_identity
    try:
        verify_jwt_in_request()
    except Exception as e:
        return jsonify({'error': str(e)}), 401

    current_user = get_jwt_identity()
    if current_user != str(id):
        return jsonify({'error': 'Unauthorized'}), 403

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User deleted'})

# ----------- Main -----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
