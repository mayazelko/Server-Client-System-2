import socket
import protocol_exe3

IP = '10.0.0.28'
first = True
firstt = True

def main():
    while True:
        try: # server

            global first
            if first:
                first = False
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip, port = protocol_exe3.get_port()
                server_socket.bind(("0.0.0.0", port))
                server_socket.listen()
                print("server is up and running")
                (client_socket, client_address) = server_socket.accept()
                print("side a is listening to port: ", port)

            global firstt
            if firstt is False and client_socket is not None:
                firstt = True
                global k
                k += 1
            firstt = False

            while True:
                valid_protocol, msg = protocol_exe3.get_msg(client_socket)

                if valid_protocol:
                    response = "client sent: " + msg
                    packet = protocol_exe3.create_msg(str(response))
                    client_socket.send(packet)
                    if msg == 'EXIT':
                        break

                    valid_protocol, port = protocol_exe3.get_msg(client_socket)
                    server_socket.close()
                    client_socket.close()

                    ###
                    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    my_socket.connect(('10.0.0.28', int(port)))
                    print("Side A connecting to port: ", port)
                    break
                    ###


        except: # client
            while True:
                msg = input("Please Enter a message, EXIT to disconnect:\n")
                packet = protocol_exe3.create_msg(msg)
                my_socket.send(packet)
                response = protocol_exe3.get_msg(my_socket)

                if msg == 'EXIT':
                    break
                print(response[1])

                ip, port = protocol_exe3.get_port()
                packet = protocol_exe3.create_msg(str(port))
                my_socket.send(packet)

                print("Side A disconnected")
                my_socket.close()

                ###
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind(("0.0.0.0", port))
                server_socket.listen()
                print("server is up and running")
                (client_socket, client_address) = server_socket.accept()
                print("Side A is listening to port: ", port)
                break
                ###

        if msg == 'EXIT':
            break


    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()