from flask import Flask, jsonify, request
import json
import uuid


def generate_id():
    return str(uuid.uuid4())


app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Flask API is up and running!"})

# salva o usuario em ARQUIVO JSON users.json


@app.route('/users/json', methods=['POST'])
def create_user_json():
    try:
        id = generate_id()
        body = request.get_json()
        name = body.get('name')

        if not name:
            return jsonify({"error": "name is required"}), 400

        with open('users.json', 'r') as f:
            data = json.load(f)

        for user in data['users']:
            if user['name'] == name:
                print("name already exists")
                return {"error": "name already exists"}, 400

        newUser = {
            "id": id,
            "name": name
        }
        data['users'].append(newUser)

        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

        return jsonify(newUser), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/json', methods=['GET'])
def get_users_json():
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/json/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)

            found = False

            for user in data['users']:
                if user['id'] == user_id:
                    body = request.get_json()
                    name = body.get('name')

                    found = True

                    if not name or name == '':
                        return jsonify({"error": "name is required"}), 400

                    user['name'] = name
                    found = True

            if not found:
                return jsonify({"error": "user not found"}), 404

            with open('users.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            return jsonify(user), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/json/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)

            found = False

            for user in data['users']:
                if user['id'] == user_id:
                    found = True
                    data['users'].remove(user)

            if not found:
                return jsonify({"error": "user not found"}), 404

            with open('users.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            return jsonify({"deleted": user['id']}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.run(host="localhost", port=3000, debug=True)
