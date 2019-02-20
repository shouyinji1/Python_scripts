import requests
import openpyxl
from requests_toolbelt import MultipartEncoder

login_data={'operator_id':'账号','password':'密码'}	# 账号密码
file='文件路径'	# 文件路径
sheet='Sheet1'	# 表格
min_range=1	# 首列
max_range=278	# 尾列+1


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
	if(excel['R'+str(i)].value in ['2018级新生号卡使用/插卡'] or excel['S'+str(i)].value in ['2018级新生号卡使用/插卡']): #筛选条件
		phoneNumber=str(excel['M'+str(i)].value) #获取号码
		print(phoneNumber)
	else:
		continue

	paramater={
		'msisdn':phoneNumber,
		'yw_id':'1823',	# 业务名称代号，2018级新生号卡使用/插卡
		'bl_time':'2018-08-20'	# 办理时间
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
