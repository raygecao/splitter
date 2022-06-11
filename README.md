## 介绍

表中的列field为多维数据combine的结果，不利于分组展示数据。本项目旨在将combined key 拆成对应的维度，根据这些维度构建一棵目录树存放相应分类对应的数据表。

此项目并无通用性，仅用以对特殊仿真软件输出的结果进行归类。



## 环境准备

- 安装git，python3，pip，python3-venv

  - 克隆本项目：`git clone https://github.com/raygecao/splitter.git`，进入到项目目录：`cd splitter`

- 构建并进入venv虚拟环境

  ```shell
  python3 -m venv venv      # 创建virtual environments
  source venv/bin/activate  # 进入虚拟环境
  ```

- 安装第三方模块： `pip3 install -r requirements.txt`



## 用法

- 根据仿真软件输出的csv生成多维树表

  ```shell
  # 第一个参数为原始表的路径，第二个参数为输出树表的根路径
  # 此例中原始表位于 data/demo.csv，输出的路径为/tmp/data
  python3 splitter.py data/demo.csv /tmp/data
  ```

- 查看输出目录树状结构

  ```shell
  # 查看目录结构，按上例输出的目录为/tmp/data
  
  tree /tmp/data
  /tmp/data
  ├── state_0
  │   ├── vdc_-0.5
  │   │   ├── cycle_1
  │   │   │   └── data.csv
  │   │   ├── cycle_2
  │   │   │   └── data.csv
  │   │   ├── cycle_3
  │   │   │   └── data.csv
  │   │   └── cycle_4
  │   │       └── data.csv
  │   ├── vdc_-1.0
  │   │   ├── cycle_1
  │   │   │   └── data.csv
  │   │   ├── cycle_2
  │   │   │   └── data.csv
  │   │   ├── cycle_3
  │   │   │   └── data.csv
  │   │   └── cycle_4
  │   │       └── data.csv
  │   ├── vdc_-1.5
  # ...略去100+行输出
  ```

- 画出某个分类下的数据图

  ```shell
  # 第一个参数为上面树表输出的目录path；第二个参数为state值；第3个参数为vdc的值（需要跟树路径中的值一致，eg -2.0, 1.0等）；第四个参数为周期数
  # state=0, vdc=-1.5, cycle=3 下两种模型的对比图
  python3 plot/plot.py /tmp/data 0 -1.5 3
  ```

  

## 扩展

- `plot/plot.py`下有使用`matplotlib`库绘制数据图的简单demo，如需绘制更复杂的图（如网格布局，区间展示等）可以参考[matplotlib用户文档]( https://matplotlib.org/stable/tutorials/introductory/usage.html )进行修改更新

