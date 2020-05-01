# 基于node2vec方法对大连理工大学机构知识库的数据处理

##  数据处理流程

* **node2vec数据处理：**利用node2vec方法，获取数据集的128维数据
* **计算余弦值**：计算获取每个USER节点和每个ITEM节点的余弦相似度，去除USER已有ITEM，取余弦相似度前20的ITEM进行学术关键词推荐。

## 数据结果分析

* **王同华  化工学院  教授、博士生导师：**

  学术关键词：碳膜、气体分离 、gas separation、carbon membrane 、carbon membranes 、聚酰亚胺 、					   polyimide 、pyrolysis 、coal 、活性炭纤维 、聚丙烯腈、polyyacrylonitrile、热解、制备、					   复合碳膜、gas、preparation、separation、吸附、炭分子筛膜

* **基于node2vec的推荐关键词：**

  adsorption、supercapacitor、graphene、活性炭、methane、hydrogen、carbon、membrane、hydrogenation、carbon nanotubes、activated carbon、permeability、oxygen、碳纳米管、biomass、zeolite、褐煤、催化剂、kinetics、synthesis



* **解茂昭  能源与动力学院  教授、博士生导师：**

  学术关键词：数值模拟、多孔介质、numerical simulation、porous media、大涡模拟、内燃机、

  ​					   large eddy simulation、numerical、超绝热燃烧、化学动力模型、泡沫铝、

  ​					   porous medium、combustion、均质压燃、多孔介质发动机、柴油机、气液两相流、湍流、

  ​					   催化燃烧

* **基于node2vec的推荐关键词：**

  heat transfer、computational fluid dynamics、乙醇、方程、co2、evaporation、激光、表面张力、有限元法、电阻率、有限元、传热、biodiesel、carbon dioxide、热力学、激波、density、depressurization、boundary element method、节能

