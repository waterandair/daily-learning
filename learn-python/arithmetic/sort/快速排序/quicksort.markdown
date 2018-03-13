## 快速排序演算
alist = [54,26,93,17,77,31,44,55,20]
### 第一次递归
start = 0; end = 8
mid = 54
low = 0; high = 8

#### 判断low < high进入循环:
##### 第一次循环
- 从右往左,判断是否大于等于mid,如果为True, high -= 1, 把high位的值,放到low位
   low = 0, high = 8
   [20,26,93,17,77,31,44,55,20]
- 从左往右,判断是否小于mid,如果为 True, low += 1, 把low位的值放到 high 位
   low = 2, high = 8 
   [20,26,93,17,77,31,44,55,93]

##### 第二次循环
- 从右往左,判断是否大于mid,如果为True, high -= 1, 把 high 位的值,放到 low 位
  low = 2; high = 6
  [20,26,44,17,77,31,44,55,93]
- 从左往右,判断是否小于 mid, 如果为 True, low += 1, 把low值放到high位
  low = 4; high = 6
  [20,26,44,17,77,31,77,55,93]

##### 第三次循环
- 从右往左,判断是否大于mid, 如果为 True, high -= 1 , 把 high 值放到 low 位
  low = 4; high = 5
  [20,26,44,17,31,31,77,55,93]
- 从左往右,判断是否小于mid, 如果为 True, low += 1, 把 low位值,放到 high 位
  low = 5; high = 5
  [20,26,44,17,31,31,77,55,93]
  退出循环
  将基准元素放到重合的位置
  [20,26,44,17,31,54,77,55,93]
  
### 分别对基准位置左边和右边的子序列进行快速排序(递归)
### 左边的子序列
#### 按照上面的规则,列表变化过程如下
初始状态: [20,26,44,17,31,54,77,55,93]
mid: 20
start = 0, end = 4
low = 0, high = 4
循环:
low = 0, high = 3
[17,26,44,17,44,31,54,55,93]
low = 1, high = 3
[17,26,44,26,44,31,54,55,93]
--- 
low = 1, high = 1
[17,26,44,26,44,31,54,55,93]
满足循环的退出条件
将基准元素放到重合的位置
[17,20,44,26,44,31,54,55,93]
1和2位置已经确定,继续排序 2 到 5位置的顺序
---
mid = 44
start = 2, end = 5
low = 2, high = 5
循环:
low = 2, high = 5
[17,20,31,26,44,31,54,55,93]
low = 4, high = 5
[17,20,31,26,44,44,54,55,93]
---
low = 4, high = 4
[17,20,31,26,44,44,54,55,93]
满足循环退出条件
将基准元素放到重合位置
[17,20,31,26,44,44,54,55,93]
5 位置的数已经确定, 继续排序 2 到 4 位置的顺序
---
mid = 31
start = 2 , end = 4
low = 2, high = 4
循环:
low = 2, high = 3
[17,20,26,26,44,44,54,55,93]
low = 3, high = 3
[17,20,26,26,44,44,54,55,93]
满足循环条件
将基准元素放到重合的位置
[17,20,26,31,44,44,54,55,93]
排序完成





   

### 快排算法
```python
def quick_sort(alist, start, end):
    """快速排序"""

    # 递归的退出条件
    if start >= end:
        return

    # 设定起始元素为要寻找位置的基准元素
    mid = alist[start]

    # low为序列左边的由左向右移动的游标
    low = start

    # high为序列右边的由右向左移动的游标
    high = end

    while low < high:
        # 如果low与high未重合，high指向的元素不比基准元素小，则high向左移动
        while low < high and alist[high] >= mid:
            high -= 1
        # 将high指向的元素放到low的位置上
        alist[low] = alist[high]

        # 如果low与high未重合，low指向的元素比基准元素小，则low向右移动
        while low < high and alist[low] < mid:
            low += 1
        # 将low指向的元素放到high的位置上
        alist[high] = alist[low]

    # 退出循环后，low与high重合，此时所指位置为基准元素的正确位置
    # 将基准元素放到该位置
    alist[low] = mid
    
    # 对基准元素左边的子序列进行快速排序
    quick_sort(alist, start, low-1)

    # 对基准元素右边的子序列进行快速排序
    quick_sort(alist, low+1, end)
```

```python
def quicksort(alist, start, end):
    if start >= end:
        return
        
    mid = alist[start]
    low, high = start, end
    
    while low < high:
        while low < high and alist[high] >= mid:
            high -= 1
            
        alist[low] = alist[high]
        
        while low < high and alist[low] < mid:
            low += 1
            
        alist[high] = alist[low]
        
    alist[low] = mid
    
    quicksort(alist, start, low - 1)
    
    quicksort(alist, low + 1, end)
```