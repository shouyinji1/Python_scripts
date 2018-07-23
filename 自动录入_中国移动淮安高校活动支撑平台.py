import requests
import openpyxl
from requests_toolbelt import MultipartEncoder

login_data={'operator_id':'User','password':'Password'}
file='File Name'
sheet='Sheet1'
min_range=1589
max_range=1627


# API of website
get_cookies_url='http://183.207.196.70:8085/haywdjpt/login!login.jspa'
post1_referer_url='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!checkYwMsisdn.jspa'
post2_referer_url='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!saveLogin.jspa'
test_login='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!frame.jspa'

#登陆
session=requests.session()
session.post(get_cookies_url,data=login_data)

#读取Excel
def excel_data(file,sheet):
	wb=openpyxl.load_workbook(filename=file)
	sheet_ranges=wb[sheet]
	return(sheet_ranges)

for i in range(min_range,max_range):
	excel=excel_data(file,sheet)
	if(excel['I'+str(i)].value in ['同意']): #筛选条件
		phoneNumber=str(excel['A'+str(i)].value) #获取号码
		print(phoneNumber)
	else:
		continue

	paramater={
		'msisdn':phoneNumber,
		'yw_id':'1761',	# 业务名称
		'bl_time':'2018-07-21'	# 办理时间
	}

	multiFiles={
		'region_id':'1210',
		'school_id':'295', # 学校
		**paramater,
		'fzr_id':login_data['operator_id']
	}

	multiFormData=MultipartEncoder(fields=multiFiles)
	res=session.post(post1_referer_url,data=paramater)
	if res.text=='0':
		res=session.post(post2_referer_url,data=multiFormData,headers={'Content-Type':multiFormData.content_type})
	print(res.text)