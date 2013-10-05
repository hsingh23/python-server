#!/usr/bin/python

from sys import argv, exit
from getopt import getopt, GetoptError
import socket
from re import findall as re_findall, I
# from json import dumps
from random import randrange
import Queue
import threading

FILES = {}


class ServeRequest(threading.Thread):

    """Threaded Request Server"""

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def compose_message(s, file_path):
        if file_path in FILES:
            return "HTTP 200 OK\r\nContent-Length: %d\r\n\r\n%s"\
                % FILES[file_path]
        else:
            return "HTTP 404 Not Found\r\n\r\n"

    def run(self):
        while True:
            # grabs host from queue
            new_file_discriptor = self.queue.get()
            try:
                header = new_file_discriptor.recv(4096)\
                    .partition("\r\n\r\n")[0]
                # header_list = dict(re_findall(r"(?P<name>.*?): \
                # (?P<value>.*?)\r\n", header))
                file_path = re_findall(r"^GET (/.*) HTTP", header, I)[0]
                new_file_discriptor.sendall(self.compose_message(
                    "."+file_path))
            except Exception as e:
                new_file_discriptor.sendall("HTTP 400 Bad Request\r\n\r\n%s" % e)
            finally:
                new_file_discriptor.close()
            self.queue.task_done()


def get_port(argv):
    try:
        opts, args = getopt(argv, "hp:", ["help", "port="])
    except GetoptError:
        print 'python server.py -p 9000 or python server.py --port 9000'
        exit(2)

    port = -1
    for opt, arg in opts:
        if opt in ['-h', "help"]:
            print 'Try python server.py -p 9000 or \
                    python server.py --port 9000'
            exit(2)
        elif opt in ("-p", "--port"):
            port = int(arg)
    if port == -1:
        print "You didn't give a port, I'll start it up on on a random port"
        port = randrange(4000, 65535)
    print 'Starting server on port %s' % (port)
    return port


def socket_bind_listen(PORT):
    HOST = ''
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print 'Socket created'
    try:
        my_socket.bind((HOST, PORT))
    except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        exit()
    print 'Socket bind complete'
    my_socket.listen(10)
    print 'Socket now listening'
    return my_socket


def load_all_files_in_ram():
    from os.path import join
    from os import walk

    def load_file(file_path):
        with open(file_path, "r") as f:
            x = f.read()
            FILES[file_path] = (len(x), x)

    files = []
    for root, dirnames, filenames in walk('.'):
        for filename in filenames:
            files.append(join(root, filename))

    threads = []
    for f in files:
        t = threading.Thread(target=load_file, args=(f,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def main(argv):
    s = socket_bind_listen(get_port(argv))
    load_all_files_in_ram()
    queue = Queue.Queue()

    # spawn a pool of threads, and pass them queue instance
    for i in range(100):
        t = ServeRequest(queue)
        t.setDaemon(True)
        t.start()

    while 1:
        # wait to accept a connection - blocking call
        try:
            new_file_discriptor, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            queue.put(new_file_discriptor)
        except (KeyboardInterrupt, SystemExit):
            print "Bye"
            break
    s.close()
    queue.join()

if __name__ == "__main__":
    main(argv[1:])
