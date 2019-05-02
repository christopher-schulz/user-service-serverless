import logging
import os
import boto3
from users.lambda_handler import LambdaHandler

logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))


class UserGetter(LambdaHandler):
    """
    UserGetter will be invoked via API gateway.  When called it'll look up the currently logged in
    user in Cognito and return those details.
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
