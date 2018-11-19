"""A simple number and datetime addition JSON API.
Run the app:

    $ env $(cat .env | grep "^[^#;]" | xargs) ./run.sh

Try the following with httpie (a cURL-like utility, http://httpie.org):

    $ pip install httpie
    $ http GET :8000/
    $ http GET :8000/ name==Ada
    $ http POST :8000/add x=40 y=2
    $ http POST :8000/dateadd value=1973-04-10 addend=63
    $ http POST :8000/dateadd value=2014-10-23 addend=525600 unit=minutes
"""
import datetime as dt
import json

from webargs import ValidationError as WebArgsValidationError
from werkzeug.wrappers import Response

from nameko_webargs.namekoparser import use_args, use_kwargs

from echoapp.entrypoints import http
from echoapp.schemas import hello_args, add_args, dateadd_args


class Service:
    name = "http_service"

    @http("GET", "/", expected_exceptions=WebArgsValidationError)
    @use_args(hello_args)
    def index(self, request, args):
        """A welcome page.
        """
        return Response(
            json.dumps({"message": "Welcome, {}!".format(args["name"])}),
            mimetype='application/json'
        )

    @http("POST", "/add", expected_exceptions=WebArgsValidationError)
    @use_kwargs(add_args)
    def add(self, request, x, y):
        """An addition endpoint."""
        return Response(
            json.dumps({"result": x + y}),
            mimetype='application/json'
        )

    @http("POST", "/dateadd", expected_exceptions=WebArgsValidationError)
    @use_kwargs(dateadd_args)
    def dateadd(self, request, value, addend, unit):
        """A date adder endpoint."""
        value = value or dt.datetime.utcnow()
        if unit == "minutes":
            delta = dt.timedelta(minutes=addend)
        else:
            delta = dt.timedelta(days=addend)
        result = value + delta
        return Response(
            json.dumps({"result": result.isoformat()}),
            mimetype='application/json'
        )
