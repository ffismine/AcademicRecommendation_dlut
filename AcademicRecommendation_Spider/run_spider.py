import Spider_relation


if __name__ == '__main__':
    # path_name = 'Your path to save name'
    # path_term = 'Your path to save term'
    # path_score = 'Your path to save relation of name&term'
    # num = 'num of teachers, sum = 8930'

    path_name = "..//data//dataset//name//name.json"
    path_term = "..//data//dataset//term//keyword.json"
    path_score = "..//data//dataset//input//user_item_score.txt"

    # 首先通过Spider_data爬取name和term信息，然后通过Spider_relation爬取关系信息
    mySpider = Spider_relation.SpiderRealation(path_name, path_term, path_score)

    # 默认学者数为8930，可以通过这里设置
    mySpider.__set__(mySpider, 15)

    # 启动爬虫
    mySpider.run()
