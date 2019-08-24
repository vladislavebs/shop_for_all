class InternalError(Exception):
    code = 500
    message = 'Unexpected exception. '
    data = {}

    def __init__(self, exception):
        if isinstance(exception, Exception):
            self.message += str(exception)
            self.data = str(exception.__cause__)

    def get_error(self):
        return {
            'error_name': self.__class__.__name__,
            'code': self.code,
            'message': self.message,
            'data': self.data
        }


class IdNotFound(InternalError):
    code = 404
    message = 'Given id not found.'

    def __init__(self, unit_id):
        self.data = {
            'id': unit_id
        }


class InvalidRequest(InternalError):
    code = 406
    message = 'Given parameters are wrong'

    def __init__(self, data):
        for key, item in data.items():
            self.message = str(item[0]) if item[0] else self.message
            self.field = key


class IntegrityErrorParser:
    code = 500

    def __init__(self, message):
        if 'duplicate key value violates unique constraint' in str(message):
            self.code = 406
            self.detail = 'Already exists'


class TransportError(Exception):
    code = 400
    message = 'Invalid filters'

    def __init__(self, message):
        self.code = message.status_code
        try:
            text = message.args[2]['error']['failed_shards'][0]['reason']['caused_by']['reason']
            self.message = f"Invalid filters {text.lower()}"
        except Exception as e:
            print(e)
