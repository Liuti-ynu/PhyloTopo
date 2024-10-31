'''
python 版本建议3.0以上
必备模块:ete3 (pip install ete3)
软件版本:Phylotopo 1.0.0
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

# 字典用于存储 Tree 对象及其计数
tree_dict = {}

# 定义一个函数，用于查找是否存在拓扑结构相同的树
def find_identical_tree(new_tree, tree_dict):
    for existing_tree, count in tree_dict.items():
        if new_tree.compare(existing_tree, unrooted=True)['rf'] == 0:
            return existing_tree
    return None

# 打开并读取基因树文件
with open(tree_file, 'r') as f:
    # 读取第一行，解析成 Tree 对象并加入字典
    first_tree = Tree(f.readline().strip(), format=1)
    tree_dict[first_tree] = 1
    
    # 处理文件中的每棵树
    for line in f:
        new_tree = Tree(line.strip(), format=1)
        identical_tree = find_identical_tree(new_tree, tree_dict)
        
        if identical_tree:
            # 如果相同，则更新字典中对应树的计数
            tree_dict[identical_tree] += 1
        else:
            # 如果不同，则将新树添加到字典中
            tree_dict[new_tree] = 1

# 将结果写入输出文件
with open(output, 'w') as f:
    for tree, count in tree_dict.items():
        f.write(tree.write(format=1).strip() + '\t' + str(count) + '\n')
