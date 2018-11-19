# pylint: disable=W0221,C0103,no-member
"""Nameko HTTP entrypoint (Werkzeug) request argument parsing module.
"""
import json
import werkzeug

from webargs import core, ValidationError as WebArgsValidationError


def is_json_request(req):
    return core.is_json(req.mimetype)


class NamekoWebParser(core.Parser):

    __location_map__ = dict(
        cookies='parse_cookies',
        files='parse_files',
        form='parse_form',
        headers='parse_headers',
        json='parse_json',
        querystring='parse_querystring',
        query_string='parse_querystring'
    )

    def parse_json(self, req, name, field):
        """Pull a json value from the request."""
        body = req.get_data(as_text=True)
        if not (body and is_json_request(req)):
            return core.missing

        try:
            json_data = json.loads(body)
        except (TypeError, ValueError):
            return core.missing

        return core.get_value(json_data, name, field, allow_many_nested=True)

    def parse_querystring(self, req, name, field):
        return core.get_value(req.args, name, field)

    def parse_form(self, req, name, field):
        try:
            return core.get_value(req.form, name, field)
        except AttributeError:
            pass
        return core.missing

    def parse_headers(self, req, name, field):
        return core.get_value(req.headers, name, field)

    def parse_cookies(self, req, name, field):
        return core.get_value(req.cookies, name, field)

    def get_request_from_view_args(self, view, args, kwargs):
        req = args[1]
        assert isinstance(req, werkzeug.Request), 'Argument is not a werkzeug.Request'
        return req

    def parse_files(self, req, name, field):
        return core.get_value(req.files, name, field)

    def handle_error(self, error, req, schema):
        """Handles errors during parsing."""
        status_code = getattr(error, 'status_code', self.DEFAULT_VALIDATION_STATUS)
        raise WebArgsValidationError(status_code=status_code, message=error.messages)


parser = NamekoWebParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
