#!/usr/bin/python3
# coding: UTF-8
from lxml import etree

test = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a> # 注意，此处缺少一个 </li> 闭合标签
     </ul>
 </div>
'''

# 利用 etree.HTML, 将字符串解析为HTML文档
html = etree.HTML(test)

# 按字符串序列化 HTML 文档
result = etree.tostring(html)
# print (result)  # lxml 可以自动修正 html 代码，例子里不仅补全了 li 标签，还添加了 body，html 标签。


# 从 html 文件中读取内容, 使用 etree.parse() 方法
html = etree.parse('./test_html.html')
result = etree.tostring(html, pretty_print=True)
print(result)
print(type(html))  # <class 'lxml.etree._ElementTree'>


# 获取所有的 <li> 标签
result = html.xpath('//li')
print(result)  # [<Element li at 0x7fc5f92fb948>, <Element li at 0x7fc5f92fb988>, <Element li at 0x7fc5f92fb9c8>, <Element li at 0x7fc5f92fba08>, <Element li at 0x7fc5f92fba48>]
print(len(result))  # 4
print(type(result))  # <class 'list'>
print(type(result[0]))  # <class 'lxml.etree._Element'>

# 继续获取 <li> 标签的所有 class 属性
result = html.xpath('//li/@class')
print(result)  # ['item-0', 'item-1', 'item-inactive', 'item-1', 'item-0']

# 继续获取 <li> 标签下 href 为 link1.html 的 <a> 标签
result = html.xpath('//li/a[@href="link1.html"]')
print(result)  # [<Element a at 0x7fcb88e54ac8>]

# 获取 <li> 标签下的所有 <span> 标签
result = html.xpath('//li//span')
print(result)  # [<Element span at 0x7f4f92a2b9c8>]

# 获取 <li> 标签下的 <a> 标签里的所有class
result = html.xpath('//li/a//@class')
print(result)

# 获取最后一个 <li> 的 <a> 的 href
result = html.xpath('//li[last()]/a/@href')
print(result)  # ['link5.html']

# 获取倒数第二个元素的内容
result = html.xpath('//li[last()-1]/a')
print(result[0].text)  # fourth item

# 获取 class 值为 bold 的标签名
result = html.xpath('//*[@class="bold"]')
print(result[0].tag)  # span