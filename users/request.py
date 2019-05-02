import json


class Request:
    """
    Convenience class for pulling apart the interesting parts of a lambda request.
    """

    def __init__(self, event):
        print("event: " + str(event))
        self._event = event
        if 'requestContext' in event and 'authorizer' in event['requestContext'] and 'claims' in event['requestContext']['authorizer']:
            self._claims = event['requestContext']['authorizer']['claims']
        else:
            self._claims = {}

        if 'pathParameters' in event:
            self._path_parameters = event['pathParameters']
        else:
            self._path_parameters = {}

        if 'queryStringParameters' in event:
            self._get_parameters = event['queryStringParameters']
        else:
            self._get_parameters = {}

        if 'cognito:groups' in self._claims and self._claims['cognito:groups'] is not None:
            self._cognito_groups = self._claims['cognito:groups'].split(',')
        else:
            self._cognito_groups = []

    def get_path_parameter(self, param):
        return self._path_parameters[param]

    def get_get_parameter(self, param):
        if param not in self._get_parameters:
            raise ValueError("Expected parameter: " + param)
        return self._get_parameters[param]

    def has_group(self, group):
        return group in self._cognito_groups

    def get_username(self):
        return self._claims['cognito:username']

    def load_body(self):
        if 'body' in self._event and self._event['body'] is not None:
            return json.loads(self._event['body'])
        else:
            return {}
