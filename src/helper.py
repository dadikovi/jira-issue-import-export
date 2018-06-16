from .jiradata import JiraData
from .jiraapi import JiraAPI
from .expressions import Expressions
from .jiraapihelper import JiraAPIHelper
from .commands import Commands
import datetime
import os
import json

class Helper:
    def import_issues(system, keys_to_import, jira_data):
        for ticket in jira_data.issues():
            if JiraAPIHelper.external_issue_id(ticket) in keys_to_import:
                ticket["key"] = Commands.put_issue(system, ticket)
                Commands.attachFilesToJira(system,ticket, jira_data)
                Commands.issueToDo(system, ticket["key"])
                
                subTicketId = Commands.openSubTicket(system, ticket)
                Commands.issueToDo(system, subTicketId)
                Commands.assignToLoxonBC(system, subTicketId)
                Commands.copyDescription(system, ticket, subTicketId)
                Commands.attachFilesToJira(system, ticket, jira_data, subTicketId)
        return

    def get_issues_data(basic_list, system):
        raw_issue_data = []
        for key in basic_list:
            d = Helper.get_issue_data(key, system)
            raw_issue_data.append(d)
        return raw_issue_data

    def key_list_to_jql(keys):
        return JiraAPIHelper.key_list_to_jql(keys)

    def get_issue_data(key, system):
        url = JiraAPIHelper.issue_get_url(key)
        resp = JiraAPI.get_api(url, system)
        return resp

    def process_issues(raw_data, jii_config):
        mapping = jii_config.get_mapping('fields')
        defaults = jii_config.get_mapping('defaults')
        jira_data = JiraData()

        for data in raw_data:
            issue = jira_data.create_issue()

            for default in defaults:
                Helper.add_default_value(default, issue)
            for rule in mapping:
                Helper.handle_rule(rule, data, issue, jii_config)
            Helper.postProcessTicket(issue, jii_config)
        
        return jira_data

    def download_attachments(jira_data, raw, jii_config, system):
        for issue in raw:
            try:
                #print(issue)
                attach_list = JiraAPIHelper.attach_list(issue)
                key = issue["key"]
                for attach in attach_list:
                    url = attach["content"]
                    jira_data.downloads().append({'key':key,'url':url})
            except KeyError:
                pass
        for download in jira_data.downloads():
            Helper.downloadAndWriteFile(download, jii_config.result_path(), system) 

    def save_data(jira_data, jii_config):      
        path = jii_config.result_path() + '/result.json'
        
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, 'a+') as f:
             json.dump(jira_data.issues(), f)
        return


# THIS PART OF CODE SHOULD BE REFACTORED!

    def handle_rule(rule, response, ticket, jii_config):
        externalKey, internalKey=rule
        key = response["key"]
        expr = Expressions(jii_config)
        
        value = str(expr.handle_key_expr(externalKey, response, key))
        Helper.writeDataToTicket(internalKey, ticket, value)    
        return

    def add_default_value(default, ticket):
        internalKey, value=default
        Helper.writeDataToTicket(internalKey, ticket, value)
        return

    def writeDataToTicket(internalKey, ticket, values):
        if(internalKey=="SPECIAL"):
            return

        levels = internalKey.split(".")
        internalValue=ticket

        i=0
        for level in levels:
            i+=1
            if i == len(levels):
                internalValue.setdefault(level, values)
            else:
                if level.endswith("[0]"):
                    level = level.replace("[0]", "")
                    internalValue.setdefault(level, list())
                    internalValue[level].append(dict())
                    internalValue = internalValue[level][0]
                else:
                    internalValue.setdefault(level, dict())
                    internalValue = internalValue[level]
        return

    def handleDueDate(ticket):
        daysToAdd = 20
        prio = JiraAPIHelper.priority_name(ticket)

        if prio == "Trivial":
            daysToAdd = 14
        elif prio == "Minor":
            daysToAdd = 7
        elif prio == "Major":
            daysToAdd = 4
        elif prio == "Critical":
            daysToAdd = 3
        elif prio == "Blocker":
            daysToAdd = 1

        dueDate = datetime.date.today() + datetime.timedelta(days=daysToAdd)
        dueDateValue = dueDate.strftime('%Y-%m-%d')
        Helper.writeDataToTicket("fields.duedate", ticket, dueDateValue)

    def handleCostItem(ticket, jii_config):
        lst = list()
        expr = Expressions(jii_config)
        lst.append(JiraAPIHelper.fix_version_name(ticket))
        expr.abstractHandleMappedField(lst, jii_config.get_mapping('costitem'))
        Helper.writeDataToTicket("fields.customfield_11611.id", ticket, lst[0])

    def postProcessTicket(ticket, jii_config):
        Helper.handleCostItem(ticket, jii_config)
        Helper.handleDueDate(ticket)

    ##########################################
    ## FILE DOWNLOAD METHODS #################
    ##########################################

    def getFullPath(pathBase, filename, key):
        return pathBase+"/"+ Helper.getFullName(filename, key)
    def getFullName(filename, key):
        return key+"_-_"+filename

    def downloadAndWriteFile(download, pathBase, system):
        url=download["url"]
        key=download["key"]
        
        filename=Helper.getFilenameFromUrl(url)
        file = JiraAPI.download(url, system)

        with open(Helper.getFullPath(pathBase, filename, key), 'wb+') as f:
            f.write(file)

        download["filepath"] = Helper.getFullPath(pathBase, filename, key);
        download["fullname"] = Helper.getFullName(filename, key)
        download["filename"] = filename
        return

    def getFilenameFromUrl(url):
        urlParts=url.split("/")
        return urlParts[-1]    