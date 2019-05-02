import logging
import os
import json
import boto3
from users.lambda_handler import LambdaHandler

logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))


class UserGetter(LambdaHandler):
    """
    ActualsFetcher will be invoked when called via the API.  When called it'll pull the
    pre-calculated actuals out of the database and return them to the caller.
    """

    def __init__(self, success_status_code, required_group):
        super().__init__(success_status_code, required_group)
        self._client = boto3.client('cognito-idp')
        self._user_pool_id = os.environ['USER_POOL_ID']

    def execute(self, request):
        username = request.get_username()
        cognito_response = self._client.admin_get_user(
            UserPoolId=self._user_pool_id,
            Username=username
        )
        return cognito_response


def handler(event, context):
    fetcher = UserGetter(200, 'ActiveUsers')
    return fetcher.lambda_handle(event, context)


if __name__ == '__main__':
    event = {
        "httpMethod": "GET",
        "requestContext": {
            "authorizer": {
                "principalId": "9804c73f-80ba-41d4-9a96-f69acc79478d"
            }
        },
        "queryStringParameters": {
            "date": "2019-03-29"
        }
    }
    response = handler(event, '')
    print(response)
