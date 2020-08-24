




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

Functions handling the pivotal tracker requests.

Custom types for type hints:

PivotalActivity: Generic data sent by Pivotal Tracker
PivotalCommentCreateActivity: Data sent by picotal on the creation of a comment
PivotalStoryUpdateActivity: Data sent by picotal on the update of a story

Constants:

SIGNATURE: String format for message signature
ANONYMOUS_FOOTER: Footer for anonymous message
"""

import re
import config
from typing import Dict, Union, List
from bugzilla import Bugzilla

# Generic data sent by Pivotal Tracker
PivotalActivity = Dict

# Data sent by picotal on the creation of a comment
PivotalCommentCreateActivity = Dict

# Data sent by picotal on the update of a story
PivotalStoryUpdateActivity = Dict

# String format for message signature
SIGNATURE = "\n\nFrom {author} on Pivotal Tracker"

# Footer for anonymous message
ANONYMOUS_FOOTER = "\n\nFrom Pivotal Tracker"

BUGZILLA_COMMENT_REGEX = re.compile("on Bugzilla\Z")

BUG_ID_REGEX = re.compile('^Bug (?P<bug_number>\d+):')

AT_BUG_REGEX = re.compile('@bugs\\b')

bugzilla = Bugzilla()


def get_author(data:PivotalActivity)->Union[None, str]:
    """
        data: the data sent by pivotal tracker.
        return the name of the author of the update, or None if not found.
    """
    if 'performed_by' not in data:
        return None
    if 'name' not in data['performed_by']:
        return None
    return data['performed_by']['name']

def get_comments(data:PivotalCommentCreateActivity)->List[str]:
    """
        data: the data sent by pivotal tracker on the creation of a comment.
        return the comments sent.
    """
    if 'changes' not in data:
        return []
    comments = []
    for change in data['changes']:
        if change['kind'] == 'comment':
            comments.append(change['new_values']['text'])
    return comments

def get_story_id(data:PivotalActivity)->Union[None,int]:
    """
        data: the data sent by pivotal tracker.
        return story id of the change if the change is related to a story,
            else None.
    """
    if 'primary_resources' not in data:
        return None
    for resource in data['primary_resources']:
        if resource['kind'] == 'story':
            return resource['id']
    return None

def get_bug_number(data:PivotalActivity)->Union[None,int]:
    """
        data: the data sent by pivotal tracker.
        return bug number of the story, if it exists. The bug number is in
            the name of the story, like this: "Bug 42: some description", where
            42 is the bug number.
    """
    if not 'primary_resources' in data:
        return None
    for ressource in data['primary_resources']:
        if ressource['kind'] != 'story':
            continue
        match = BUG_ID_REGEX.match(ressource['name'])
        if match is None:
            continue
        return int(match.group('bug_number'))
    return

def handle_comment_create(data:PivotalCommentCreateActivity):
    """
        data: the data sent by pivotal tracker on the creation of a comment.

        Send the comment to bugzilla.
    """
    author = get_author(data)
    comments = get_comments(data)
    bug_number = get_bug_number(data)
    if bug_number is None:
        return

    for comment in comments:
        if BUGZILLA_COMMENT_REGEX.findall(comment):
            continue
        if not AT_BUG_REGEX.findall(comment):
            continue
        #comment = re.sub(AT_BUG_REGEX, '', comment)
        if author is None:
            comment = comment + ANONYMOUS_FOOTER
        else:
            comment = comment + SIGNATURE.format(author=author)
        bugzilla.send_comment(comment, bug_number)
        #print(r.text)

def handle_story_update(data:PivotalStoryUpdateActivity):
    """
        data: the data sent by pivotal tracker on the creation of a comment.

        Check if the story is linked to bugzilla, if the status is updated and
        change the bugzilla status according to the config.
    """
    bug_number = get_bug_number(data)
    if bug_number is None:
        return
    for change in data['changes']:
        if not (change['kind'] == 'story' and change['change_type'] == 'update'):
            continue
        if 'original_values' not in change or 'new_values' not in change:
            continue
        if 'current_state' in change['original_values'] and \
           'current_state' in change['new_values'] and \
           change['original_values']['current_state'] != change['new_values']['current_state']:
            new_status = config.STATUS_PIVOTAL_TO_BUGZILLA.get(change['new_values']['current_state'], None)
            if new_status is not None:
                bugzilla.update_status(new_status, bug_number)

def handle_update(data:PivotalActivity):
    """
        data: the data sent by pivotal tracker.

        Read the data sent by pivotal tracker and call.
    """
    if data['kind'] == 'comment_create_activity':
        handle_comment_create(data)
    if data['kind'] == 'story_update_activity':
        handle_story_update(data)
    #print(data)
