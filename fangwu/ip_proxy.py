import random

ip_pool = [
    '117.143.109.136:80',
    '39.137.139.26:80',
    '222.74.61.98:53281',
    '60.169.1.145:808',
    # 翻墙代理
    # '127.0.0.1:1080'
]


def ip_proxy():
    ip = ip_pool[random.randrange(0, len(ip_pool))]
    proxy_ip = 'http://' + ip
    proxies = {'http': proxy_ip}
    print(proxies)
    return proxies
