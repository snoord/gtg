# -----------------------------------------------------------------------------
# Getting Things GNOME! - a personal organizer for the GNOME desktop
# Copyright (c) The GTG Team
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

"""Code to read older versions of the XML file."""

import os

from lxml import etree as et
from GTG.core.dates import Date
from GTG.core.dirs import DATA_DIR
from GTG.core import xml
from GTG.core import datastore

from datetime import datetime
from typing import Optional


def is_required(path: str) -> bool:
    """Determine if we need to run versioning code."""

    # Old filename for versions before 0.5
    old_file = os.path.join(DATA_DIR, 'gtg_tasks.xml')

    return not os.path.isfile(path) and os.path.isfile(old_file)


def convert(path: str, ds: datastore) -> et.ElementTree:
    """Convert old XML into the new format."""

    old_tree = xml.open_file(path, 'project')

    new_root = et.Element('gtgData')
    new_root.set('appVersion', '0.5')
    new_root.set('xmlVersion', '2')

    et.SubElement(new_root, 'taglist')

    tasklist = et.SubElement(new_root, 'tasklist')

    for task in old_tree.iter('task'):
        new_task = convert_task(task, ds)

        if new_task:
            tasklist.append(new_task)

    return et.ElementTree(new_root)


def convert_task(task: et.Element, ds: datastore) -> Optional[et.Element]:
    """Convert old task XML into the new format."""

    tid = task.attrib['id']
    real_task = ds.task_factory(tid)

    if task is None:
        return

    # Get the old task properties
    # TIDs were stored as UUID, but sometimes they were not present
    tid = task.get('uuid') or real_task.get_uuid() or tid
    status = task.get('status')
    title = task.find('title').text
    content = task.find('content').text

    try:
        done_date = task.find('donedate').text
    except AttributeError:
        done_date = None

    try:
        due_date = task.find('duedate').text
    except AttributeError:
        due_date = None

    try:
        modified = task.find('modified').text
    except AttributeError:
        modified = None

    try:
        added = task.find('added').text
    except AttributeError:
        added = None

    try:
        start = task.find('startdate').text
    except AttributeError:
        start = None


    # Build the new task
    new_task = et.Element('task')

    new_task.set('status', status)
    new_task.set('id', tid)

    new_title = et.SubElement(new_task, 'title')
    new_title.text = title

    dates = et.SubElement(new_task, 'dates')
    new_added = et.SubElement(dates, 'addedDate')
    new_modified = et.SubElement(dates, 'modifyDate')

    if added:
        added = Date(added).xml_str()
    else:
        added = datetime.now().isoformat()

    new_added.text = added

    if modified:
        modified = Date(modified).xml_str()
    else:
        modified = datetime.now().isoformat()

    new_modified.text = modified

    if done_date:
        new_done = et.SubElement(dates, 'doneDate')
        new_done.text = Date(done_date).xml_str()

    if start:
        start = Date(start)

        if start.is_fuzzy():
            new_start = et.SubElement(dates, 'fuzzyStartDate')
        else:
            new_start = et.SubElement(dates, 'startDate')

        new_start.text = start.xml_str()

    if due_date:
        due_date = Date(due_date)

        if due_date.is_fuzzy():
            new_due = et.SubElement(dates, 'fuzzyStartDate')
        else:
            new_due = et.SubElement(dates, 'startDate')

        new_due.text = due_date.xml_str()

    new_content = et.SubElement(new_task, 'content')
    new_content.text = et.CDATA(convert_content(content))

    return new_task


def convert_content(content: str) -> str:
    """Convert a task contents to new format."""

    # TODO: Implement this
    return content
