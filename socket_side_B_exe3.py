import socket
import protocol_exe3

# IP = '10.0.0.18'
# port = 8820
first = True
server_socket = None
firstt = True


def main():
    while True:
        try:  # Client
            global first
            if first:
                first = False
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip, port = protocol_exe3.get_port()
                if port:
                    my_socket.connect(('10.0.0.18', port))
                else:
                    port = 8820
                    my_socket.connect(('10.0.0.18', port))

            global server_socket
            global firstt
            if firstt is False and server_socket is not None:
                firstt = True
                global k
                k += 1

            firstt = False

            while True:
                print("Side B connecting to port: ", port)

                msg = input("Please enter a message, EXIT to disconnect:\n")
                packet = protocol_exe3.create_msg(msg)
                my_socket.send(packet)
                response = protocol_exe3.get_msg(my_socket)

                if msg == 'EXIT':
                    break
                print(response[1])

                ip, port = protocol_exe3.get_port()
                packet = protocol_exe3.create_msg(str(port))
                my_socket.send(packet)

                print("Side B disconnected")
                my_socket.close()

                ####
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind(("0.0.0.0", port))
                server_socket.listen()
                (client_socket, client_address) = server_socket.accept()
                print("Side B is listening to port: ", port)
                break
                ####


        except:  # server
            while True:
                valid_protocol, msg = protocol_exe3.get_msg(client_socket)
                if valid_protocol:
                    response = "Client sent: " + msg
                    packet = protocol_exe3.create_msg(str(response))
                    client_socket.send(packet)
                    if msg == 'EXIT':
                        break

                    valid_protocol, port = protocol_exe3.get_msg(client_socket)
                    server_socket.close()
                    client_socket.close()

                    ###
                    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    my_socket.connect(("10.0.0.18", int(port)))
                    print("Side B is connecting to port: ", port)
                    break
                    ###

        if msg == 'EXIT':
            break

    print("Closing Connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
