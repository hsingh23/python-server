#!/usr/bin/python

from sys import argv, exit
import getopt
import socket
from re import findall as re_findall

DATA_SIZE = 4096


def get_domain_port_file(argv):
    help = """To set host, type --domain=localhost or -d localhost
                To set port, type --port=9000 or -p 9000
                To set file, type --file=9000 or -f 9000
                Try python client.py -d localhost -p 9000 -f 1b"""
    try:
        opts, args = getopt.getopt(
            argv, "hd:p:f:", ["help", "domain=", "port=", "file="])
    except getopt.GetoptError:
        print help
        exit(2)
    host, filename, port = (-1,) * 3
    for opt, arg in opts:
        if opt in ['-h', "help"]:
            print help
            exit(2)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-d", "--domain"):
            host = arg
        elif opt in ("-f", "--file"):
            filename = arg
    if -1 in [host, filename, port]:
        print "OI! You didn't supply one of the required values!!!!"
        print help
        exit(2)
    return host, port, filename


def setup_socket(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create setup_socket'
        exit()
    print 'Socket Created'
    try:
        remote_ip = socket.gethostbyname(host)

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        exit(-1)

    s.connect((remote_ip, int(port)))
    print 'Socket Connected to ' + host + ' on ip ' + remote_ip
    return s


def ask_for_file(s, filename):
    from re import sub as re_sub
    filename = re_sub(r"^[(\.\./)|(\./)|(/)]+", "/", filename)
    message = "GET /%s HTTP1.1\r\n\r\n" % filename
    try:
        s.sendall(message)
    except socket.error:
        print 'Send failed'
        exit(-1)
    print 'Message send successfully'


def get_file(s):
    data = s.recv(DATA_SIZE)
    header, _, reply = data.partition("\r\n\r\n")
    header_list = dict([(x.lower(), y)
                       for (x, y) in re_findall("(.*):\s+?(.*)", header)])
    content_length, recieved_so_far = int(header_list['content-length']), len(reply)
    while content_length > recieved_so_far:
        reply += s.recv(DATA_SIZE)
        recieved_so_far = len(reply)
    print reply
    s.close()


def main(argv):
    host, port, filename = get_domain_port_file(argv)
    s = setup_socket(host, port)
    ask_for_file(s, filename)
    get_file(s)


if __name__ == "__main__":
    main(argv[1:])
