import pytest
from src.http.url import Url
from src.http.parser import Parser
from src.http.serializer import Serializer
from src.http.request import Request
from src.http.response import Response
from src.http.exceptions import ParseError

# --- Тесты Url ---
def test_url_parse_full():
    u = Url("http://example.com:8080/path?q=1")
    assert u.scheme == "http"
    assert u.host == "example.com"
    assert u.port == 8080
    assert u.path == "/path"
    assert u.query == "q=1"

def test_url_default_port():
    u = Url("http://example.com/path")
    assert u.port == 80

def test_url_invalid():
    with pytest.raises(ParseError):
        Url("garbage")

# --- Тесты Parser ---
def test_parse_request():
    data = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    req = Parser.parse_request(data)
    assert req.method == "GET"
    assert req.path == "/"
    assert req.get_header("Host") == "localhost"

def test_parse_request_with_body():
    data = b"POST /echo HTTP/1.1\r\nHost: localhost\r\nContent-Length: 5\r\n\r\nhello"
    req = Parser.parse_request(data)
    assert req.body == b"hello"

def test_parse_request_no_host():
    with pytest.raises(ParseError):
        Parser.parse_request(b"GET / HTTP/1.1\r\n\r\n")

def test_parse_response():
    data = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nhi"
    resp = Parser.parse_response(data)
    assert resp.status == 200
    assert resp.body == b"hi"

# --- Тесты Serializer ---
def test_serialize_request():
    req = Request(method="GET", path="/", headers={"Host": "x"})
    data = Serializer.serialize_request(req)
    assert b"GET / HTTP/1.1" in data
    assert b"Host: x" in data

def test_serialize_response():
    resp = Response(status=200, reason="OK", body=b"hello")
    data = Serializer.serialize_response(resp)
    assert b"HTTP/1.1 200 OK" in data
    assert b"Content-Length: 5" in data