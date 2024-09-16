from flask import Flask, request, jsonify
from database_manager import Session, User

app = Flask(__name__)
session = Session()

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        company=data['company'],
        manager_id=data['manager_id']
    )
    session.add(new_user)
    session.commit()
    return jsonify({"message": "User registered successfully", "user_id": new_user.id})

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/access_event', methods=['POST'])

def access_event():
    data = request.json
    event = AccessEvent(
        person_id=data['idPersoana'],
        gate_id=data['idPoarta'],
        direction=data['sens'],
        timestamp=datetime.fromisoformat(data['data'])
    )
    session.add(event)
    session.commit()
    return jsonify({"message": "Access event recorded successfully"})