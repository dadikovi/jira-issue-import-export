from .jiraapi import JiraAPI
from .jiraapihelper import JiraAPIHelper
import json

class Commands:
    "The commands which can be executed on JIRA systems."

    def get_key_list(system, jql, force_use_key = False):
        url = JiraAPIHelper.search_url(jql)
        response = JiraAPI.get_api(url, system)
        return JiraAPIHelper.parse_key_list_response(response, force_use_key)

    def put_issue(system, issue):
        url = JiraAPIHelper.issue_put_url()
        data = json.dumps(issue)
        ret = JiraAPI.post_api(url, system, data)
        return JiraAPIHelper.parse_put_issue_response(ret)

    def issueToDo(system, key):
        Commands.doTransition(system, key, JiraAPIHelper.transition_id_todo())

    def doTransition(system, key, transitionId):
        url = JiraAPIHelper.transition_url(key)
        data = JiraAPIHelper.create_transition_data(transitionId)
        JiraAPI.post_api(url, system, data)

    def create_sub_issue(system, ticket, type_id):
        data = JiraAPIHelper.create_sub_issue_create_data(type_id)
        url = JiraAPIHelper.transition_url(ticket["key"])
        ret = JiraAPI.post_api(url, system, data)

        jql = JiraAPIHelper.jql_child_issues(ticket)
        created = Commands.get_key_list(system, jql, True)

        created_latest = created[0]
        print("INFO - Created key: " + str(created_latest))
        return created_latest        

    def assign(system, subTicketId, name):
        url = JiraAPIHelper.assignee_url(subTicketId)
        data = JiraAPIHelper.create_assign_data(name)
        JiraAPI.put_api(url, system, data)

    #DEPRECATED
    def assignToLoxonBC(system, subTicketId):
        assign(system, subTicketId, "loxon_bc")

    def copyDescription(system, ticket, subTicketId):
        url = JiraAPIHelper.issue_get_url(subTicketId)
        data =  JiraAPIHelper.copy_description_data(ticket)
        JiraAPI.put_api(url, system, data)

    def attachFilesToJira(system,ticket, jira_data, ticketId="OWN"):
        if ticketId == "OWN":
            ticketId = ticket["key"]

        for download in jira_data.downloads():
            print("INFO - uploading attachment " + str(download["key"]) + " " + str(JiraAPIHelper.external_ticket_id(ticket)) )
            if download["key"] == JiraAPIHelper.external_ticket_id(ticket):
                Commands.attachFileToJira(system, ticket, ticketId, download)
        return

    def attachFileToJira(system, ticket, ticketId, download):
        attachment = open(download["filepath"], 'rb')
        filename = download["filename"]
        files = {'file': (filename, attachment, 'application/octet-stream')}
        url = JiraAPIHelper.attach_file_url(ticketId)
        JiraAPI.upload(system, url, files)
        return







    