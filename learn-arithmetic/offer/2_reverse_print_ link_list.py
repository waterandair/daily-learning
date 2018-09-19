# -*- coding:utf-8 -*-

"""
输入一个链表，按链表值从尾到头的顺序返回一个ArrayList。
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    # 返回从尾部到头部的列表值序列，例如[1,2,3]
    def printListFromTailToHead(self, listNode):
            arr = []
            if listNode.next is None:
                arr.append(listNode.val)
            else:
                self.printListFromTailToHead(listNode.next)
                arr.append(listNode.val)
            


if __name__ == '__main__':
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node1.next = node2
    node2.next = node3


    s = Solution()
    print(s.printListFromTailToHead(node1))

