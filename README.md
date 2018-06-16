# JIRA issue importer
Version 0.3.0

## Installation

The whole installation process should be executed on virtual machine (where you can reach the external JIRA system. If you can reach it on your computer, than you can install this tool also there.)

You will need the following softwares to run the importer script:

- Python (not the snake, but the powerful script interpreter)
- Requests module for Python
- Markdown Viewer plugin for Chrome (recommended)

### Python

You have to download Python3, eg. from here:
`https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe`

Install it with "PIP" option (this is asked on the first screen of installer, but standard mode is OK).
Also, the checkbox about "adding to path" should be checked.

Then easily press Next and Install buttons...

### Requests module for Python

1. Download requests source code from this link: `https://github.com/requests/requests/zipball/master`
2. Extract it
3. Open a terminal (Windows + R then type `cmd` and press Enter)
4. Navigate to the directory where you extracted the source code (with `cd` command)
5. You will need the "_requests_" directory (if there is another "_requests_" directory in it, open that too.)
6. Execute command:

```pip install .```

That's all.

### Markdown Viewer plugin for Chrome (recommended)

1. Install it from chrome store: `https://chrome.google.com/webstore/detail/markdown-viewer`
2. In advanced options enable "_Detect text/markdown and text/x-markdown content type_" option.
3. Make sure that your computer opens `.md` files with Chrome

## Parameterization of the script

The behavior of the script can be parameterized with property files in directory `jiraIssueImporter/params`:

- `config.json`: the configurations of the handled JIRA systems. **Fill it!**
    - It has to be a well-formed JSON document, like:
    ```json
    {
        "jira_systems": {
            "name1": {
                "attribute1":"value1",
                "attribute2":"value2"
            },
            "name2": {
                ...
            }
        }
    }
    ```

    - Attributes:
        - url_base (required): the full URL of the system.
        - username (required): username used by login
        - password (required): password used by login
        - username_http (optional): if http base authentication needed for the jira system, the username should be provided in this attribute.
        - password_http (optional): if http base authentication needed for the jira system, the password should be provided in this attribute.
        - url_postfix_auth (required): mostly it is `auth/1/session`
        - url_postfix_api (required): mostly it is `rest/api/latest/`
        - key_list_jql (required in some cases): the JQL which determines the tickets to handle (should be specified only on that system where the JQL has to be executed)
- `defaults.properties.txt`: these values will be inserted by default.
- `fields.properties.txt`: contains the data mapping between JIRA instances.
- `priority.properties.txt`: mapping of priority values.
- `projectcode.properties.txt`: mapping of project code values.
- `fixversion.properties.txt`: mapping of fixversion values.

## Usage

After proper parameterization execute the following command in directory `jiraIssueImporter`:

```python import_issues_s2.py```

or

```python import_issues_t2.py```

according to your team. The two script will execute different import steps.

Check the output of script:
- _INFO_ messages contain some data for debugging
- _WARN_ messages can appear, this is not necessarily a problem.
- _ERROR_ messages mean problem...
- At the end of execution a _Success!_ message is written.

After that you can check the generated report (markdown viewer recommended) here:

`jiraIssueImporter/result/{latest-directory}/report.md`

In this directory you can find also the downloaded attachments (all of them, also the imported ones.), and the whole generated data file in json format.

**WARNING:** The _result_ directory is never cleaned, this should be done by you...

## Changelog

### v0.1.1

- fixed issue about CONCAT method ordering: eg. the comments in Description field will be at the bottom as requested.
- added cost item (new mapping file added)

### v0.1.2

- during post-processing of mapping properties now only the line-ending whitespaces will be deleted. Before every whitespace was deleted which caused wrong handling of fix versions (also the default value was selected).

### v0.2.0

- Developed dueDate handling
- Description and attachments are copied to created subticket
- Slightly bugfixes and improvements

### v0.3.0

- Huge refactor, parameterization changed
- Contains CR from T2 team

## TODO

### Business

- Fix version, affected version proper handling
- Better external environment handling
- Handling RT-project tickets

### DEV

- what about multiple values?
- empty expression handling
- refactor expression and reporter engines

### Future

- updates in external JIRA
- handling of modified tickets
- GUI for configure import steps