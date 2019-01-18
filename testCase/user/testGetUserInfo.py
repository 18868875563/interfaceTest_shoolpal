import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp
from common import businessCommon
from common import  businessCommon


localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localClass_xls = common.get_xls("userCase.xlsx", "user")


@paramunittest.parametrized(*localClass_xls)
class GetClassList(unittest.TestCase):

    def setParameters(self, case_name, method, token, email, password, result, code, msg):
        """
                set params
                :param case_name:
                :param method:
                :param token:
                :param email:
                :param password:
                :param result:
                :param code:
                :param msg:
                :param pageIndex
                :param pageSize
                :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.email = str(email)
        self.password = str(password)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")

    def testGetClassList(self):
        """
                test body
                :return:
                """
        # set url
        self.url = common.get_url_from_xml('getuserinfo')
        localConfigHttp.set_url(self.url)

        # set header
        if self.token == '0.0':
            token = localReadConfig.get_headers("token_b")
        else:
            token = self.token
        header = {"Cookie": token, "Content-Type": "application/json"}
        localConfigHttp.set_headers(header)

        # set param
        data = {}
        localConfigHttp.set_data(data)

        # test interface
        self.response = localConfigHttp.post()
        print(self.case_name + "post请求返回")

        # check result
        self.checkResult()

    def tearDown(self):
        """
                :return:
                """
        # logout
        # businessCommon.logout(self.login_token)
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        self.info = self.response.json()
        print(self.info)
        common.show_return_msg(self.response)

        if self.result == '0.0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            result = self.info['info'].get('result')
            self.assertEqual(result,1)

        if self.result == '1.0':
            self.assertEqual(self.info['errCode'], self.code)
            self.assertEqual(self.info['errorMessage'], self.msg)
