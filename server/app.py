from flask import Flash, jsonify, request

app = Flask(__name__)

# sample data
alarmSettings = {
	'time' : '07:00 AM',
	'enabled' : True
}

@app.route('/')
def home():
	return "Welcome to the Ultimate Alarm!"

@app.route('/alarm', methods=['GET', 'POST'])
def manageAlarm():
	if request.method == 'GET':
		return jsonify(alarmSettings)
	elif request.method == 'POST':
		data = request.get_json()
		alarmSettings['time'] = data.get('time', alarmSettings['time'])
		alarmSettings['enabled'] = data.get('enabled', alarmSettings['enabled'])
		return jsonify(alarmSettings), 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)