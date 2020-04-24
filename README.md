# 基于大连理工大学机构知识库的主题词推荐

## 研究目的

面向大连理工大学学者，基于大连理工大学机构知识库，推荐潜在主题词，优化科研方向，促进跨学部、学科、领域科研合作。

## [数据来源：大连理工大学机构知识库](http://dlutir.dlut.edu.cn/)

## 数据集介绍及获取方式
- **大连理工大学机构知识库**：大连理工大学机构知识库作为支撑大连理工大学学术研究的基础设施，以知识管理与学术交流为目标，收集、组织、管理、保存、传播大连理工大学教职工的学术研究成果，实现知识传播与共享。机构知识库中拥有期刊论文、会议论文、学位论文、专利、著作、报纸、标准等多种类型学术成果。
- **爬虫**：主要采用requsts库和etree库相结合的方法，通过post方法获取XML，etree库构建XML树，xpath方法提取内容，获取学者关键词。


## 推荐方法介绍

* **基于协同过滤**：主要采用itemcf经典推荐模型，构建学者-主题向量以及主题共现相似度矩阵，通过MapReduce计算推荐主题词TOP10。

* **基于表示学习的链路预测**：主要采用网络表示学习经典模型node2vec，训练学者及主题embedding，通过Inner-Product计算学者-主题链接强度，从而达到推荐主题词的目的。

* **基于表示学习的协同过滤**：采用网络表示学习经典模型node2vec对主题共现相似度矩阵进行更新，更精准捕捉主题词内在联系，最终通过MapReduce计算最终的推荐主题词主题词TOP20及去除已有主题词TOPN。

* **基于图注意力网络**：在方法2和3的基础上，解决网络节点异质性的问题。数据集加入其他节点，如期刊、会议、学科等实体时，可以更有效地训练embedding，达到在异构网络条件下进行多种学术推荐的目的。

  

## 相关代码

### [大连理工大学机构知识库爬虫](https://github.com/ffismine/AcademicRecommendation_dlutir.dlut.edu.cn/tree/master/AcademicRecommendation_Spider)

### [基于协同过滤](https://github.com/ffismine/AcademicRecommendation_dlutir.dlut.edu.cn/tree/master/AcademicRecommendation_MR)
### [基于链路预测](https://github.com/ffismine/AcademicRecommendation_dlutir.dlut.edu.cn/tree/master/AcademicRecommendation_GE)
### [基于表示学习的协同过滤](https://github.com/ffismine/AcademicRecommendation_dlutir.dlut.edu.cn/tree/master/AcademicRecommendation_MRGE)



## 作者信息
- [谢张](https://github.com/ffismine)

- [徐长琦](https://github.com/xyclxcq)
