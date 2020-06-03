import socket
import logging
from urllib.request import urlparse
from urllib.parse import urlencode
from requests.structures import CaseInsensitiveDict
import json

# logging.basicConfig(level=logging.DEBUG)


class Request:
    def __init__(self, method, url, data=None, headers=None):
        """Request objects
        :param method: an HTTP method
        :param url: a full URL including query string if needed
        :param data: data to be sent in the body of POST request
        :param headers: dict representing headers. Case-insensitive
                    Content-Type header should be given at least if data exists
        """

        self.method = method.upper()
        self.url = url
        if self.method == 'GET':
            self.data = None
        elif self.method == 'POST':
            self.data = data
        else:
            raise NotImplementedError('{}: unknown method'.format(self.method))

        r = urlparse(self.url)
        if r.scheme not in ('http', ):
            raise NotImplementedError('{}: not supported'.format(r.scheme))
        self.hostname = r.hostname
        self.port = r.port if r.port else 80

        # set request path
        self.path = r.path or '/'
        # append params and query to path if exist
        if r.params:
            self.path += ';' + r.params
        if r.query:
            self.path += '?' + r.query

        # make headers
        self.headers = CaseInsensitiveDict()
        self.headers['Host'] = self.hostname
        self.headers['Agent'] = 'httpcli'
        self.headers['Accept'] = '*/*'
        self.headers['Connection'] = 'keep-alive'
        if headers:
            for key, value in headers.items():
                self.headers[key] = value
        if self.data:   # for PUT method
            if not self.headers.get('content-type', None):
                raise ValueError('No Content-type header specified')
            self.headers['content-length'] = str(len(self.data))

    def open(self):
        """Open an HTTP session. Then, send/receive request/response.
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.hostname, self.port))
        self.file = file = self.sock.makefile('rwb')

        headers_list = [key + ': ' + value for key, value in self.headers.items()]
        headers_str = '\r\n'.join(headers_list) + '\r\n'
        template = '{method} {path} HTTP/1.1\r\n{headers}\r\n'
        message = template.format(method=self.method,
                                path=self.path, headers=headers_str)
        logging.debug('Request message:\n{}'.format(message))
        file.write(message.encode('utf-8'))
        if self.data:
            file.write(self.data.encode('utf-8'))
        file.flush()

        response = Response(self)
        # read status line
        response.status_code = response.read_status()
        logging.debug('status code: {}'.format(response.status_code))
        # read headers
        response.read_headers()
        logging.debug('Response headers:\n{}'.format(response.headers))

        # read contents
        response.read_content()
        if response.status_code >= 400:             # HTTP error response
            logging.warning(response.content)
        return response

    def close(self):
        """Close this HTTP session
        """
        if not self.sock._closed:
            self.file.close()
            self.sock.close()


class Response:
    def __init__(self, request):
        """Response object corresponding to the request object
        """
        self.request = request
        self.status_code = None
        self.content = bytearray()
        self.headers = CaseInsensitiveDict()

    def read_status(self):
        return int(self.request.file.readline().decode('utf-8').split()[1])

    def read_headers(self):
        for line in self.request.file:
            if line == b'\r\n':  # end of headers
                break
            header = line.decode().strip()  # remove leading and trailing white spaces
            key, value = header.split(':', maxsplit=1)
            self.headers[key] = value.strip()

    def read_content(self):
        file = self.request.file
        ## Content-length specified:
        if self.headers.get('Content-length', None):  # Content-length header exists
            self.content = file.read(int(self.headers['Content-length']))
        ## Chunked transfer specified: chunk represented as hexa string + CRLF
        elif self.headers.get('Transfer-Encoding', None) == 'chunked':  # chunked transfer
            while True:
                content_length = int(file.readline().decode('utf-8').strip(), 16)
                if content_length == 0:
                    break
                chunk = file.read(content_length)
                self.content.extend(chunk)
                file.readline()
            file.readline()  # skip CRLF
        ## nothing specified:
        else:
            self.content = file.read()  # read until FIN arrival


def get(url, params=None):
    """Send an HTTP GET request and receive its response.

    :param url: URL for the new :class: Request object
    :param params: dict to be sent in the query string for the :class:`Request`.
    """

    if params:
        url += '?' + urlencode(params)
    request = Request('GET', url)
    return request.open()

def post(url, data=None, json_data=None):
    """Send an HTTP POST request and receive its response.

    :param url: URL for the new :class: Request object
    :param data: dict for form data to be sent in the body of the request
    :param json_data: dict for JSON data sent in the body of the request
    Note: both of data and json_data cannot be given
    """

    if json_data:
        request = Request('POST', url, data=json.dumps(json_data),
                          headers={'Content-Type': 'application/json'})
    elif data:
        request = Request('POST', url, data=urlencode(data),
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
    else:
        raise ValueError('No body to send')
    return request.open()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # GET method - chunked transfer
    url = 'http://mclab.hufs.ac.kr/wiki/Lectures/IA/2019#Python_Network_Programming'
    # url = 'http://localhost:8080/test/index.html'
    response = get(url)
    print('Content:')
    print(response.content[:400])

    # Test POST method with JSON data
    url = 'http://httpbin.org/post'     # simple HTTP Request & Response Service.
    sensor_data = {
        "deviceid": "iot123",
        "temp": 54.98,
        "humidity": 32.43,
        "coords": {
            "latitude": 47.615694,
            "longitude": -122.3359976,
        },
        "organization": "한국외대"
    }
    response = post(url, json_data=sensor_data)
    # end of POST
    print('content:')
    print(response.content)
    if response.headers.get('content-type') == 'application/json':
        text = json.loads(response.content.decode('utf-8'))
        print('decoded json content:')
        print(text)
