#!/usr/bin/env python3
# 登陆淮阴工学院上网认证系统
import requests
userName=input("Your userName: ")
pwd=input("Your password: ")
rememberPwd=input("Whether Remember login status? (1=true,0=false): ")
post_url='http://172.16.5.73/portal/login.php'
post_data={
    'opr':'pwdLogin',
    'userName':userName,
    'pwd':pwd,
    'rememberPwd':rememberPwd
}
res=requests.post(post_url,data=post_data)
print(res.text)
