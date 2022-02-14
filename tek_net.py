import csv
import datetime
import logging
import time
import sys
import subprocess
import socket

HOST = '192.168.1.1'  # Your attacking machine to connect back to
PORT = 5025  # The port your attacking machine is listening on

logger = logging.getLogger(__file__)
logging.basicConfig(filename="power.log", filemode='a', level='INFO',
                    format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s',
                    datefmt='%Y-%m-%d, %H:%M:%S')


def connect(host, port):
    go = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    go.connect((host, port))
    return go


def send_rec_tek_command(conn, cmd_string):
    conn.send((cmd_string + "\n").encode())
    dataFromServer = conn.recv(1024)
    return dataFromServer.decode()



def run(args):
    with open(args.csv, 'w') as myfile:
        wrtr = csv.writer(myfile, delimiter=',', quotechar='"')

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
                        # print('data ready')
                        data_ready = True
                    time.sleep(.3)
                # print('reading')
                resp = send_rec_tek_command(go, ":FRD?")
                now = datetime.datetime.now()
                start_time = now.isoformat(sep=' ', timespec='milliseconds')

                wrtr.writerow([start_time, float(resp.strip())])
                # logger.info(f"{start_time},{float(resp.strip())}")
                print(f"{start_time},{float(resp.strip())}")
        except KeyboardInterrupt:
            logger.info('closing connection')
            go.close()
            sys.exit()
        go.close()

def setup_parser(args):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', '-c', help="to write to")

    args = parser.parse_args(args)
    # print(args)
    return args


if __name__ == "__main__":
    args = setup_parser(sys.argv[1:])
    logger.info(f'starting logging to file {args.csv}')
    run(args)

