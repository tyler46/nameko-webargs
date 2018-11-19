# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io

import pytest
from webargs.core import MARSHMALLOW_VERSION_INFO

from tests.apps.nameko_app import AppService


@pytest.fixture
def web_session(container_factory, web_config, web_session):
    container = container_factory(AppService, web_config)
    container.start()
    return web_session


def test_echo_use_args_validated(web_session):
    res = web_session.get("/echo_use_args_validated", params={"value": 44})
    assert res.json() == {"value": 44}


def test_echo_use_kwargs(web_session):
    res = web_session.get("/echo_use_kwargs", params={"name": "John"})
    assert res.json() == {"name": "John"}


def test_echo_multi(web_session):
    res = web_session.get("/echo_multi", params={"name": ["John", "Perry"]})
    assert res.json() == {"name": ["John", "Perry"]}


def test_echo_many_schema(web_session):
    res = web_session.post("/echo_many_schema", json=[{"name": "John"}, {"name": "Tom"}])
    assert res.json() == [{"name": "John"}, {"name": "Tom"}]


def test_echo_use_args_with_path_param(web_session):
    res = web_session.get("/echo_use_args_with_path_param/john", params={"value": 4})
    assert res.json() == {"value": 4}


def test_echo_use_kwargs_with_path_param(web_session):
    res = web_session.get("/echo_use_kwargs_with_path_param/john", params={"value": 4})
    assert res.json() == {"value": 4}


def test_error(web_session):
    res = web_session.get("/error", params={"text": "foo"})
    assert res.status_code == 422
    assert res.json()['error'] == "UNPROCESSABLE_ENTITY"


def test_echo_headers(web_session):
    res = web_session.get("/echo_headers", headers={"name": "lengthok"})
    assert res.json() == {"name": "lengthok"}


def test_echo_cookies(web_session):
    res = web_session.get("/echo_cookie", cookies={"name": "lengthok"})
    assert res.json() == {"name": "lengthok"}


def test_echo_file(web_session):
    res = web_session.post("/echo_file", files={"myfile": io.BytesIO(b"data")})
    assert res.json() == {"myfile": "data"}


def test_echo_nested(web_session):
    res = web_session.post("/echo_nested", json={"name": {"first": "Joel", "last": "Embiid"}})
    assert res.json() == {"name": {"first": "Joel", "last": "Embiid"}}


def test_echo_nested_many(web_session):
    res = web_session.post(
        "/echo_nested_many",
        json={
            "users": [
                {"id": 21, "name": "Embiid"},
                {"id": 25, "name": "Simmons"}
            ]
        })
    assert res.json() == {"users": [{"id": 21, "name": "Embiid"}, {"id": 25, "name": "Simmons"}]}


def test_echo_nested_many_data_key(web_session):
    res = web_session.post("/echo_nested_many_data_key", json={"x_field": [{"id": 21}]})
    if MARSHMALLOW_VERSION_INFO[0] < 3:
        assert res.json() == {"x_field": [{"id": 21}]}

    res = web_session.post("/echo_nested_many_data_key", json={"X-Field": [{"id": 21}]})
    assert res.json() == {"x_field": [{"id": 21}]}

    res = web_session.post("/echo_nested_many_data_key", json={})
    assert res.json() == {}
