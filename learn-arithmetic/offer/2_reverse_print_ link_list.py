# -*- coding:utf-8 -*-

"""
输入一个链表，按链表值从尾到头的顺序返回一个ArrayList。
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution_1:
    """
    递归解法
    """
    # 返回从尾部到头部的列表值序列，例如[1,2,3]
    def printListFromTailToHead(self, listNode):
        arr = []
        if type(listNode) is ListNode:
            self.tail_to_head(listNode, arr)
        return arr

    def tail_to_head(self, listNode, arr):
        if listNode.next is None:
            arr.append(listNode.val)
            return
        else:
            self.tail_to_head(listNode.next, arr)
            arr.append(listNode.val)


class Solution_2:
    """
    循环解法
    """
    # 返回从尾部到头部的列表值序列，例如[1,2,3]
    def printListFromTailToHead(self, listNode):
        l = []
        head = listNode
        while head:
            l.insert(0, head.val)
            head = head.next
        return l


if __name__ == '__main__':
    node1 = ListNode(67)
    node2 = ListNode(0)
    node3 = ListNode(24)
    node4 = ListNode(58)
    node1.next = node2
    node2.next = node3
    node3.next = node4

    s = Solution_1()
    print(s.printListFromTailToHead(node1))

