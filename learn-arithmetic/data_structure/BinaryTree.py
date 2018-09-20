"""
二叉树
    性质：
        1. 二叉树第 i 层上的结点数目最多为 2 的 (i-1) 次方， i>=1
        2. 深度为 k 的二叉树至多有 2 的 k 次方减 1 个结点, k≥1
        3. 包含n个节点的二叉树的高度至少为log2 (n+1)。
        4. 在任意一棵二叉树中，若终端结点的个数为n0，度为2的节点(即节点子树个数为2的节点)数为n2，则n0=n2+1。

满二叉树:
        高度为h，并且由2的n次方减1个结点的二叉树，被称为满二叉树。

完全二叉树（堆）：
        一棵二叉树中，只有最下面两层结点的度可以小于2，并且最下一层的叶结点集中在靠左的若干位置上。这样的二叉树称为完全二叉树。
        叶子结点只能出现在最下层和次下层，且最下层的叶子结点集中在树的左部。显然，一棵满二叉树必定是一棵完全二叉树，而完全二叉树未必是满二叉树。
    编号：
        如果对完全二叉树从的n个节点从1到n顺序编序，对编号为 i 的节点有一下性质：
            i = 1, 则节点i是二叉树的根
            i > 1, 则其父节点是 i//2
            2i <= n, 则节点i的的左孩子为 2i
            2i > n, 则节点i无左孩子
            2i+1 <= n, 节点i的有孩子为 2i + 1
            2i+1 > n, 则节点i无右孩子


二叉查找树：
        二叉查找树(Binary Search Tree)，又被称为二叉搜索树。设x为二叉查找树中的一个节点，x节点包含关键字key，节点x的key值记为key[x]。
        如果y是x的左子树中的一个结点，则key[y] <= key[x]；如果y是x的右子树的一个结点，则key[y] >= key[x]。
    性质：
        若任意节点的左子树不空，则左子树上所有结点的值均小于它的根结点的值；
        任意节点的右子树不空，则右子树上所有结点的值均大于它的根结点的值；
        任意节点的左、右子树也分别为二叉查找树。
        没有键值相等的节点（no duplicate nodes）。

"""


class Node:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left_child = left
        self.right_child = right

    # 插入左节点
    def insert_left(self, node):
        if type(node) is Node:
            if self.left_child is None:
                self.left_child = node
            else:
                node.left_child = self.left_child
                self.left_child = node
        else:
            return False

    def insert_right(self, node):
        if type(node) is Node:
            if self.right_child is None:
                self.right_child = node
            else:
                node.right_child = self.right_child
                self.right_child = node
        else:
            return False

    # 获取左节点
    def get_left_child(self):
        return self.left_child

    # 获取有右节点
    def ger_right_child(self):
        return self.right_child

    def set_val(self, value):
        self.value = value

    def get_val(self):
        return self.value

    # 前序遍历，返回前序遍历的结果列表
    def pre_traverse(self):
        arr = []

        def _pre_traverse(node):
            if node is None:
                return
            else:
                arr.append(node.value)
                _pre_traverse(node.left_child)
                _pre_traverse(node.right_child)
        _pre_traverse(self)

        return arr


if __name__ == '__main__':
    root = Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(9)))
    print(root.pre_traverse())






