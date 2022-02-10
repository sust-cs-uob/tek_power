import time
import sys
import subprocess
import socket


HOST = '192.168.1.1'    # Your attacking machine to connect back to
PORT = 5025           # The port your attacking machine is listening on


def connect(host, port):
   go = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   go.connect((host, port))
   return go


def send_rec_tek_command (conn, cmd_string):
    
    conn.send((cmd_string + "\n").encode())
    dataFromServer = conn.recv(1024)
    return dataFromServer.decode()

def tek_connect():
    data = ":SEL:CLR\n"
    data = ":SEL:WAT\n"
    data = ":FRD?\n"
    so.send(data.encode())
    dataFromServer = so.recv(1024)
    print(dataFromServer.decode())

def wait(go):
    data = go.recv(1024)
    if data == "exit\n":
        go.close()
        sys.exit(0)
    elif len(data) == 0:
      return True


def run():
    print('test')
    go = connect(HOST, PORT)

    while True:
        data_ready = False
        while not data_ready:
            resp = send_rec_tek_command(go, ":DSR?")
            print(resp)
            if resp == "2":
                data_ready = True
            time.sleep(.1)
        resp = send_rec_tek_command(go, ":FRD?")
        print(resp)

    return 0

def main(): 
    while True:
        dead = False
        try:
            go = connect((HOST, PORT)) 
            while not dead:
                dead = wait(go) 
            go.close()
        except socket.error:
            pass
        time.sleep(2)


if __name__ == "__main__":
#    sys.exit(main())
    sys.exit(run())

