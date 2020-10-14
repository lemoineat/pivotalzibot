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

Bugzilla handler.
"""

from typing import Union
import requests
import config

class Bugzilla:
    """
    This class encapsulate the handling of the Bugzilla API.

    self.addr: str, the addresse of the bugzilla server
    self.api_key: str, the api token
    """

    def __init__(self):
        self.addr = config.BUGZILLA_ADDR
        self.api_key = config.API_KEY

    def send_comment(self, comment:str, bug_id:int):
        """
            comment: the comment to send
            bug_id: the bugzilla id of the bug to comment
            Send a comment to a bugzilla bug.
        """
        url = "{}/rest/bug/{}/comment".format(self.addr, bug_id)
        data = {
            'api_key': self.api_key,
            'comment': comment
        }
        return requests.post(url, json=data)

    def update_status(self, new_status:str, bug_id:int, resolution:Union[None, str]=None):
        """
            new_status: the new status of the bug
            bug_id: the bugzilla id of the bug to update
            Update the status of a bugzilla bug.

            If the change is not allowed by the workflow, bugzilla is not updated.
        """
        url = "{}/rest/bug/{}".format(self.addr, bug_id)
        data = {
            'api_key': self.api_key,
            'status': new_status,
        }
        resolution = config.DEFAULT_RESOLUTION.get(new_status, None)
        if resolution is not None:
            data['resolution'] = resolution
        return requests.put(url, json=data)
