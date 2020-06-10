import time

def msgs(n, length=1000):
    """Generate n messages of length ending with new line char
    including extra delay in seconds
    """

    if length < 6:
        length = 6
    msg = bytearray(b'00000' + (length-6) * b'a' + b'\n')

    for i in range(1, n+1):
        msg[:5] = b'%5.5d' % i
        yield msg

def report(n_sent, n_rcvd):
    """Print report on sent/received msgs
    """

    delta = len(n_sent) - len(n_rcvd)
    if delta > 0:
        n_rcvd.extend([0 for i in range(delta)])
    elif delta < 0:
        n_sent.extend([0 for i in range(-delta)])
    print(' n   sent  rcvd')
    print('---------------')
    for e in enumerate(zip(n_sent, n_rcvd)):
        print(e)
    print('total', (sum(n_sent), sum(n_rcvd)))

if __name__ == '__main__':
    # Can be used as iterable objects with next()
    it = iter(msgs(20, length=2000))
    while True:
        try:
            print(next(it))
        except StopIteration:
            break