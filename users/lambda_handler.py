import json
from abc import ABC, abstractmethod
import logging
from users.request import Request
from datetime import date, datetime


def iso_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class LambdaHandler(ABC):
    def __init__(self, success_status_code, required_group):
        self._success_status_code = success_status_code
        self._required_group = required_group

    @abstractmethod
    def execute(self, request):
        pass

    def lambda_handle(self, event, context):
        """
        Handle the incoming request from the API Gateway, wrap it in a Request object,
        and pass it on via the abstract execute method.
        :param event: the lambda event
        :param context: the lambda context
        :return: the response formatted for the API Gateway
        """
        status_code = self._success_status_code
        body = None
        try:
            request = Request(event)
            if not request.has_group(self._required_group):
                raise PermissionError

            body = self.execute(request)

        except ValueError as ve:
            status_code = 422
            body = {"message": str(ve)}

        except PermissionError as pe:
            logging.exception(pe)
            status_code = 403
            body = {"message": "Forbidden"}

        except Exception as e:
            logging.exception(e)
            status_code = 500

        # create a response
        response = {
            "statusCode": status_code,
        }
        if body is not None:
            response['body'] = json.dumps(body, default=iso_serializer)
        logging.debug(response)
        return response
