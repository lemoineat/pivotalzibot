#!/usr/bin/env python3
#codinf:utf-8

"""
Copyright(C) 2020 Lemoine Automation Technologies

This file is part of trackerzibot.

trackerzibot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

trackerzibot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with trackerzibot.  If not, see <https://www.gnu.org/licenses/>.

This program forwards the commments on Pivotal Tracker to bugzilla.

"""
from flask import Flask, request, json
from pivotal_handler import handle_update
import config

app = Flask(__name__)

@app.route('/test')
def hello():
    return """
Demons run when a good man goes to war <br>
Night will fall and drown the sun <br>
When a good man goes to war <br>
<br>
Friendship dies and true love lies<br>
Night will fall and the dark will rise<br>
When a good man goes to war<br>
<br>
Demons run, but count the cost<br>
The battle's won, but the child is lost
"""

@app.route('/', methods=['POST'])
def read_input():
    """
        Function called when the webhook of pivotal tracker is triggered.
    """
    data = request.get_json()
    print(data)
    try:
        handle_update(data)
    except Exception as e:
        print(e)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':
    # Test only, use `gunicorn -w 4 -b 127.0.0.1:5001 main:app` and nginx to
    # run the production server.
    app.run(host='0.0.0.0', port=1025, debug=False, ssl_context = 'adhoc')
