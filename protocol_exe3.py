PORT = 8820
import socket
first = True

def get_port():
    global first
    print(first)
    if first:
        first = False
        return '_____', 8820
    ip = socket.gethostbyname(socket.gethostname())
    for port in range(65535):
        try:
            serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv.bind((ip, port))
            serv.connect((ip, port))
            serv.close()
            return ip, port
        except:
            pass


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """

    length = str(len(data))
    zfill_length = length.zfill(4)
    data = zfill_length + str(data)

    return data.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """

    length = my_socket.recv(4).decode()
    data = my_socket.recv(int(length)).decode()

    return True, data
