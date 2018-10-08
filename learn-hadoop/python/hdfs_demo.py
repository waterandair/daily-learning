from hdfs import InsecureClient
from hdfs.client import Client


# 读取hdfs文件内容,将每行存入数组返回
def read_hdfs_file(client, filename):
    lines = []
    with client.read(filename, encoding='utf-8', delimiter='\n') as reader:
        for line in reader:
            lines.append(line.strip())
    return lines


def write_hdfs_file(client, filename, content):
    with client.write(filename) as writer:
        writer.write(content)


if __name__ == '__main__':
    client = InsecureClient('http://localhost:9870', user='zj')
    # 读取文件内容
    # print(read_hdfs_file(client, "/nba/LAL/kobe.txt"))

    # 写文件，不可以有重复文件
    # write_hdfs_file(client, "/nba/LAL/kobe2.txt", b"content")

    # 追加数据到hdfs文件
    # client.write("/nba/LAL/kobe.txt", "append", overwrite=False, append=True)

    # 覆盖数据写到hdfs文件
    # client.write("/nba/LAL/kobe.txt", "overwrite", overwrite=True, append=False)

    # 获取目录下所有文件和文件夹
    # print(client.list("/nba/LAL"))

    # 获取文件或文件夹的元信息
    # print(client.content("/nba/LAL"))

    # 获取文件或文件夹的元信息
    # print(client.status("/nba/LAL"))

    # 移动或修改文件或文件夹
    # client.rename("/nba", "/NBA")

    # 创建目录
    # client.makedirs("/new/dir")

    # 删除文件或目录
    # client.delete('/NBA', recursive=True)

    # 上传文件
    # client.upload("/new", "/etc/hosts")

    # 下载文件或文件夹到本地
    # client.download('/NBA', '/home/zj/', n_threads=5)

    # 获取文件夹下所有的目录以及目录下的文件， 可以指定深度
    # files = client.walk("/", 3)
    # for dpath, _, fnames in files:
    #     print(dpath, fnames)

    # 使用 content() 或 status() 判断文件是否存在, 加入参数 strict=False，如果问价不存在返回 None
    print(client.content("/not/exist/file", strict=False))  # None
    print(client.status("/not/exist/file", strict=False))  # None








