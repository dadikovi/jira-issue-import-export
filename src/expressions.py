import json
import re

class Expressions:
    "Very basic expression engine, should be refactored\
    or replaced by a tool"
    
    def __init__(self, jii_config):
        self.jii_config = jii_config

    def handle_key_expr(self, rule_key, response, issue_key, allowObj = False):
        if rule_key.startswith("CONCAT("):
            val = self.concatValues(rule_key, response, issue_key)
        elif rule_key.startswith("JSONDECODE("):
            val = self.jsonDecode(rule_key, response, issue_key);
        else:
            val = self.selectValueByRule(rule_key, response, issue_key, allowObj)

        return val

    def handleJsonObject(self, jsonObject, parentKey, externalKeys, values, key):
        value = ""
        i = 0
        for externalKey in externalKeys:
            externalKey = externalKey.replace(parentKey+".", "")
            parsedValue = self.handle_key_expr(externalKey, jsonObject, key)
            
            i = i+1
            
            if i < 3:
                value = value + "*";
            
            value = value + parsedValue
            
            if i < 3:
                value = value + "*";
            
            value = value + "\r\n"
        
        value = value[:-1]
        values = values + "\r\n----\r\n" + value
        return values

    def jsonDecode(self, jsonExpr, response, key):
        externalKeys = self.getKeysFromJsonExpr(jsonExpr)
        parentKey = externalKeys[0]
        del externalKeys[0]

        jsonObjects = self.handle_key_expr(parentKey, response, key, True)

        values = ""
        if isinstance(jsonObjects, list):
            for jsonObject in jsonObjects:
                values = self.handleJsonObject(jsonObject, parentKey, externalKeys, values, key)
        else:
            values = self.handleJsonObject(jsonObjects, parentKey, externalKeys, values, key)
        return values[:-1]

    def concatValues(self, concatExpr, response, key):
        externalKeys = self.getKeysFromConcatExpr(concatExpr)
        values = ""

        for key in externalKeys:
            if(key):
                valuesFromResp = self.handle_key_expr(key, response, key)

                if type(valuesFromResp) is str:
                    values = values + valuesFromResp + " "
                elif type(valuesFromResp) is list:
                    for value in valuesFromResp:
                        if value != "N/A":
                            values = values + str(value) + " "
                else:
                    print("WARN - Type of value is " + str(type(valuesFromResp)))

        return values[:-1] #Removes the last char

    def removeOneExprFromKeyList(self, keyList,expr):
        keyList_old = keyList
        keyList = keyList.replace(expr+",", "", 1)
        if keyList_old == keyList:
            #Expression is at the end of keyList. 
            keyList = keyList.replace(expr, "", 1)
        return keyList

    def abstractGetKeysFromExpr(self, expr, function):    
        returnValues = []
        expr = expr.replace(function + "(", "")[:-1] #removes last ) char
        calcFull = False

        while not calcFull:
            for key in expr.split(","):
                if re.match(r'([A-Z]+\()', key):
                    #This is an expression.
                    otherExp = re.match('([A-Z]+\(.*?\))', expr);
                    if otherExp:
                        #This is a valid expression.
                        otherExpStr = otherExp.group(0)
                        returnValues.append(otherExpStr)
                        expr = self.removeOneExprFromKeyList(expr,otherExpStr)
                        break
                else:
                    returnValues.append(key)
                    expr = self.removeOneExprFromKeyList(expr,key)

                if expr == "":
                    calcFull = True
        return returnValues

    def getKeysFromConcatExpr(self, concatExpr):
        return self.abstractGetKeysFromExpr(concatExpr, "CONCAT")
    def getKeysFromJsonExpr(self, jsonExpr):
        return self.abstractGetKeysFromExpr(jsonExpr, "JSONDECODE")

    def selectValueByRule(self, externalKey, response, key, allowObj):
        "Selects the value named by `externalKey` in the response. Can handle arrays too."
        values = [response] # An array with one element
        levels = externalKey.split(".")
        for level in levels:
            for i in range(0, len(values)):
                value=values[i]
                if level not in value:
                    values[i] = externalKey; # Value does not exists in response
                else:    
                    try:
                        if isinstance(value[level], list):
                            for element in value[level]:                   
                                values.append(element)
                            del values[i]
                        else:
                            values[i]=value[level]
                    except TypeError:
                        print("ERROR - could not find value: " + externalKey)
                        print(response)

        self.handleSpecialFields(externalKey, values, key)
        
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return ""
        elif allowObj:
            return values
        else:        
            return values[0]

##########################################
## SPECIAL FIELD PLUGINS #################
##########################################

    def handleSpecialFields(self, externalKey, values, key):
        #self.handleAttachment(externalKey, values, key)
        self.handlePriority(externalKey, values)
        self.handleFixVersion(externalKey, values)
        self.handleProjectCode(externalKey, values)
        return

    #def handleAttachment(self, externalKey, values, key):
    #    if externalKey == "fields.attachment.content":
    #        for url in values:
    #            downloads.append({'key':key,'url':url})
    #    return

    def abstractHandleMappedField(self, values,mapping):
        for rule in mapping:
            external,internal=rule
            for i in range(0, len(values)):
                value=values[i]
                if(value==external):
                    values[i]=internal
                    break
            if (external == "default"):
                if (len(values) == 0):
                    values.append(internal)
                elif(not values[0].strip()):
                    values[0] = internal;  
        return

    def handlePriority(self, externalKey, values):
        if(externalKey=="fields.priority.name"):
            self.abstractHandleMappedField(values, self.jii_config.get_mapping('priority'))
        return

    def handleFixVersion(self, externalKey, values):
        if(externalKey=="fields.fixVersions.name"):
            self.abstractHandleMappedField(values, self.jii_config.get_mapping('fixversion'))
        return
    def handleProjectCode(self, externalKey, values):
        if(externalKey=="fields.project.key"):
            self.abstractHandleMappedField(values, self.jii_config.get_mapping('projectcode'))
        return

