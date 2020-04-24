# 爬取三元组，需要前两个文件储存的ID

import requests
from lxml import etree
import json
import Spider_data


class SpiderRealation(object):

    def __init__(self, path_name, path_term, path_score):
        self.path1 = path_name
        self.path2 = path_term
        self.path3 = path_score

        # 大连理工大学机构知识库
        self.url = 'http://dlutir.dlut.edu.cn/SearchResult/FilterPage'

        # 模拟成浏览器去访问网站，解决requests请求反爬问题
        self.headers = {'user-agent':'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'}
        self.num = 8930

        # 关键词的Xpath路径
        self.termlabel = '//dd/label/@title'

        # 关键词权重的Xpath路径
        self.numlabel = '//dd/span/text()'

    def __set__(self, instance, value):
        self.num = value

    def run(self):
        Spiderdata = Spider_data.SpiderData(self.path1, self.path2, self.num)
        Spiderdata.spiderName()
        Spiderdata.spiderTerm()
        self.spider()

    def spider(self):
        with open(self.path1, 'r', encoding='utf-8') as n:
            with open(self.path2, 'r', encoding='utf-8') as k:
                with open(self.path3, 'w', encoding='utf-8') as s:
                    n_dict = json.load(n)
                    k_dict = json.load(k)
                    for i in range(self.num):
                        name_url = 'http://dlutir.dlut.edu.cn/Scholar/Detail/{}'.format(i)

                        # 等待30s后服务器无反应，停止请求，由req.raise_for_status()抛出异常
                        try:
                            req = requests.get(name_url, headers=self.headers, timeout=30)
                            req.raise_for_status()

                            # 获得返回值的编码方式
                            req.encoding = req.apparent_encoding
                        except:
                            print("服务器中断连接！！！")
                            continue

                        # 分析XML文档
                        req.xpath = etree.HTML(req.text).xpath

                        # 检验教师是否关闭个人学术主页
                        if req.xpath('/html/head/title/text()') == '此页面不公开或你没有访问此页面的权限':
                            continue

                        # 作者姓名的Xpath路径
                        name_list = req.xpath(
                            '/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/p/a/text()')

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
                            r = requests.post(self.url, data=from_data, headers=self.headers, timeout=30)
                            r.raise_for_status()

                            # 获得返回值的编码方式
                            r.encoding = r.apparent_encoding
                        except:
                            print('服务器中断连接！！！')
                            continue

                        # 分析XML文档
                        r.xpath = etree.HTML(r.text).xpath

                        # 关键词的Xpath路径
                        term_list = r.xpath(self.termlabel)

                        # 关键词权重的Xpath路径
                        number_list = r.xpath(self.numlabel)

                        # 形成三元组
                        for keys in zip(term_list, number_list):
                            for names in name_list:
                                s.write(str(n_dict.get("%s" % names, 'none')))
                                s.write('\t')
                            s.write(str(k_dict.get('%s' % keys[0], 'none')))
                            s.write('\t')
                            s.write(keys[1])
                            s.write('\n')

                        # 当前爬取的进度
                        print(i)





