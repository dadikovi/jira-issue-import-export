from src import Configuration
from src import Commands
from src import Helper
from src import JIRAAppendS2
from src import Reporter

# init

jii_config = Configuration()
jii_config.system('external').start_session()

# get the key list to process

basic_key_list = Commands.get_key_list(
    jii_config.system('external'),
    jii_config.system('external').get_config('key_list_jql')
)

# process the issues (do mappings, etc.)

print("INFO - Started handling the following issues:" + str(basic_key_list))

raw_data = Helper.get_issues_data(basic_key_list, jii_config.system('external'))
jira_data = Helper.process_issues(raw_data, jii_config)
Helper.save_data(jira_data, jii_config)
Helper.download_attachments(jira_data, raw_data, jii_config, jii_config.system('external'))

# filter existing issues

jii_config.system('internal').start_session()
jql = Helper.key_list_to_jql(basic_key_list)
existing_list = Commands.get_key_list(
    jii_config.system('internal'),
    jql
)

keys_to_import = list(set(basic_key_list) - set(existing_list))

print("INFO - These tickets should be imported:" + str(keys_to_import))
print("INFO - These tickets are already imported:" + str(existing_list))

JIRAAppendS2.import_issues(jii_config.system('internal'), keys_to_import, jira_data)

Reporter.create_report(jii_config, jira_data)

print("INFO - Success!")