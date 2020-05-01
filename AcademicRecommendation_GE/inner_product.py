import numpy as np
import operator


class PrepareState(object):
    def __init__(self):

        # User - Item - Score 三元组文件路径
        self.prepare_read_path = '..//xcq.txt'

        # 以 User - Item - Item 为索引的文件路径
        self.prepare_write_path = '..//prepare.txt'

        # node2vec算法生成的128维向量文件
        self.embedding_path = '..//embeddings.txt'

        # 储存 User - Vector 节点的文件路径
        self.u_embedding_path = '..//u_embeddings.txt'

        # 储存 Item - Vector 节点的文件路径
        self.i_embedding_path = '..//i_embeddings.txt'

    def prepare(self):

        # 创建 User 索引字典
        index = dict()
        r = open(self.prepare_read_path, 'r')
        w = open(self.prepare_write_path, 'w')

        # 按行读入文件内容，以'\t'为标志分割字符串
        while True:
            entry = r.readline().split('\t')

            # 读入文件为三元组，若每行读入的列表长度若小于等于1，则可认为读入完成
            if len(entry) <= 1:
                break

            # 判断三元组的 User 是否在字典中，
            # 若不在，创建以该 User 为键，空列表为值的键值对，若在，则将 Item 添加到列表中
            if entry[0] not in index:
                index.setdefault(entry[0], [])
                index[entry[0]].append(entry[1])
            else:
                index[entry[0]].append(entry[1])

        # 写入文件
        for u in index:
            w.write(u + '\t')
            for i in index.get(u, None):
                w.write(i + ' ')
            w.write('\n')
        w.close()
        r.close()

    def embedding(self):

        r = open(self.embedding_path, 'r')
        u = open(self.u_embedding_path, 'w')
        i = open(self.i_embedding_path, 'w')

        # 按行读入文件内容，去除'\n'字节，以'\t'为标志分割字符串
        while True:
            entry = r.readline().replace('\n', '').split(' ')

            # 读入文件为128维向量，若每行读入的列表长度若小于等于1，则可认为读入完成
            if len(entry) <= 1:
                break

            # 筛选出 User 节点的128维向量
            if entry[0].startswith('u'):
                for key in entry:
                    u.write(key + '\t')
                u.write('\n')

            # 筛选出 Item 节点的128维向量
            if entry[0].startswith('i'):
                for key in entry:
                    i.write(key + '\t')
                i.write('\n')
        r.close()
        u.close()
        i.close()


class Embeddings(PrepareState):
    def __init__(self):
        super().__init__()

        # 储存 User - Item - Inner product 的文件路径
        self.inner_product_path = '..//inner_product.txt'

        # 储存 User - Item:Inner product - Item:Inner product 的文件路径
        self.inner_product_score_path = '..//inner_product_score.txt'

        # 取余弦相似度大小前 rank 个输出
        self.rank = 20

        # 储存去重 User - Item:Inner product - Item:Inner product 的文件路径
        self.inner_product_duplicate_score_path = '..//inner_product_duplicate_score.txt'

        # 储存 Item - Item - inner product 的三元组文件路径
        self.i_inner_product = '..//i_inner_product.txt'

        # 储存倒排索引的函数
        self.reverse_index_path = '..//reverse_index.txt'

    def inner_product(self):

        u = open(self.u_embedding_path, 'r')
        i = open(self.i_embedding_path, 'r')
        w = open(self.inner_product_path, 'w')
        l = 0
        # 按行读入文件内容，去除'\n'字节，以'\t'为标志分割字符串
        for a in range(20):
            entry1 = u.readline().replace('\n', '').split('\t')
            print(l)
            l += 1
            # 读入文件为128维向量，若每行读入的列表长度若小于等于1，则可认为读入完成
            if (len(entry1)) <= 1:
                break

            # str -> float，便于数据处理
            for key in range(1, len(entry1) - 1):
                entry1[key] = float(entry1[key])
            vec1 = np.array(entry1[1:len(entry1) - 1])

            # 按行读入文件内容，去除'\n'字节，以'\t'为标志分割字符串
            while True:
                entry2 = i.readline().replace('\n', '').split('\t')

                # 读入文件为128维向量，若每行读入的列表长度若小于等于1，则可认为读入完成
                if (len(entry2)) <= 1:
                    break

                # str -> float，便于数据处理
                for key in range(1, len(entry2) - 1):
                    entry2[key] = float(entry2[key])
                vec2 = np.array(entry2[1:len(entry2) - 1])

                # 求内积
                inner_pdt = np.dot(vec1, vec2)

                # 写入文件
                w.write(str(entry1[0]) + '\t' + str(entry2[0]) + '\t' + str(inner_pdt) + '\n')

            #  Item 文件遍历一次后，文件指针重新回到文件开头继续遍历
            i.seek(0)
        u.close()
        i.close()
        w.close()

    def score_line(self):

        # 创建 User 索引字典
        index = dict()
        r = open(self.inner_product_path, 'r')
        w = open(self.inner_product_score_path, 'w')

        # 按行读入文件内容，去除'\n'字节，以'\t'为标志分割字符串
        while True:
            entry = r.readline().replace('\n', '').split('\t')

            # 读入文件为三元组，若每行读入的列表长度若小于等于1，则可认为读入完成
            if len(entry) <= 1:
                break

            # 判断三元组的 User 是否在字典中，
            # 若不在，创建以该 User 为键，空字典为值的键值对
            # 若在，则将 {Item: inner product} 更新到字典中
            if entry[0] not in index:
                index.setdefault(entry[0], dict())
                index[entry[0]].update({entry[1]: entry[2]})
            else:
                index[entry[0]].update({entry[1]: entry[2]})

        # 写入文件
        for u in index.keys():
            w.write(u + '\t')
            for key, value in index.get(u, None).items():
                w.write(key + ':' + value + ' ')
            w.write('\n')
        w.close()
        r.close()

    def score_line_duplicate_removal(self):
        """
        :param read_path: User - Item - inner product 三元组文件路径
        :param duplicate_read_path: prepare 函数中生成的以 User 为索引的文件路径
        :param write_path: 以 User 索引的文件路径
        :param rank: 取余弦相似度大小前 rank 个输出
        """

        # 创建 User 索引字典
        index = dict()
        renard_index = dict()
        l = 0
        r = open(self.inner_product_path, 'r')
        d = open(self.prepare_write_path, 'r')
        w = open(self.inner_product_duplicate_score_path, 'w')
        while True:
            renard = d.readline().replace('\n', '').replace('\t', ' ').split(' ')
            renard.remove('')
            print(l)
            l += 1
            if len(renard) <= 1:
                break
            if renard[0] not in renard_index:
                renard_index.setdefault(renard[0], [])
            for renards in renard[1:]:
                renard_index[renard[0]].append(renards)

        # 按行读入文件内容，去除'\n'字节，以'\t'为标志分割字符串
        while True:
            entry = r.readline().replace('\n', '').split('\t')

            # 读入文件为三元组，若每行读入的列表长度若小于等于1，则可认为读入完成
            if len(entry) <= 1:
                break

            # 判断三元组的 User 是否在字典中，
            # 若不在，创建以该 User 为键，空字典为值的键值对
            # 若在，则将 {Item: inner product} 更新到字典中
            if entry[0] not in index:
                index.setdefault(entry[0], dict())
            if entry[1] in renard_index[entry[0]]:
                continue

            entry[2] = float(entry[2])
            index[entry[0]].update({entry[1]: entry[2]})

        # 写入文件
        for u in index:
            w.write(u + '\t')
            num = 0
            sorted_index = sorted(index[u].items(), key=operator.itemgetter(1), reverse=True)
            for key, value in sorted_index:
                w.write(key + ':' + str(value) + ' ')
                num += 1
                if num >= self.rank:
                    break
            w.write('\n')
        w.close()
        r.close()
        d.close()

    def item(self):
        """
        :param read_path: 以 Item 为节点的128维向量文件路径
        :param write_path: Item - Item - inner product 的三元组文件路径
        :return:
        """

        r = open(self.i_embedding_path, 'r')
        w = open(self.i_inner_product, 'w')

        # 按行读入文件内容，去除'\n'字节，以'\t'为标志分割字符串
        for a in range(10):
            entry1 = r.readline().replace('\n', '').split('\t')

            # 读入文件为128维向量，若每行读入的列表长度若小于等于1，则可认为读入完成
            if (len(entry1)) <= 1:
                break
            print(a)
            # str -> float，便于数据处理
            for key in range(1, len(entry1) - 1):
                entry1[key] = float(entry1[key])
            vec1 = np.array(entry1[1:len(entry1) - 1])

            #
            fp = r.tell()
            # 将文件指针置于开头
            r.seek(0)
            # 按行读入文件内容，去除'\n'字节，以'\t'为标志分割字符串
            for s in range(10):
                entry2 = r.readline().replace('\n', '').split('\t')

                # 读入文件为128维向量，若每行读入的列表长度若小于等于1，则可认为读入完成
                if (len(entry2)) <= 1:
                    break
                print(s)
                # str -> float，便于数据处理
                for key in range(1, len(entry2) - 1):
                    entry2[key] = float(entry2[key])
                vec2 = np.array(entry2[1:len(entry2) - 1])

                # 求内积
                inner_pdt = np.dot(vec1, vec2)

                # 写入文件
                w.write(str(entry1[0]) + '\t' + str(entry2[0]) + '\t' + str(inner_pdt) + '\n')

            #  Item 文件遍历一次后，文件指针重新回到外层循环继续遍历
            r.seek(fp, 0)
        r.close()
        w.close()

    def reverse_index(self):

        r = open(self.inner_product_path, 'r')
        w = open(self.reverse_index_path, 'w')
        index = dict()
        inverted_index = dict()

        while True:
            entry = r.readline().replace('\n', '').split('\t')

            # 读入文件为三元组，若每行读入的列表长度若小于等于1，则可认为读入完成
            if len(entry) <= 1:
                break

            # 判断三元组的 User 是否在字典中，
            # 若不在，创建以该 User 为键，空字典为值的键值对
            # 若在，则将 {Item: inner product} 更新到字典中
            if entry[0] not in index:
                index.setdefault(entry[0], dict())
                index[entry[0]].update({entry[1]: entry[2]})
            else:
                index[entry[0]].update({entry[1]: entry[2]})
        for User, Item in index.items():
            for Item_id, inner_pdt in Item.items():
                if Item_id not in inverted_index.keys():
                    inverted_index.setdefault(Item_id, dict())
                inner_pdt = float(inner_pdt)
                inverted_index[Item_id].update({User: inner_pdt})

        for i in inverted_index:
            w.write(i + '\t')
            num = 0
            sorted_index = sorted(inverted_index[i].items(), key=operator.itemgetter(1), reverse=True)
            for key, value in sorted_index:
                w.write(key + ':' + str(value) + ' ')
                num += 1
                if num >= self.rank:
                    break
            w.write('\n')
        r.close()
        w.close()


if __name__ == "__main__":
    # prepare 函数的参数
    # prepare(prepare_read_path, prepare_write_path)
    # embedding 函数的参数
    # embedding(embedding_path, u_embedding_path, i_embedding_path)
    # inner_product 函数的参数
    # inner_product(u_embedding_path, i_embedding_path, inner_product_path)
    # score_line 函数的参数
    # score_line(inner_product_path, inner_product_score_path)
    # item 函数的参数
    # item(i_embedding_path, i_inner_product)
    # score_line_duplicate_removal 函数的参数
    # score_line_duplicate_removal(inner_product_path, prepare_write_path, inner_product_duplicate_score_path, n)
    # reverse_index 函数的参数
    # reverse_index(inner_product_path, reverse_index_path, n)

    second = Embeddings()
    second.inner_product()
    print('ok')
    second.score_line_duplicate_removal()
