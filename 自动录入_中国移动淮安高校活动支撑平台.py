import requests
import openpyxl
from requests_toolbelt import MultipartEncoder

file='excel file'
sheet='Sheet1'

#读取Excel
def excel_data(file,sheet):
    wb=openpyxl.load_workbook(filename=file)
    sheet_ranges=wb[sheet]
    return(sheet_ranges)

for i in range(2,32):
    excel=excel_data(file,sheet)
    if(excel['F'+str(i)].value in ['√']):
        phoneNumber=str(excel['C'+str(i)].value)
        print(phoneNumber)
    else:
        continue
    
    paramater={'msisdn':phoneNumber,'yw_id':'1761','bl_time':'2018-06-08'}

    login_data={'operator_id':'user','password':'password'}
    multiFiles={
            'region_id':'1210',
            'school_id':'295',
            **paramater,
            'fzr_id':login_data['operator_id'],
            'fzr_name':login_data['operator_id']
        }

    # API of website
    get_cookies_url='http://183.207.196.70:8085/haywdjpt/login!login.jspa'
    post1_referer_url='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!checkYwMsisdn.jspa'
    post2_referer_url='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!saveLogin.jspa'
    test_login='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!frame.jspa'

    multiFormData=MultipartEncoder(fields=multiFiles)
    session=requests.session()
    session.post(get_cookies_url,data=login_data)

    res=session.post(post1_referer_url,data=paramater)
    if res.text=='0':
        res=session.post(post2_referer_url,data=multiFormData,headers={'Content-Type':multiFormData.content_type})
    print(res.text)
