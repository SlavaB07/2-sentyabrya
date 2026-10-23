"""
HttpClient — HTTP-клиент на голых сокетах.
"""

from typing import Dict, Optional

from ..http.url import Url
from ..http.request import Request
from ..http.response import Response
from ..http.parser import Parser
from ..http.serializer import Serializer
from ..http.exceptions import HttpError
from ..net.socket_wrapper import SocketWrapper


class HttpClient:
    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    def set_timeout(self, timeout: float) -> None:
        self.timeout = timeout

    def get(self, url: str,
            headers: Optional[Dict[str, str]] = None) -> Response:
        return self._request("GET", url, headers=headers, body=b"")

    def post(
        self,
        url: str,
        body: bytes = b"",
        content_type: str = "text/plain",
        headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        all_headers = dict(headers or {})
        all_headers["Content-Type"] = content_type
        all_headers["Content-Length"] = str(len(body))
        return self._request("POST", url, headers=all_headers, body=body)

    def _request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        body: bytes = b"",
    ) -> Response:
        parsed = Url(url)

        all_headers = dict(headers or {})
        if "Host" not in all_headers:
            if parsed.port == parsed.DEFAULT_PORTS.get(parsed.scheme):
                all_headers["Host"] = parsed.host
            else:
                all_headers["Host"] = f"{parsed.host}:{parsed.port}"

        all_headers.setdefault("Connection", "close")
        all_headers.setdefault("Accept", "*/*")

        path = parsed.path
        if parsed.query:
            path = f"{path}?{parsed.query}"

        request = Request(
            method=method,
            path=path,
            headers=all_headers,
            body=body)

        response = self._send_and_receive(parsed, request)

        if response.is_error():
            raise HttpError(response.status, response.reason)

        return response

    def _send_and_receive(self, url: Url, request: Request) -> Response:
        if url.scheme == "https":
            raise NotImplementedError("HTTPS пока не поддерживается")

        with SocketWrapper() as sock:
            sock.connect(url.host, url.port, timeout=self.timeout)

            raw_request = Serializer.serialize_request(request)
            sock.send_all(raw_request)

            raw_head = sock.recv_until(b"\r\n\r\n")

            separator = b"\r\n\r\n"
            idx = raw_head.find(separator)
            head_bytes = raw_head[:idx]
            body_bytes = raw_head[idx + len(separator):]

            head_text = head_bytes.decode("latin-1", errors="replace")
            content_length = self._extract_content_length(head_text)
            is_chunked = "transfer-encoding: chunked" in head_text.lower()

            if content_length is not None:
                remaining = content_length - len(body_bytes)
                if remaining > 0:
                    body_bytes += sock.recv_exact(remaining)
                elif remaining < 0:
                    body_bytes = body_bytes[:content_length]

            elif is_chunked:
                body_bytes = self._read_chunked_body(sock, body_bytes)

                # Убираем Transfer-Encoding и ставим Content-Length
                new_head_lines = []
                for line in head_text.split("\r\n"):
                    if line.lower().startswith("transfer-encoding:"):
                        continue
                    if line.lower().startswith("content-length:"):
                        continue
                    new_head_lines.append(line)
                new_head_lines.append(f"Content-Length: {len(body_bytes)}")
                head_text = "\r\n".join(new_head_lines)
                head_bytes = head_text.encode("latin-1")

            else:
                while True:
                    try:
                        chunk = sock.recv(4096)
                        if not chunk:
                            break
                        body_bytes += chunk
                    except Exception:
                        break

            raw_response = head_bytes + separator + body_bytes
            response = Parser.parse_response(raw_response)

            return response

    def _read_chunked_body(self, sock: SocketWrapper,
                           initial_bytes: bytes) -> bytes:
        result = b""
        data = initial_bytes

        while True:
            while b"\r\n" not in data:
                chunk = sock.recv(4096)
                if not chunk:
                    return result
                data += chunk

            size_line, data = data.split(b"\r\n", 1)

            try:
                size = int(size_line, 16)
            except ValueError:
                return result

            if size == 0:
                return result

            while len(data) < size + 2:
                chunk = sock.recv(4096)
                if not chunk:
                    return result
                data += chunk

            result += data[:size]
            data = data[size + 2:]

    @staticmethod
    def _extract_content_length(head_text: str) -> Optional[int]:
        for line in head_text.split("\r\n"):
            if ":" not in line:
                continue
            name, value = line.split(":", 1)
            if name.strip().lower() == "content-length":
                try:
                    return int(value.strip())
                except ValueError:
                    return None
        return None
