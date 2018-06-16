from .commands import Commands

class JIRAAppendS2:
    def import_issues(system, keys_to_import, jira_data):
        for ticket in jira_data.issues():
            if Helper.getExternalTicketId(ticket) in keys_to_import:
                ticket["key"] = Commands.put_issue(system, ticket)
                Commands.attachFilesToJira(system,ticket, jira_data)
                Commands.issueToDo(system, ticket["key"])
                
                subTicketId = Commands.create_sub_issue(system, ticket, 11913) # Investigation type
                Commands.issueToDo(system, subTicketId)
                Commands.assignToLoxonBC(system, subTicketId)
                Commands.copyDescription(system, ticket, subTicketId)
                Commands.attachFilesToJira(system, ticket, jira_data, subTicketId)
        return