# JIRA issue importer
## Under development

This is an out-of-JIRA tool to export-import issues with automated flows.

## Installation

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