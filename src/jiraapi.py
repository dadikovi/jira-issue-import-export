import requests
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from json.decoder import JSONDecodeError

class JiraAPI:
    @staticmethod
    def get_json_header():
        return {'Content-Type':'application/json'}

    @staticmethod
    def create_session(system):
        sess_id = JiraAPI.create_session_id(system)
        session = requests.Session()
        session.auth = JiraAPI.create_session_id_auth(system)
        session.verify = False
        session.cookies = requests.cookies.cookiejar_from_dict({ 'JSESSIONID' : sess_id })
        session.headers.update(JiraAPI.get_json_header())
        return session

    @staticmethod
    def create_session_id(system):
        try:
            print(JiraAPI.create_session_id_url(system))
            response = requests.post(
                JiraAPI.create_session_id_url(system),
                auth = JiraAPI.create_session_id_auth(system),
                verify = False,
                data = JiraAPI.create_session_id_data(system),
                headers = JiraAPI.get_json_header()
            )
            resp_json = json.loads(response.text)
            return resp_json["session"]["value"]
        except JSONDecodeError:
            print("Response could no be parsed: ")
            print(JiraAPI.create_session_id_url(system))
            print(str(response.text))
            sys.exit(1)
        except TimeoutError:
            print("ERROR! Connection to " + JiraAPI.create_session_id_url(system) + " could not be established!")

    @staticmethod
    def create_session_id_data(system):
        data = dict()
        data["username"] = system.get_config('username')
        data["password"] = system.get_config('password')
        return json.dumps(data)

    @staticmethod
    def create_session_id_url(system):
        url = system.get_config('url_base')
        url = url + system.get_config('url_postfix_auth')
        return url

    @staticmethod
    def create_session_id_auth(system):
        if system.get_config('username_http'):
            return (
                system.get_config('username_http'),
                system.get_config('password_http')
                )
        else:
            return None

    @staticmethod
    def get_api(url, system):
        try:
            full_url = JiraAPI.create_full_url(url, system)
            
            print("INFO - Get " + full_url)

            resp = system.session().get(full_url)
            resp_json = json.loads(resp.text)
            return resp_json
        except JSONDecodeError:
            print("WARN - Not a valid JSON message arrived! " + str(resp.status_code))
            print(str(resp.text))
            return ""

    @staticmethod
    def put_api(url, system, data):
        try:
            full_url = JiraAPI.create_full_url(url, system)
            
            print("INFO - Put " + full_url)
            
            resp = system.session().put(full_url, data=data)
            resp_json = json.loads(resp.text)
            return resp_json
        except JSONDecodeError:
            print("WARN - Not a valid JSON message arrived! " + str(resp.status_code))
            print(str(resp.text))
            print(str(data))
            return ""

    @staticmethod
    def post_api(url, system, data):
        try:
            full_url = JiraAPI.create_full_url(url, system)
            
            print("INFO - Post " + full_url)
            
            resp = system.session().post(full_url, data=data)
            resp_json = json.loads(resp.text)
            return resp_json
        except JSONDecodeError:
            print("WARN - Not a valid JSON message arrived! " + str(resp.status_code))
            print(str(resp.text))
            print(str(data))
            return ""

    @staticmethod
    def download(full_url, system):
        resp = system.session().get(full_url)
        return resp.content

    @staticmethod
    def upload(system, url, files):
        full_url = JiraAPI.create_full_url(url, system)
        header = {'content-type': None, 'X-Atlassian-Token':'nocheck'}
        print("INFO - Upload " + full_url)
        system.session().post(full_url, headers=header, files=files)

    @staticmethod
    def create_full_url(url, system):
        full_url = system.get_config('url_base')
        full_url = full_url + system.get_config('url_postfix_api')
        full_url = full_url + url
        return full_url