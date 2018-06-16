import json

class JiraAPIHelper:
    "Each JIRA API - specific thing goes here. The goal is,\
    that if JIRA API changes, only this file has to be changes."

    # URLs
    def search_url(jql):
        return "search?jql=" + jql
    def issue_put_url():
        return "issue"
    def issue_get_url(key):
        return "issue/" + key
    def transition_url(id):
        return "issue/" + id + "/transitions"
    def assignee_url(id):
        return "issue/" + id + "/assignee" 
    def attach_file_url(key):
        return "issue/" + ticketId + "/attachments"

    #JQLs
    def jql_child_issues(issue):
        return "parent=" + issue["key"] + " order by createdDate DESC"
    def key_list_to_jql(keys):
        jql = ""
        for key in keys:
            jql = jql + " summary ~" + key + " or"
        return jql[:-1][:-1] #removes last "or"

    # Select given attributes from issue
    def external_issue_id(issue):
        return issue["fields"]["customfield_10013"]
    def description_of_issue(issue):
        return issue["fields"]["description"]
    def external_ticket_id(ticket):
        return ticket["fields"]["customfield_10013"]
    def attach_list(issue):
        return issue["fields"]["attachment"]
    def priority_name(issue):
        return issue["fields"]["priority"]["name"]
    def fix_version_name(issue):
        return issue["fields"]["fixVersions"][0]["name"]
    
    # Transition things
    def transition_id_todo():
        return 501

    # Create API data
    def create_transition_data(transitionId):
        data = dict()
        data["transition"] = dict()
        data["transition"]["id"] = transitionId
        return json.dumps(data)

    def create_sub_issue_create_data(type_id):
        data = dict()
        data["transition"] = dict()
        data["transition"]["id"] = 561        
        data["fields"] = dict()
        data["fields"]["customfield_11310"] = list() # Possible sub-tasks
        data["fields"]["customfield_11310"].append(dict())
        data["fields"]["customfield_11310"][0]["id"] = str(type_id)
        return json.dumps(data)

    def create_assign_data(name):
        data = dict()
        data["name"]=name
        return json.dumps(data)

    def copy_description_data(issue):
        data = dict()
        data["fields"] = dict()
        data["fields"]["description"] = JiraAPIHelper.description_of_issue(issue)
        return json.dumps(data)

    # Parse API responses
    def parse_key_list_response(response, force_use_key):
        keys = []
        if "issues" in response:
            for issue in response["issues"]:
                if force_use_key:
                    keys.append(issue["key"])
                else: 
                    try:
                        keys.append(JiraAPIHelper.external_issue_id(issue))
                    except:
                        keys.append(issue["key"])                    
        else:
            print("WARN - empty response from JIRA. Response:")
            print(str(response))
        return keys

    def parse_put_issue_response(response):
        if "key" in response:
            print("INFO - Issue successfully created with ID " + response["key"])
            return response["key"]
        else:
            print("WARN - Issue creation seems successful, but there is no returned key! Message:")
            print(str(response))
            return ""