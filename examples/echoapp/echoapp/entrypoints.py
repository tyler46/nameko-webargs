import json

from nameko.web.handlers import HttpRequestHandler
from nameko.exceptions import safe_for_serialization
from webargs import ValidationError as WebArgsValidationError
from werkzeug.wrappers import Response


class HttpEntrypoint(HttpRequestHandler):
    """
    Overrides `response_from_exception` so we can customize error  handling.
    """
    mapped_errors = {
        WebArgsValidationError: (422, 'UNPROCESSABLE_ENTITY'),
    }

    def response_from_exception(self, exc):
        status_code, error_code = 500, 'UNEXPECTED_ERROR'

        if isinstance(exc, self.expected_exceptions):
            if type(exc) in self.mapped_errors:
                status_code, error_code = self.mapped_errors[type(exc)]
            else:
                status_code = 400
                error_code = 'BAD_REQUEST'

        return Response(
            json.dumps({
                'error': error_code,
                'message': safe_for_serialization(exc),
            }),
            status=status_code,
            mimetype='application/json'
        )


http = HttpEntrypoint.decorator
