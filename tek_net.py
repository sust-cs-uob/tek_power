import time
import sys
import subprocess
import socket

HOST = '192.168.1.1'  # Your attacking machine to connect back to
PORT = 5025  # The port your attacking machine is listening on


def connect(host, port):
    go = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    go.connect((host, port))
    return go


def send_rec_tek_command(conn, cmd_string):
    conn.send((cmd_string + "\n").encode())
    dataFromServer = conn.recv(1024)
    return dataFromServer.decode()



def run():
    # print('test')
    go = None
    try:
        go = connect(HOST, PORT)

        send_rec_tek_command(go, ":SEL:CLR")
        send_rec_tek_command(go, ":SEL:WAT")
        send_rec_tek_command(go, ":DSE 2")
        while True:
            data_ready = False
            while not data_ready:
                resp = send_rec_tek_command(go, ":DSR?")
                # print(resp)
                if int(resp.strip()) == 2:
                    print('data ready')
                    data_ready = True
                time.sleep(.05)
            # print('reading')
            resp = send_rec_tek_command(go, ":FRD?")
            print(resp)
    except KeyboardInterrupt:
        print('closing connection')
        go.close()
        sys.exit()
    go.close()

if __name__ == "__main__":

    run()

