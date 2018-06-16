from .commands import Commands
from .jiraapihelper import JiraAPIHelper

class JIRAAppendT2:
    def import_issues(system, keys_to_import, jira_data):
        for ticket in jira_data.issues():
            print("Try to import: " + str(JiraAPIHelper.external_issue_id(ticket)))
            if JiraAPIHelper.external_issue_id(ticket) in keys_to_import:
                ticket["key"] = Commands.put_issue(system, ticket)
                Commands.attachFilesToJira(system,ticket, jira_data)
                Commands.issueToDo(system, ticket["key"])
                
                spec_issue = Commands.create_sub_issue(system, ticket, 11918)
                Commands.issueToDo(system, spec_issue)
                Commands.assign(system, spec_issue, "loxon_bc")
                Commands.copyDescription(system, ticket, spec_issue)
                Commands.attachFilesToJira(system, ticket, jira_data, spec_issue)

                spec_review_issue = Commands.create_sub_issue(system, ticket, 13993)
                Commands.assign(system, spec_review_issue, "loxon_bc")

                doc_issue = Commands.create_sub_issue(system, ticket, 11912)
                Commands.assign(system, doc_issue, "loxon_bc")

                doc_review_issue = Commands.create_sub_issue(system, ticket, 12115)
                Commands.assign(system, doc_review_issue, "loxon_bc")

                code_issue = Commands.create_sub_issue(system, ticket, 11916)
                Commands.assign(system, spec_review_issue, "loxon_dev")

                code_review_issue = Commands.create_sub_issue(system, ticket, 12114)
                Commands.assign(system, code_issue, "loxon_dev")

                com_issue = Commands.create_sub_issue(system, ticket, 11911)
                Commands.assign(system, com_issue, "pavlo.teyfel@loxon.eu")
        return