# XML File Format Specification

This document specifices the XML file format for GTG data (task, tags, etc).


## Location and files

GTG saves all data in one file: `[XDG_DATA]/data/gtg/gtg_data.xml`. If the
file doesn't exist, GTG will try to load the different quick backups and
if that fails too it will create an empty file. The data file is
UTF-8 encoded.

**Backups** are stored in the `backups` folder next to the data file. GTG
creates a backup every time the file is saved, up to 10 versions. These
files are called `gtg_data.xml.bak.0`, `gtg_data.xml.bak.1` and so on. It also makes daily backups, there's no limit to these.


**Versioning** code is stored in the `versioning.py` module. We maintain
support for n-1 versions, with n being the current version of the file
format. File format versions don't necessarily follow GTG versions and they
can be found in the root tag of the data file.


## Tag structure

### gtgData

The root tag for the file.


| Attribute           | Description                                  |
|---------------------|----------------------------------------------|
| appVersion          | GTG version that generated this file         |
| xmlVersion          | File format version                          |


### tagList

Contains task tags. Every tag is stored, even if it doesn't have any
custom attributes.

- Always present: **Yes**


### tag




### taskList



## Task Content

Task contents are stored in _GTG-flavored_ markdown. At the moment this
includes the following tags:


| Tag                 | Description                                  |
|---------------------|----------------------------------------------|
| `{! [Task UUID] !}` | Link to a subtask identified by [Task UUID]  |
| `@Tag-name`         | A GTG tag applied to the task                |


### Mapping of Gtk Text Tags to content


## Full Example
