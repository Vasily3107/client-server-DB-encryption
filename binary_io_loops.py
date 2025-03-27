from socket import socket



ITERATION_END_SIGNAL = b'looprecv_end_iteration'



def loopsend(connection: socket, binary_data: bytes, packet_len: int = 1024) -> None:

    for i in range(0, len(binary_data), packet_len):

        packet = binary_data[i : i + packet_len]

        connection.sendall(packet)

    connection.sendall(ITERATION_END_SIGNAL)



def looprecv(connection: socket, packet_len: int = 1024) -> bytes:
    binary_data = b''

    while True:
        packet = connection.recv(packet_len)
            
        if not packet or packet == ITERATION_END_SIGNAL: break

        binary_data += packet

    return binary_data