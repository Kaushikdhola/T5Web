from flask import Flask, jsonify, request
import json
app = Flask(__name__)

file_path = "users.json"

def read_users():
    
    try:
        with open(file_path, "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    return users

def write_users(users):
    with open(file_path, "w") as file:
        print(users)
        json.dump(users, file, indent=4)

@app.route('/')
def hello():
    return "hellow, please use /users, /user, /add, /update to test the application."

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = read_users()
        return jsonify({
            "message": "Users retrieved",
            "success": True,
            "users": users
        }), 200
    except Exception as e:
        return jsonify({"message": "Failed to get users", "success": False, "error": str(e)}), 500


@app.route('/add', methods=['POST'])
def add_user():
    try:
        data = request.json
        if 'email' not in data or 'firstName' not in data:
            return jsonify({"message": "Missing data in request body", "success": False}), 400
        users = read_users()
        new_user = {
            "email": data['email'],
            "firstName": data['firstName'],
            "id": str(len(users) + 1)
        }
        users.append(new_user)
        write_users(users)

        return jsonify({"message": "User added", "success": True}), 201
    except Exception as e:
        return jsonify({"message": "Failed to add user", "success": False, "error": str(e)}), 500

@app.route('/update/<string:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.json
        users=read_users()
        for user in users:
            if user['id'] == id:
                user['email'] = data.get('email', user['email'])
                user['firstName'] = data.get('firstName', user['firstName'])
                write_users(users)
                return jsonify({"message": "User updated", "success": True}), 200
        
        return jsonify({"message": "User not available", "success": False}), 404
    except Exception as e:
        return jsonify({"message": "Failed to update user", "success": False, "error": str(e)}), 500

@app.route('/user/<string:id>', methods=['GET'])
def get_user(id):
    try:
        users = read_users()
        for user in users:
            if user['id'] == id:
                return jsonify({"success": True, "user": user}), 200
        
        return jsonify({"message": "User not available", "success": False}), 404
    except Exception as e:
        return jsonify({"message": "Failed to retrieve user", "success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
