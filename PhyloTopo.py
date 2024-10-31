'''
python 版本建议3.0以上
必备模块:ete3 (pip install ete3)
软件版本:Phylotopo 1.0.1
软件功能:统计不同拓扑结构的基因树数量
使用方法:python PhyloTopo.py -i 基因树文件路径 -o 输出文件路径
注意事项:输入文件应为基因树文件，每行一棵树，格式为 Newick 格式
'''

from ete3 import Tree
import argparse

# 设置 argparse 参数
parser = argparse.ArgumentParser(description='PhyloTopo - 基因树拓扑结构分析软件：统计不同拓扑结构的基因树数量')
parser.add_argument('-i', '--input', type=str, required=True, help='输入基因树文件路径')
parser.add_argument('-o', '--output', type=str, required=True, help='输出文件路径')
parser.add_argument("-v", "--verbose", action="version", version="Phylotopo 1.0.0", help="显示软件版本")
args = parser.parse_args()

# 读取命令行参数
tree_file = args.input
output = args.output

# 字典用于存储拓扑结构ID及其计数
topology_dict = {}

# 打开并读取基因树文件
with open(tree_file, 'r') as f:
    for line in f:
        new_tree = Tree(line.strip(), format=1)
        # 获取树的拓扑结构 ID
        topology_id = new_tree.get_topology_id()

        # 使用拓扑结构 ID 判断是否已存在相同结构
        if topology_id in topology_dict:
            topology_dict[topology_id]['count'] += 1
        else:
            topology_dict[topology_id] = {'tree': new_tree, 'count': 1}

# 将结果写入输出文件
with open(output, 'w') as f:
    for data in topology_dict.values():
        f.write(data['tree'].write(format=1).strip() + '\t' + str(data['count']) + '\n')
