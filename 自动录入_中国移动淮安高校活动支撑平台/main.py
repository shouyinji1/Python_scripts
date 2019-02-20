#!/usr/bin/python3

import re
import requests
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup

class Execute:
        # API of website
        __get_cookies_url='http://183.207.196.70:8085/haywdjpt/login!login.jspa'
        __post1_referer_url='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!checkYwMsisdn.jspa'
        __post2_referer_url='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!saveLogin.jspa'
        __test_login='http://183.207.196.70:8085/haywdjpt/gxdj/ywdj!frame.jspa'

        __session=None
        __r=None

        __login_data={    # 账号密码
                'operator_id':'',
                'password':''
        }	
        __paramater={ # 录入信息
                'msisdn':'',   # 录入手机号
                'yw_id':'',	# 业务名称代号
                'bl_time':'',	# 办理时间
                'team_name':''  # 队员姓名
        }
        __multiFiles={    # post信息
                'region_id':'',     # 县区
                'school_id':'', # 学校
                'fzr_id':'',  # 账号
        }

        def __init__(self,username,password,phoneNumber,yw,bl_time,team_name=''):
                self.__login_data['operator_id']=username
                self.__login_data['password']=password
                try:
                        self.__session=requests.session()
                        self.__session.post(self.__get_cookies_url,data=self.__login_data)
                        self.__r=self.__session.get(self.__test_login)
                except Exception:
                        raise InitFault()
                self.__paramater['msisdn']=phoneNumber
                self.__paramater['yw_id']=self.__convert_id(yw)
                self.__paramater['bl_time']=bl_time
                self.__paramater['team_name']=team_name
                self.__multiFiles['region_id']=self.__get_id('region_id')
                self.__multiFiles['school_id']=self.__get_id('school_id')
                self.__multiFiles['fzr_id']=self.__login_data['operator_id']
                self.__multiFiles.update(self.__paramater)

        def __get_id(self, string_id):
                soup=BeautifulSoup(self.__r.text,'html.parser')
                soup=soup.find(id=string_id)
                get_id=soup.find('option',selected=True).get('value')
                return(get_id)

        def __convert_id(self, string_yw):
                soup=BeautifulSoup(self.__r.text,'html.parser')
                soup=soup.find(id='ywID')
                yw_id=soup.find_all('option')
                for i in range(1,len(yw_id)):
                        if yw_id[i].get_text() == string_yw:
                                return yw_id[i].get('value')
                raise YwIDisNotMatch()

        def send(self):
                multiFormData=MultipartEncoder(fields=self.__multiFiles)
                try:
                        res=self.__session.post(self.__post1_referer_url,data=self.__paramater)  # 检查是否重复录入，重复为1，不重复为0
                except Exception:
                        raise ParameterDoesNotMatchTheFormat()
                        
                if res.text=='0':
                        res=self.__session.post(self.__post2_referer_url,data=multiFormData,headers={'Content-Type':multiFormData.content_type})
                        try:
                                res.text.index("alert(\"已成功登记！\");")
                        except ValueError:
                                raise EntryFailed()
                else:
                        raise EntryRepeated()

class YwIDisNotMatch(Exception):
        def __init__(self,err='业务名称与业务ID无匹配项，业务名称不存在'):
                super().__init__(self,err)
class InitFault(Exception):
        def __init__(self,err='初始化失败，请检查网络和账户状态'):
                super().__init__(self,err)
class EntryFailed(Exception):
        def __init__(self,err='录入失败，请检查'):
                super().__init__(self,err)
class EntryRepeated(Exception):
        def __init__(self,err='录入重复，请检查'):
                super().__init__(self,err)
class ParameterDoesNotMatchTheFormat(Exception):
        def __init__(self,err='参数格式可能不正确，请检查'):
                super().__init__(self,err)

# 录入，2为录入成功，-1为录入异常,1为录入重复
def execute(username, password, phoneNumber, yw, bl_time, team_name=''):
        try:
                luru=Execute(username,password,phoneNumber,yw,bl_time,team_name)
                luru.send()
                return 2
        except EntryRepeated as ex:
                print(ex)
                return 1
        except YwIDisNotMatch as ex:
                print(ex)
        except InitFault as ex:
                print(ex)
        except EntryFailed as ex:
                print(ex)
        except ParameterDoesNotMatchTheFormat as ex:
                print(ex)
        return -1
