import logging
import os
import boto3

from users.lambda_handler import LambdaHandler

logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))


class UserCreator(LambdaHandler):
    """
    UserCreator will be invoked via API gateway.  When called it'll authorize the user
    and then add requested cognito user.
    """

    def __init__(self, success_status_code, required_group):
        super().__init__(success_status_code, required_group)
        self._client = boto3.client('cognito-idp')
        self._user_pool_id = os.environ['USER_POOL_ID']

    def execute(self, request):
        request_body = request.load_body()
        username = request_body['username']
        email = request_body['email']

        cognito_response = self._client.admin_create_user(
            UserPoolId=self._user_pool_id,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ],
            DesiredDeliveryMediums=['EMAIL']
        )
        return cognito_response


def handler(event, context):
    fetcher = UserCreator(200, 'UserManager')
    return fetcher.lambda_handle(event, context)
