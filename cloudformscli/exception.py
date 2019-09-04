class CloudFormsClientException(Exception):
    pass


class ObjectNotFoundException(CloudFormsClientException):
    pass

class TooManyObjectsException(CloudFormsClientException):
    pass

class InvalidProviderException(CloudFormsClientException):
    pass

class CloudFormsClientRequestException(CloudFormsClientException):
    def __init__(self, error_data, http_status_code):
        super(CloudFormsClientRequestException, self).__init__(
            str({"error_data": error_data,
                 "http_status_code": http_status_code}))
        self.error_data = error_data
        self.http_status_code = http_status_code
