import logging
import os
import boto3

from users.lambda_handler import LambdaHandler

logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))


class GroupRemover(LambdaHandler):
    """
    GroupRemover will be invoked via API gateway.  When called it'll authorize the user
    and then remove the requested user from the requested cognito group.
    """

    def __init__(self, success_status_code, required_group):
        super().__init__(success_status_code, required_group)
        self._client = boto3.client('cognito-idp')
        self._user_pool_id = os.environ['USER_POOL_ID']

    def execute(self, request):
        groupname = request.get_path_parameter('groupname')
        username = request.get_path_parameter('username')

        cognito_response = self._client.admin_remove_user_from_group(
            UserPoolId=self._user_pool_id,
            Username=username,
            GroupName=groupname
        )
        return cognito_response


def handler(event, context):
    fetcher = GroupRemover(200, 'UserManager')
    return fetcher.lambda_handle(event, context)
