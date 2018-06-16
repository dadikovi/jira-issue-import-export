import os
import json

class Reporter:
    def create_report(jii_config, jira_data):
        print("INFO - Writing report...")
        mdcontent = Reporter.get_content(jira_data)
        path = jii_config.result_path() + '/report.md'
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, 'a+') as f:
             f.write(mdcontent)

    def get_content(jira_data):
        imported = []
        didnttry = []
        written = False
        md = "# IssueImporter Report\n\n"

        for issue in jira_data.issues():
            if "key" in issue:
                imported.append(issue)
            else:
                didnttry.append(issue)

        md = md + "Imported tickets: "

        for issue in imported:
            md = md + " - " + issue["key"] + " (" + issue["fields"]["customfield_10013"] + ")\n"
        
        if not written:
            md = md + " - _none_\n"

        md = md + "Already imported tickets (no changes executed): "

        for ticket in didnttry:
            md = md + "### " + ticket["fields"]["customfield_10013"] + "\n\n"
            md = md + "Information:\n\n"
            md = md + "```\n\n"
            md = md + json.dumps(ticket, indent=4, sort_keys=True)
            md = md + "```\n\n"
            md = md + "\n\n"

            startText = False

            for download in jira_data.downloads():
                if(download["key"] == ticket["fields"]["customfield_10013"]):
                    if not startText:
                        md = md + "Also, here are some attachments:\n\n"
                        startText = True
                    md = md + "![" + download["filename"] + "](" + download["fullname"] + " \"" + download["filename"] + "\")\n\n"
        return md



