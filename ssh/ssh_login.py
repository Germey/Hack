# coding=utf-8

import pexpect

PROMPT = ['#', '>>>', '>', '\$']

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)

def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connStr)
    #print('[+] %s' %(child))
    print('[+] Attempt Once')
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    print ret
    if ret == 0:
        print('[-] Error Connecting')
        return
    if ret == 1:
        print('[+] Confirm Connecting')
        child.sendline('yes')
    if ret == 2:
        child.sendline(password)
        print('[+] Sending Password')
    print(child)
    ret = child.expect(['Welcome'])
    if ret == 0:
        child.expect(PROMPT)
        return child


def main():
    host = '115.28.24.44'
    user = 'root'
    password = ''
    print('[+] Start to connect')
    child = connect(user, host, password)
    if child:
        print('[+] Connect Successfully')
        send_command(child, 'cat ~/.bash_history')
    else:
        print('[-] Connect failed')


if __name__ == '__main__':
    main()