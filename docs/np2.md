
# Network Programming, Part 2: Clients

## Getting started with echo client and server
Echo service(well-known port 7)는 client가 보낸 메시지를 그대로 회신하는 sevice다. Client가 connection을 connection 종료를 요청할 때 까지 연결이 지속된다.

### intro/echocli.py:

### intro/echoserv.py:
Server은 두 종류의 socket을 처리해야 한다
- listening socket
  - `listen()`에 의해 listening socket으로 변환된다. Client의 connection request(TCP SYN)를 기다리고, TCP 3-way handshake를 거쳐 connection이 성립된 것이 있으면, 비로소 `accept()`가 return된다. 
  - TCP는 connection queue(size는 `listen()`에서 정의됨)를 생성하여 동시에 여러 connection request에 대해 TCP 처리한다. 그러나 socket API에서는 단순히 `accept()`만 call하면 충분하다. Connection queue가 empty이면, `accept()`는 blocked된다.
- connected socket  
  - `accept()`는 connection이 완료된 socket하나를 client address와 함께 return한다. 이것은 이미 connection이 완료된 socket으로 이를 통해 데이터를 send/recv할 수 있다.
  - 현재 connection이 성립된 client 수 만큼 connected socket object가 생성되고 존재한다.
  
문제점: 
- 동시에 다수의 client에게 service 제공이 불가능하다. 왜냐 하면, Client와의 connection이 끝나야 새로운 client이 connection request를 accept하기 때문. 
- 개선 방향은? client connection을 지원하면서 new connection을 accept할 수 있어야
    1. Mulit-threading
    2. concurrent processing (by folk)
    3. I/O multiplexing (by select)

## Clients의 구현 방식
#### Testing clients with existing echo server
np.hufs.ac.kr에 echo server가 port 7번으로 실행되고 있다. 개발 중인 echo client를 이것과 시험해 보자. `sent_bytes`와 `recv_bytes`는 `send`한 bytes와 `recv`한 bytes를 list로 저장한다.

##### clients/msg.py: a message generator
보낼 메시지('\n'으로 끝남)를 생성해 주는 message generator와 report와 module이 실험에 사용해 보자. (file에서 읽어도 마찬가지다.)

#### clients/client_wrong.py: 잘못된 구현
Q: Report를 보라. Sent bytes와 received bytes가 다른가? 총 sent bytes와 received bytes는?

`send(message)`:
- TCP send buffer(혹은, socket send buffer라고도 칭함)에 message를 저장하라는 뜻
  - blocking socket: message 전체를 성공적으로 저장할 때까지 blocked
  - non-blocking socket: 비어 있는 공간만큼만 저장하고 바로 return(blocking 되지 않는다). 이때, 저장에 성공한 byte 수를 return
- Kernel내에 존재하는 TCP send buffer(혹은, socket send buffer라고도 칭함)에 있는 data를 어떻게 나눠 보낼지는 TCP가 결정한다. 

#### clients/client_shutdown.py: client는 FIN을 보낸 후 남은 회신 메시지를 받을 수 있어야
메시지를 다 보낸 후에도 남아 있는 데이터를 받아야 할 것이다. Socket을 `close`하면 더 이상 데이터 송수신이 불가능하기 때문에 대신, TCP에게 FIN(보내는 방향의 connection 종료) 송신을 요청하기 위해 `shutdown(socket.SHUT_WR)`을 사용한다.

`shutdown`은 반대편 소켓에 대한 권고입니다. 전달하는 인자에 따라, `shutdown(socket.SHUT_WR)`는 《더는 보내지 않을 것이지만, 여전히 들을 겁니다》 나 `shutdown(socket.SHUT_RD)`는 《듣고 있지 않습니다, 즐거웠습니다!》를 뜻할 수 있습니다.
- `shudown` 후 남은 데이터를 수신하는 code를 추가한다.
- FIN이 도착했음을 socket API에서 아는 방법은 `recv`한 데이터가 `b''`(empty bytes)일 때다.
- Echo service는 client가 종료하기 전에 server가 먼저 종료시키면 안되는 프로토콜이다. 하지만, 예외적인 경우로 송신 중에도 언제든지 FIN이 올 수 있다고 가정해서 coding해야 한다. 아래와 같은 비정상 경우에 FIN이 도착한다.
  - Server process가 비정상 종료(exception이 발생했거나 kill 당해서)  
  - Server가 설치된 컴퓨터가 shutdown 중 (OS bug, 정전 또는 운영자에 의해)
  
참고: process가 종료할 때, open한 file과 socket을 close한 후 종료한다.
- main을 call하는 보이지 않는 code가 여러분의 프로그램에 들어 있다. 즉, mother function이 있다. 이것이 OS로 부터 control을 받아 main을 call한다. main에서 `return` 또는 `exit`하면 mother function으로 돌아와 close하지 않은 file이나 socket들을 찾아 `close`해 준다. Process가 kill 당할 때도 미친가지이다. (Programming language에 무관하게) 
- 따라서, 프로그램이 정상 종료될 때에 명시적으로 `close`하지 않아도 자동적으로 `close`된다.

사실, send한 후 recv하는 방식은 특별한 의미를 찾을 수 없다. 왜냐 하면, send한 것이 그대로 돌아와 recv되는 것은 아니기 때문이다. 
의미론적으로 볼 때, echo service에 관한 한, 보내는 byte stream이 어떤 크기의 데이터로 오든 무관하게 byte steam으로 회신되고 최종적으로 이 둘이 같으면 충분하다.

#### clients/client_thread.py: a multi-threading client
송신하는 message들의 stream과 수신하는 message stream을 독립적으로 동시에 처리하는 방법을 생각해 보자. 
먼저 thread를 활용해서 구현해 보자. 

양방향의 stream에 대해 전담하는 sending 측과 receiving 측 function을 작성하고, 이들이 다른 thread로 실행시키면 해결할 수 있을 것이다.  

> See [threading — Manage Concurrent Operations Within a Process](https://pymotw.com/3/threading/index.html)

#### clients/client_select.py: an I/O multiplexing client
File이나 socket 여러 개를 동시에 handling할 수 있게, 다시 말해, I/O를 multiplexing하도록 coding이 가능하다. 먼저, socket을 non-blocking mode로 바꾼다.
```Python
sock.setblocking(False)
```

Non-blocking socket에 대해서는 blocking 될 수 있는 socket API들(send, recv, connect, accept 등)을 call하면 바로  return되기 때문에, socket이 readable이나 writable이 될 때를 기다리고(`select`) 이들을 사용해야 한다. Socket receive buffer에 읽을 것이 있으면(1 byte 이상) 있으면 *readable*, socket send buffer가 full이 아니면 *writable*이라 한다.

사용할 platform에 적절한 selector를 선택하고, 어떤 socket이 readable/writable을 check할 event를 등록한다. 아래는 readable과 writable event 두 가지를 등록한다. (Bit로 표현된다. 아래는 bit-wise OR로 두 가지를 등록)
```Python
import selectors
sel = selectors.DefaultSelector()  # choose a selector suitable for this platform
sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE) 
```

그 다음, event가 발생할 때까지 대기해야 한다. Event는 동시에 하나 이상 발생 가능하다. `timout` 파라미터를 주면, timout event도 기다릴 수 있다.
```Python
events = sel.select(timeout=1)
```

EVENT_READ, EVENT_WRITE, timeout event 중 어느 하나 또는 여러가지가 발생할 수 있으며, 이때 `select` 문이 return 된다. Return되는 object는 [(key, mask), ...] list type이다. Timeout이 발생했을 때, empty list `[]`가 return된다. (참고: timeout을 정의하지 않으면, event가 발생하지 않으면 계속 blocked된다. Blocked에서 깨어 났을 때야 비로소 외부에서 발생된 예외들(socket error나 process kill 등)을 잡을 수 있는 platform도 있기 때문에, timeout을 설정해서 주기적으로 깨어나게 함이 바람직하다.)  
```Python
for key, mask in events:
    conn = key.fileobj

    if mask & selectors.EVENT_READ:  # readable
        # recv 처리
    if mask & selectors.EVENT_WRITE: # writable
        # sendall 처리
```

> 주의: 두번 째 `if` 문은 `elif` 문이 아니어야 한다. 왜냐 하면, mask에 기록된 발생한 event가 여럿일 때 차례로 처리해야 하기 때문이다.

> 참고: `sock.sendall(message)`: non-blocking socket에 대해서도 loop을 돌며 확실하게 전부를 저장

#### 메시지간에 경계를 설정했다면,
이상의 client들은 메시지 간에 경계가 없다. (사실, echo service는 반드시 메지지 경계가 있을 필요가 없다.)
이어지는 메시지 사이에 경계가 있다면, 메시지 단위로 송신하고 수신해야 한다. 왜냐 하면, 메시지 하나를 끝까지 받아야 해석할 수 있기 때문이다. 

TCP 원천적으로 byte stream을 전달하는 목적으로 설계되었기 때문에 메시지 간의 경계가 없다. (이것이 장점이기도 하다.) 그러나, programming language에서 statement 간에 `;` 나 new line으로 경계를 표시하듯, marker를 정의하면, 수신 stream에서 하나의 메시지를 완성하며 꺼낼 수 있겠다.

많은 경우 LF(`'\n'`), CRLF(`'\r\n'`)를 경계 marker로 사용할 수 있다. HTTP 경우 빈 줄, 즉 두개의 CRLF를 HTTP message 경계로 삼는다.

> 참고: UDP protocol은 datgram이라는 단위로 송수신하기 때문에 메시지 경계가 있다. UDP socket을 이용하면 메시지 단위의 송수신이 가능하다.

#### clients/client_makefile.py: using file-like objects
Client가 송신할 request messge와 서버가 회신하는 response message의 경계 마커로 LF를 사용하기로 하자. 수신 메시지를 분리해 내기 위해서는 buffering 해야 LF 문자까지의 한 line을 가져올 수 있다. Socket을 file-like object로 변환하면, `read(), write()` 등의 file method를 사용할 수 있다. Socket은 양방향 통신이니 read mode, write mode 두 가지의 file-like object를 생성할 수 있다.

```Python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('np.hufs.ac.kr', 7))
rfile = sock.makefile('rb')
wfile = sock.makefile('wb')
print(type(rfile), type(wfile))
```

여기서는 write 대신 그냥 send를 사용하는 편이 낫다.
- write 한 후 buffer를 flush하지 않으면 buffering된 채 송신이 미뤄질 수 있다. Server에게 송신하지 않으면, 수신할 것도 없을 것이다. --> wait forever

> 주의: Non-blocking socket에 대해 makefile 해서는 안된다.

#### clients/client_class.py:  client_makefile.py의 class 버전

#### clients.py: run multiple clients with multi-threading
Suclassing으로 thread 구현한다.
- `Client` class instance 마다 data attributes 별도 저장함
- `run` method가 thread target function임
- OO approach: run method만 overloading하면 다른 client 구현 가능

Multi-threading으로 여러개의 client의 concurrent execution이 가능하다. main code에서 여러 `Client` object을 instantiate하고 thread를 실행시키고 있다.  

앞으로 server측 개발에서 시험용으로 사용될 프로그램이다.

> Usage: `clients.py` host:port \[n\]<br>
>- n: number of clients (3 in default)
