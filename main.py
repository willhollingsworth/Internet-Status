import subprocess
import os
import time
from collections import defaultdict

def run(cmd):
    cmd = cmd.split()
    completed = subprocess.run(cmd, capture_output=True,encoding="utf-8")
    return completed

def get_default_gateway() -> str:
    ip_conf = run('ipconfig').stdout
    for x in ip_conf.split('\n'):
        if 'Default Gateway' in x:
            if ip:=x.split('. : ')[1]:
                return ip
    return ''

def ping_ip(ip:str) -> list[str, str]:
    output = run(f'ping {ip} -n 1').stdout.split('\n')
    if len(output) > 2:
        return [ip] + parse_reply_str(output[2])

def parse_reply_str(str) -> list[str, str]:
    ip = str.split(':')[0].split()[2]
    latency = str.split('time=')[1].split('ms')[0]
    return [ip,latency]

def multi_ping(ip:str,count=5,interval=1):
    latency_responses = []
    for i in range(count):
        latency_responses.append(ping_ip(ip)[2])
        time.sleep(interval)
    return latency_responses

def multi_host_ping(hosts):
    responses = defaultdict(list)
    for i in range(3):
        for ip in hosts:
            responses[ip].append(ping_ip(ip)[2])
        time.sleep(.3)
    return responses

def clear_screen() -> None:
    os.system('cls')

def print_responses(responses) -> None:
    for host,responses in responses.items():
        print(host,end=': ')
        for response in responses:
            print(response,end=' ')
            # ...
        print()

def print_mockup() -> None:
    print('''
                last 5                  total
                avg    loss   jitter    avg    packetloss   jitter
    Gateway     2      0%      3        4      3%               2
    Google      30     5%      4        35     5%               6
        
    gateway - 2  2  3  2  3  4  2 
    google  - 30 30 30 31 33 30 29

        ''')
    
def main():
    google = 'www.google.com'
    def_gate = get_default_gateway()
    hosts = [google,def_gate]
    responses = multi_host_ping(hosts)
    print_responses(responses)


if __name__ == '__main__':
    main()
    # print_mockup()
    # clear_screen()
