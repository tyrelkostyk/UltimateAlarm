from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# sample data
alarmSettings = {
	'time' : '07:00 AM',
	'enabled' : True
}

def currentAlarms():
	return "Alarm Time: {time} - {status}".format(
	time=alarmSettings['time'],
	status='Enabled' if alarmSettings['enabled'] else 'Disabled'
	)

def homepage():
    return '''
    <h1>Welcome to the Ultimate Alarm!</h1>
	<h2>{alarms}</h2>
    <form method="post" action="/">
        <label for="time">Alarm Time:</label>
        <input type="text" id="time" name="time" value="{time}"><br>
        <label for="enabled">Enabled:</label>
        <input type="checkbox" id="enabled" name="enabled" {checked}><br>
        <input type="submit" value="Update Alarm">
    </form>
    '''.format(
	alarms=currentAlarms(),
	time=alarmSettings['time'],
	checked='checked' if alarmSettings['enabled'] else ''
	)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Update alarm settings based on the form data
        alarmSettings['time'] = request.form['time']
        alarmSettings['enabled'] = 'enabled' in request.form
    # Show the form regardless of request
    return homepage()

# @app.route('/alarm', methods=['GET', 'POST'])
# def manageAlarm():
# 	if request.method == 'GET':
# 		return jsonify(alarmSettings)
# 	elif request.method == 'POST':
# 		data = request.get_json()
# 		alarmSettings['time'] = data.get('time', alarmSettings['time'])
# 		alarmSettings['enabled'] = data.get('enabled', alarmSettings['enabled'])
# 		return jsonify(alarmSettings), 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
