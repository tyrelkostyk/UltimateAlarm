import os
import sqlite3
from flask import Flask, request, render_template_string, g, abort

app = Flask(__name__)


## DATABASE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'alarm.db')

def getDb():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def initDb():
	with app.app_context():
		db = getDb()
		cursor = db.cursor()
		cursor.execute('''
		CREATE TABLE IF NOT EXISTS alarms (
			day INTEGER PRIMARY KEY,
			timeHour INTEGER NOT NULL,
			timeMinute INTEGER NOT NULL,
			enabled BOOLEAN NOT NULL DEFAULT 0
		);
		''')
		db.commit()

		# Pre-populate the table with default values for each day of the week (if empty)
		cursor.execute('SELECT COUNT(*) FROM alarms')
		if cursor.fetchone()[0] == 0:  # Fetchone returns a tuple and [0] is the count
			# Table is empty, populate it with default values
			days = [(i, 0, 0, False) for i in range(7)]  # Default values for each day
			cursor.executemany('INSERT INTO alarms (day, timeHour, timeMinute, enabled) VALUES (?, ?, ?, ?);', days)
			db.commit()


### HTML

homePageHtml = '''
<h1>Welcome to the Ultimate Alarm!</h1>
{alarmsHtml}
<form method="post" action="/update">
	<label for="day">Day:</label>
	<select id="day" name="day">
		<option value="0">Monday</option>
		<option value="1">Tuesday</option>
		<option value="2">Wednesday</option>
		<option value="3">Thursday</option>
		<option value="4">Friday</option>
		<option value="5">Saturday</option>
		<option value="6">Sunday</option>
	</select><br>
	<label for="timeHour">Hour:</label>
	<input type="number" id="timeHour" name="timeHour" min="0" max="23"><br>
	<label for="timeMinute">Minute:</label>
	<input type="number" id="timeMinute" name="timeMinute" min="0" max="59"><br>
	<label for="enabled">Enabled:</label>
	<input type="checkbox" id="enabled" name="enabled"><br>
	<input type="submit" value="Update Alarm">
</form>
'''

def getAlarmsHtml():
	db = getDb()
	cursor = db.cursor()
	alarmsHtml = ''
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	for i, day in enumerate(days):
		cursor.execute('SELECT timeHour, timeMinute, enabled FROM alarms WHERE day = ?', (i,))
		alarm = cursor.fetchone()
		if alarm:
			timeHour, timeMinute, enabled = alarm
			enabledText = 'Yes' if enabled else 'No'
		else:
			timeHour, timeMinute, enabledText = '0', '0', 'No'
		alarmsHtml += f'<div><strong>{day}:</strong> {timeHour}:{timeMinute} - Enabled: {enabledText}</div>'
	return alarmsHtml

### ROUTES

@app.route('/')
def home():
	return render_template_string(homePageHtml.format(alarmsHtml=getAlarmsHtml()))

@app.route('/update', methods=['POST'])
def updateAlarm():
	try:
		day = request.form['day']
		timeHour = request.form['timeHour']
		timeMinute = request.form['timeMinute']
		enabled = 'enabled' in request.form
		db = getDb()
		cursor = db.cursor()
		print(f"Updating alarm for {day}: {timeHour}:{timeMinute}, enabled: {enabled}")
		cursor.execute('REPLACE INTO alarms (day, timeHour, timeMinute, enabled) VALUES (?, ?, ?, ?);',
						(day, timeHour, timeMinute, enabled))
		db.commit()
		print("Database updated successfully.")
	except sqlite3.DatabaseError as e:
		print(f"Database error occurred: {e}")
		abort(500)
	except Exception as e:
		print(f"An error occurred: {e}")
		abort(500)
	return home()


if __name__ == '__main__':
	initDb()
	app.run(host='0.0.0.0', port=5000)
