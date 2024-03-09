from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {
        "email": "abc@abc.ca",
        "firstName": "ABC",
        "id": "5abf6783"
    },
    {
        "email": "xyz@xyz.ca",
        "firstName": "XYZ",
        "id": "5abf674563"
    }
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({
        "message": "Users retrieved",
        "success": True,
        "users": users
    })

@app.route('/add', methods=['POST'])
def add_user():
    data = request.json
    if 'email' not in data or 'firstName' not in data:
        return jsonify({"message": "Missing data in request body", "success": False}), 400
    
    new_user = {
        "email": data['email'],
        "firstName": data['firstName'],
        "id": str(len(users) + 1)
    }
    users.append(new_user)
    return jsonify({"message": "User added", "success": True}), 201

@app.route('/update/<string:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    for user in users:
        if user['id'] == id:
            user['email'] = data.get('email', user['email'])
            user['firstName'] = data.get('firstName', user['firstName'])
            return jsonify({"message": "User updated", "success": True}), 200
    
    return jsonify({"message": "User not available", "success": False}), 404

@app.route('/user/<string:id>', methods=['GET'])
def get_user(id):
    for user in users:
        if user['id'] == id:
            return jsonify({"success": True, "user": user}), 200
    
    return jsonify({"message": "User not available", "success": False}), 404

if __name__ == '__main__':
    app.run(debug=True)
