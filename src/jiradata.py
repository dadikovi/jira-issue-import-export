import json

class JiraData:
    def downloads(self):
        if not hasattr(self, '_downloads'):
            self._downloads = []
        return self._downloads

    def issues(self):
        if not hasattr(self, '_issues'):
            self._issues = []
        return self._issues

    def create_issue(self):
        issue = dict()
        self.issues().append(issue)
        return issue
