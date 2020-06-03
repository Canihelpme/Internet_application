def parse_headers(rfile):
    """Read from rfile and parse header lines
    :param rfile: input file-like object
    :returns:     parsed header dict
                  (Keys in the dict are capitalized for convention)
    """

    headers = {}
    for line in rfile:
        if line == b'\r\n':
            return headers
        header = line.decode().strip()  # remove leading and trailing white spaces
        key, value = header.split(':', maxsplit=1)
        key, value = key.strip().capitalize(), value.strip()
        headers[key] = value
    return headers


def to_bytes(headers):
    """Convert headers dict into plain bytes separated by CRLF
    :param headers: header dict
    :returns:       bytes
    """

    lines = [key + ": " + value for key, value in headers.items()]
    text = "\r\n".join(lines) + "\r\n\r\n"
    return text.encode()


# Tester
if __name__ == '__main__':
    # read request message from an HTTP client
    import io

    request_msg = b'''GET /test/index.html HTTP/1.1\r
host: mclab.hufs.ac.kr\r
CONNECTION: close\r
\r
'''
    file = io.BytesIO(request_msg)
    status = file.readline()  # read status line
    request_headers = parse_headers(file)
    print(request_headers)

    # Build response headers
    headers = {
        'Date': 'Thu, 27 Sep 2018 04:25:01 GMT',
        'Server': 'Apache/2.2.22 (Ubuntu)',
        'Last-modified': 'Tue, 19 Sep 2017 06:13:15 GMT',
        'Etag': '"1e982f-569-55984c1337a5f"',
        'Accept-ranges': 'bytes',
        'Vary': 'Accept-Encoding',
        'Connection': 'close',
    }
    headers['Content-type'] = 'text/html'
    headers['Content-lenght'] = '1385'
    header_lines = to_bytes(headers)
    print()
    print(header_lines)