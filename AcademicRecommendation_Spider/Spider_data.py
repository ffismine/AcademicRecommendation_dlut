import requests
from lxml import etree
import json


class SpiderData(object):
    def __init__(self, path_name, path_term, num):

        # 大连理工大学机构知识库
        self.url = 'http://dlutir.dlut.edu.cn/SearchResult/FilterPage'

        # 模拟成浏览器去访问网站，解决requests请求反爬问题
        self.headers_name = {
            'user-agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
        self.headers_term = {
            'user-agent': 'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'}
        self.n = num
        self.Path_name = path_name
        self.Path_term = path_term
        self.namelabel = '/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/p/a/text()'
        self.termlabel = '//dd/label/@title'


    # 获取名字
    def spiderName(self):
        namelist = []
        for i in range(self.n):
            name_url = 'http://dlutir.dlut.edu.cn/Scholar/Detail/{}'.format(i)

            # 等待30s后服务器无反应，停止请求，由req.raise_for_status()抛出异常
            try:
                req = requests.get(name_url, headers=self.headers_name, timeout=30)
                req.raise_for_status()

                # 获得返回值的编码方式
                req.encoding = req.apparent_encoding
            except:
                print("服务器中断连接！！！")
                continue

            # 分析XML文档
            req.xpath = etree.HTML(req.text).xpath

            # 检验教师是否关闭个人学术主页
            if req.xpath('/html/head/title/text()')[0] == '此页面不公开或你没有访问此页面的权限':
                continue

            # 学者姓名的Xpath路径
            s = req.xpath(self.namelabel)

            # 爬取关键词需要向浏览器提交的表单
            from_data = {'KeywordList[0][FieldName]': 'OwnerCancel_UserId',
                         'KeywordList[0][Aggs]': 'Owner_UserId',
                         'KeywordList[0][FieldValue][]': i,
                         'KeywordList[0][FieldValueName][]': i,
                         'UserId': i,
                         'Type_Index': 1,
                         'SubjectId_Index': 1,
                         'Index_Index': 1,
                         'ImportantType_Index': 1,
                         'ScientificSource_Index': 1,
                         'JournalCondition_Index': 1,
                         'Year_Index': 1,
                         'KeywordCondition_Index': 1,
                         'Language_Index': 1,
                         'CurrentIndex': 1,
                         'Id': i,
                         'PageIndex': 1,
                         'IncludeFieldList': 'KeywordCondition',
                         'CurrentOrder': 'PrintDate',
                         'isResult': 'false'
                         }

            # 向服务器提交表单，等待30s后服务器无反应，停止请求，由req.raise_for_status()抛出异常
            try:
                r = requests.post(self.url, data=from_data, headers=self.headers_name, timeout=30)
                r.raise_for_status()

                # 获得返回值的编码方式
                r.encoding = r.apparent_encoding
            except:
                print('服务器中断连接！！！')
                continue

            # 分析XML文档
            r.xpath = etree.HTML(r.text).xpath

            # 判断返回的关键词列表是否为空，若该作者关键词不为空，那么获取该作者姓名
            if len(r.xpath(self.termlabel)) != 0:
                for q in s:
                    if q != '管理员':
                        namelist.append(q)
            else:
                continue

            # 当前爬取的进度
            print(i)

            # 构造字典，以字典形式储存在json文件
            text_dict = dict(zip(namelist, range(len(namelist))))
            json_str = json.dumps(text_dict, indent=2, ensure_ascii=False)

            with open(self.Path_name, 'w', encoding='utf-8') as f:
                f.write(json_str)

    # 获取关键词/主题
    def spiderTerm(self):
        termset = set()
        for i in range(self.n):

            # 爬取关键词需要向浏览器提交的表单
            from_data = {'KeywordList[0][FieldName]': 'OwnerCancel_UserId',
                         'KeywordList[0][Aggs]': 'Owner_UserId',
                         'KeywordList[0][FieldValue][]': i,
                         'KeywordList[0][FieldValueName][]': i,
                         'KeywordList[0][IsShow][]': 'false',
                         'UserId': i,
                         'Type_Index': 1,
                         'SubjectId_Index': 1,
                         'Index_Index': 1,
                         'ImportantType_Index': 1,
                         'ScientificSource_Index': 1,
                         'JournalCondition_Index': 1,
                         'Year_Index': 1,
                         'KeywordCondition_Index': 1,
                         'Language_Index': 1,
                         'CurrentIndex': 1,
                         'Id': i,
                         'PageIndex': 1,
                         'IncludeFieldList': 'KeywordCondition',
                         'CurrentOrder': 'PrintDate',
                         'isResult': 'false'
                         }

            # 向服务器提交表单，等待30s后服务器无反应，停止请求，由req.raise_for_status()抛出异常
            try:
                r = requests.post(self.url, data=from_data, headers=self.headers_term, timeout=30)
                r.raise_for_status()

                # 获得返回值的编码方式
                r.encoding = r.apparent_encoding
            except:
                print('服务器中断连接！！！')
                continue

            # 分析XML文档
            r.xpath = etree.HTML(r.text).xpath

            # 关键词去重
            for q in r.xpath(self.termlabel):
                termset.add(q)

            # 当前爬取的进度
            print(i)

        # 构造字典，以字典形式储存在json文件
        lists = list(termset)
        text_dict = dict(zip(lists, range(len(lists))))
        json_str = json.dumps(text_dict, indent=2, ensure_ascii=False)
        with open(self.Path_term, 'w', encoding='utf-8') as f:
            f.write(json_str)


