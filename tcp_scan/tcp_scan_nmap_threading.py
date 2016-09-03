# coding=utf-8
import json
import optparse
import socket
import threading
from nmap import PortScanner
from urlparse import urlparse

lock = threading.Semaphore(value=1)
open_ports = []
closed_ports = []

def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


def get_host_path(des):
    return urlparse(des, scheme='http').path


def get_host_name(ip):
    try:
        return socket.gethostbyaddr(ip)
    except socket.herror:
        print '[-] Unknown host name'


def get_ip(des):
    if not valid_ip(des):
        try:
            ip = socket.gethostbyname(get_host_path(des))
            return ip
        except socket.error:
            print '[-] Errors occur when getting ip'
            exit(0)
    else:
        return des


def nmap_scan(ip, port):
    global lock
    try:
        nmap_scanner = PortScanner()
        result = nmap_scanner.scan(ip, str(port))
        state = result['scan'][ip]['tcp'][int(port)]['state']
        lock.acquire()
        print '[+][', port, '], IP:', ip, 'Port:', port, 'State:', state
        print '[+]', result['scan'][ip]['tcp'][int(port)]
        if state == 'open':
            open_ports.append(port)
        else:
            closed_ports.append(port)
    except Exception, e:
        lock.acquire()
        print '[-] IP:', ip, 'Port:', port, 'Errors occur when scanning', e.message
        closed_ports.append(port)
    finally:
        lock.release()


def parse_args():
    usage = 'Nmap Ports Scanner of Host'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-d', '--des', dest='des', type='string', help='specify a target destination')
    parser.add_option('-p', '--ports', dest='ports', type='string', help='specify target ports')
    (options, args) = parser.parse_args()
    des = options.des
    if des == None:
        print('[-] You must specify a destination')
        exit(0)
    if options.ports == None:
        ports = range(25)
    else:
        args.append(options.ports)
        ports = args
    print des, ports
    return des, ports


def main():
    threads = []
    (des, ports) = parse_args()
    for port in ports:
        ip = get_ip(des)
        threads.append(threading.Thread(target=nmap_scan, args=(ip, port)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print '[+] Scan finished'
    print '[+] Open Ports', open_ports
    print '[+] Closed Ports', closed_ports

if __name__ == '__main__':
    main()
