import json

import marshmallow as ma
from nameko.web.handlers import HttpRequestHandler
from nameko.exceptions import safe_for_serialization
from webargs import ValidationError, fields
from nameko_webargs.namekoparser import parser, use_args, use_kwargs
from webargs.core import MARSHMALLOW_VERSION_INFO
from werkzeug.wrappers import Response


class HttpEntrypoint(HttpRequestHandler):
    """
    Overrides `response_from_exception` so we can customize error  handling.
    """
    mapped_errors = {
        ValidationError: (422, 'UNPROCESSABLE_ENTITY'),
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


hello_args = {"name": fields.Str(missing="World", validate=lambda n: len(n) >= 3)}
hello_multiple = {"name": fields.List(fields.Str())}


class HelloSchema(ma.Schema):
    name = fields.Str(missing="World", validate=lambda n: len(n) >= 3)


strict_kwargs = {"strict": True} if MARSHMALLOW_VERSION_INFO[0] < 3 else {}
hello_many_schema = HelloSchema(many=True, **strict_kwargs)


class AppService(object):

    name = "app"

    @http("GET,POST", "/echo")
    def echo(self, request):
        parsed = parser.parse(hello_args, request)
        return Response(
            response=json.dumps(parsed),
            mimetype="application/json"
        )

    @http("GET", "/echo_query")
    def echo_query(self, request):
        parsed = parser.parse(hello_args, request, locations=("query",))
        return Response(
            response=json.dumps(parsed),
            mimetype="application/json"
        )

    @http("GET,POST", "/echo_use_args")
    @use_args(hello_args)
    def echo_use_args(self, request, args):
        return Response(
            response=json.dumps(args),
            mimetype="applcation/json"
        )

    @http("GET,POST", "/echo_use_args_validated")
    @use_args({"value": fields.Int()}, validate=lambda args: args["value"] > 42)
    def echo_use_args_validated(self, request, args):
        return Response(
            response=json.dumps(args),
            mimetype="applcation/json"
        )

    @http("GET,POST", "/echo_use_kwargs")
    @use_kwargs(hello_args)
    def echo_use_kwargs(self, request, name):
        return Response(
            response=json.dumps({"name": name}),
            mimetype="application/json"
        )

    @http("GET,POST", "/echo_multi")
    def multi(self, request):
        parsed = parser.parse(hello_multiple, request)
        return Response(
            response=json.dumps(parsed),
            mimetype="application/json"
        )

    @http("GET,POST", "/echo_many_schema")
    def many_nested(self, request):
        arguments = parser.parse(hello_many_schema, request, locations=("json", ))
        return Response(
            response=json.dumps(arguments),
            mimetype="application/json"
        )

    @http("GET", "/echo_use_args_with_path_param/<name>")
    @use_args({"value": fields.Int()})
    def echo_use_args_with_param(self, request, args, name):
        return Response(
            response=json.dumps(args),
            mimetype="applcation/json"
        )

    @http("GET", "/echo_use_kwargs_with_path_param/<name>")
    @use_kwargs({"value": fields.Int()})
    def echo_use_kwargs_with_path_param(self, request, name, value):
        return Response(
            response=json.dumps({"value": value}),
            mimetype="application/json"
        )

    @http("GET,POST", "/error", expected_exceptions=ValidationError)
    def error(self, request):
        def always_fail(value):
            raise ValidationError("something went wrong")

        args = {"text": fields.Str(validate=always_fail)}
        return Response(
            response=json.dumps(parser.parse(args, request)),
            mimetype="application/json"
        )

    @http("GET", "/echo_headers")
    def echo_headers(self, request):
        headers = parser.parse(hello_args, request, locations=("headers", ))
        return Response(
            response=json.dumps(headers),
            mimetype="applcation/json"
        )

    @http("GET", "/echo_cookie")
    def echo_cookies(self, request):
        cookies = parser.parse(hello_args, request, locations=("cookies", ))
        return Response(
            response=json.dumps(cookies),
            mimetype="applcation/json"
        )

    @http("POST", "/echo_file")
    def echo_file(self, request):
        args = {"myfile": fields.Field()}
        result = parser.parse(args, request, locations=("files", ))
        fp = result["myfile"]
        content = fp.read().decode("utf8")
        return Response(
            response=json.dumps({"myfile": content}),
            mimetype="applcation/json"
        )

    @http("POST", "/echo_nested")
    def echo_nested(self, request):
        args = {"name": fields.Nested({"first": fields.Str(), "last": fields.Str()})}
        return Response(
            response=json.dumps(parser.parse(args, request)),
            mimetype="application/json"
        )

    @http("POST", "/echo_nested_many")
    def echo_nested_many(self, request):
        args = {
            "users": fields.Nested({"id": fields.Int(), "name": fields.Str()}, many=True)
        }
        return Response(
            response=json.dumps(parser.parse(args, request)),
            mimetype="application/json"
        )

    @http("POST", "/echo_nested_many_data_key")
    def echo_nested_many_with_data_key(self, request):
        data_key_kwarg = {
            "load_from" if (MARSHMALLOW_VERSION_INFO[0] < 3) else "data_key": "X-Field"
        }
        args = {"x_field": fields.Nested({"id": fields.Int()}, many=True, **data_key_kwarg)}
        parsed = parser.parse(args, request)
        return Response(
            response=json.dumps(parsed),
            mimetype="application/json"
        )
