import requests
import openpyxl
from requests_toolbelt import MultipartEncoder

file='../省内不限量外呼分配4.19.xlsx'
sheet='2015年以后'
login_data={'operator_id':'Account','password':'Password'}

# API of website
get_cookies_url='http://183.207.196.70:8085/haywdjpt/login!login.jspa'
post1_referer_url='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!checkYwMsisdn.jspa'
post2_referer_url='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!saveLogin.jspa'
test_login='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!frame.jspa'

# open the excel
wb=openpyxl.load_workbook(filename=file)
sheet_ranges=wb[sheet]

# login in
multiFormData=MultipartEncoder(fields=multiFiles)
session=requests.session()
session.post(get_cookies_url,data=login_data)
    
for i in range(898,1123):
    phoneNumber=str(sheet_ranges['A'+str(i)].value)
    
    paramater={'msisdn':phoneNumber,'yw_id':'1761','bl_time':'2018-05-07'}
    multiFiles={
            'region_id':'1210',
            'school_id':'295',
            **paramater,
            'fzr_id':login_data['operator_id'],
            'fzr_name':login_data['operator_id']
        }

    res=session.post(post1_referer_url,data=paramater)
    if res.text=='0':
        res=session.post(post2_referer_url,data=multiFormData,headers={'Content-Type':multiFormData.content_type})
    print(res.text)
