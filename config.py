#!/usr/bin/env python3
#codinf:utf-8

"""
Copyright(C) 2020 Lemoine Automation Technologies

This file is part of Pivotalzibot.

Pivotalzibot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pivotalzibot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with Pivotalzibot.  If not, see <https://www.gnu.org/licenses/>.

Config file.

BUGZILLA_ADDR: the address of the bugzilla server
API_KEY: the token for the bugzilla api.

PIVOTAL_xxx: xxx bug status on pivotal.
BUGZILLA_S_xxx: xxx bug status on bugzilla
BUGZILLA_R_xxx: xxx bug resolution on bugzilla

DEFAULT_RESOLUTIONS: dict mapping the bugzilla status to the resolution
    associated.

STATUS_PIVOTAL_TO_BUGZILLA: map a pivotal status to a bugzilla status. Is a
    pivotal status is not in STATUS_PIVOTAL_TO_BUGZILLA, we wont update the
    bugzilla status.
"""

BUGZILLA_ADDR = ""
API_KEY = ""

PIVOTAL_UNSTARTED = 'unstarted'
PIVOTAL_STARTED = 'started'
PIVOTAL_DELIVERED = 'delivered'
PIVOTAL_ACCEPTED = 'accepted'
PIVOTAL_DELIVERED = 'delivered'
PIVOTAL_FINISHED = 'finished'
PIVOTAL_REJECTED = 'rejected'
PIVOTAL_PLANNED = 'planned'
PIVOTAL_UNSHEDULED = 'unscheduled'


BUGZILLA_S_UNCONFIRMED = 'UNCONFIRMED'
BUGZILLA_S_CONFIRMED = 'CONFIRMED'
BUGZILLA_S_IN_PROGRESS = 'IN_PROGRESS'
BUGZILLA_S_RESOLVED = 'RESOLVED'
BUGZILLA_S_VERIFIED = 'VERIFIED'

BUGZILLA_R_FIXED = 'FIXED'
BUGZILLA_R_INVALID = 'INVALID'
BUGZILLA_R_WONTFIX = 'WONTFIX'


DEFAULT_RESOLUTION = {
    BUGZILLA_S_RESOLVED: BUGZILLA_R_FIXED,
}

STATUS_PIVOTAL_TO_BUGZILLA = {
  PIVOTAL_UNSTARTED: BUGZILLA_S_UNCONFIRMED,
  PIVOTAL_STARTED: BUGZILLA_S_CONFIRMED,
  PIVOTAL_FINISHED: BUGZILLA_S_RESOLVED,
  PIVOTAL_DELIVERED: BUGZILLA_S_RESOLVED,
  PIVOTAL_ACCEPTED: BUGZILLA_S_VERIFIED,
}
