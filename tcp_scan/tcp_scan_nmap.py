# coding: utf-8

import optparse
from nmap import PortScanner
import json


def nmapScan(tgtHost, tgtPort):
    nmScan = PortScanner()
    result = nmScan.scan(tgtHost, tgtPort)
    print json.dumps(result, indent=4)
    state = result['scan'][tgtHost]['tcp'][int(tgtPort)]['state']
    print 'Host:', tgtHost, 'Port:', tgtPort, 'State:', state


def main():
    parser = optparse.OptionParser('usage %prog -H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port')
    (options, args) = parser.parse_args()
    print options, args
    tgtHost = options.tgtHost
    tgtPort = options.tgtPort
    args.append(tgtPort)

    if tgtHost == None or tgtPort == None:
        print 'You must specify a target host and port'
        return

    for port in args:
        nmapScan(tgtHost, port)


if __name__ == '__main__':
    main()
