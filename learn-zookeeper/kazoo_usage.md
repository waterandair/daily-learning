### 基本用法
#### 处理连接
要开始使用Kazoo，必须创建一个KazooClient对象并建立连接：
```python
from kazoo.client import KazooClient

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
```
默认情况下，客户端将连接到`127.0.0.1:2181`。 
应该确保 Zookeeper 服务器正在运行中，否则 start 命令将一直等到它的默认超时(10s)。  
客户端一旦连接到服务器，不论是连接丢失或是会话到期，都会尝试保持连接。  
可以调用 `stop` 方法删除客户端连接。
```python
zk.stop()
```
##### 日志设置
如果不设置日志，会收到以下消息:
```
No handlers could be found for logger "kazoo.client"
```
为了避免这个问题，仅仅需要加入以下代码：
```python
import logging
logging.basicConfig()
```
详细了解`logging`请阅读[python 日志指南](https://docs.python.org/howto/logging.html)

##### 监听连接事件
客户端需要知道连接什么时候被删除、重置或过期。`kazoo` 简化了这个过程，当连接状态发生变化的时候，会调用被注册的监听函数。
```python
from kazoo.client import KazooState

def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
    else:
        # Handle being connected/reconnected to Zookeeper

zk.add_listener(my_listener)
```
在使用`kazoo.recipe.lock.Lock`或新建临时节点的时候，强烈建议注册状态监听函数去处理连接中断或会话丢失

##### 理解 Kazoo 状态
`KazooState` 对象表示客户端连接的几个状态，始终可以通过 `state` 属性查看连接当前的状态，可能的状态是:
- LOST
- CONNECTED
- SUSPENDED  

首次创建`KazooClient`状态是 `LOST`， 成功建立连接后，状态会转换为 `CONNECTED`。在创建连接的过程中，如果出现连接问题或者需要连接到不同的zookeeper集群节点，状态将转换为 `SUSPENDED`，表示当前命令不能正确执行。如果 zookeeper 节点已经不在是集群节点的一部分时，状态也会为`SUSPENDED`。
重新建立连接后，如果会话已过期，连接转换为`LOST`，如果会话仍然有效，则可以转换为`CONNECTED`。
`建议注册状态监听函数监听连接状态，以保证客户端连接正常运行`
当连接处于`SUSPENDED`的时候，如果客户端正在执行需要其他系统协商的操作(比如锁操作)，应当暂停操作。重新连接后在继续操作，当连接朱状态为`LOST`时，zookeeper 会删除已创建的临时节点，这回影响到临时节点的操作(比如锁操作)，当状态再次转化为`CONNECTED`后，需要重新获取锁。

###### 有效的状态转换
- `LOST -> CONNECTED`： 新建连接或已经创建但丢失的连接重新连接正常
- `CONNECTED -> SUSPENDED`： 处于连接状态的连接发生连接丢失
- `CONNECTED -> LOST`： 仅当建立连接后不能有效的验证身份的时候发生
- `SUSPENDED -> LOST`： 因为连接重连后会话过期而丢失
- `SUSPENDED -> CONNECTED`： 丢失的连接重连成功

##### 只读连接(0.6版后加入)
zookeeper 3.4版加入`只读模式`的功能，要先在zookeeper服务器中启用此模式。  
在 kazoo 中，调用 KazooClient 时设置 `read_only` 为 `True`，这样客户端将连接到已经变为`只读`的节点，并且会继续扫描其他`读写`节点
```python
from kazoo.client import KazooClient

zk = KazooClient(hosts='127.0.0.1:2181', read_only=True)
zk.start()
```

KeeperState 添加了一个新属性 `CONNECTED_RO`. 之前提到的状态仍然有效，但是在 `CONNECTED` 时，需要检查状态是否为 `CONNECTED_RO`:
```python
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.client import KeeperState

zk = KazooClient()

@zk.add_listener
def watch_for_ro(state):
    if state == KazooState.CONNECTED:
        if zk.client_state == KeeperState.CONNECTED_RO:
            print("read only mode!")
        else:
            print("read/write mode")
```
注意将 `KazooState` 传给监听函数，只有通过与 `KeeperState` 对象比较才能判断

#### zookeeper 增删改查

kazoo 针对 zookeeper 对 znode 的增删改查提供了优雅的 API
##### 创建节点
方法:
- `ensure_path()`：可以递归的创建节点，但不能为节点设置数据，只能设置 ACL。 
- `create()`：创建节点并且可以设置数据以及监视功能，它需要一个已存在的路径，也可以传入`makepath=True`

```python
# 确认路径，如果不存在则创建
zk.ensure_path("/my/favorite")
# 创建节点并设置数据
zk.create("/my/favorite/node", b"a value")
```

##### 读取数据
方法:
- `exists()`： 检查节点是否存在
- `get()`： 获取节点数据以及 ZnodeStat 的详细节点信息
- `get_children()`： 获取节点的子节点列表
```python
#　判断节点是否存在
if zk.exists("/my/favorite"):
    pass

# 打印节点的数据和version
data, stat = zk.get("/my/favorite")
print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

# 子节点列表
children = zk.get_children("/my/favorite")
print("There are %s children with names %s" % (len(children), children))
```

##### 更新数据
方法：
- `set()`： 为指定节点更新数据。支持`version`选项， 在更新数据前会检查`version`是否匹配，如果不匹配，则不能更新数据并抛出`BadVersionError`错误。
```python
zk.set("/my/favorite", b"some data")
```

##### 删除数据
方法:
- `delete()`: 删除节点，支持递归删除选项(recursive=True)。支持`version`选项，在删除节点前会与节点的版本匹配，不匹配不会删除且抛出`BadVersionError`错误

```python
zk.delete("/my/favorite/node", recursive=True)
```

#### 重试指令
客户端与 zookeeper 服务器的连接可能会中断，默认情况下，kazoo 不会重连，将抛出一个异常。为了帮助解决这个问题，kazoo 提供了一个 `retry()` 辅助函数，
如果连接跑出异常，它将重试一个指令，例如:
```python
result = zk.retry(zk.get, "/path/to/node")
```
某些指令具有唯一性，不保证每个指令都会自动重试。例如，创建节点成功后连接丢失，这时再次重试的话会引发`NodeExistsError`错误。  
`retry()` 方法接受指令函数及其参数，因此可以将多个 zookeeper 指令传给它，以便在连接丢失的时候重试整个函数。  

下面是一个`kazoo`实现的 `锁`的例子，说明了如果重试去获得锁:
```python
# kazoo.recipe.lock snippet

def acquire(self):
    """Acquire the mutex, blocking until it is obtained"""
    try:
        self.client.retry(self._inner_acquire)
        self.is_acquired = True
    except KazooException:
        # if we did ultimately fail, attempt to clean up
        self._best_effort_cleanup()
        self.cancelled = False
        raise

def _inner_acquire(self):
    self.wake_event.clear()

    # make sure our election parent node exists
    if not self.assured_path:
        self.client.ensure_path(self.path)

    node = None
    if self.create_tried:
        node = self._find_node()
    else:
        self.create_tried = True

    if not node:
        node = self.client.create(self.create_path, self.data,
            ephemeral=True, sequence=True)
        # strip off path to node
        node = node[len(self.path) + 1:]
```
`create_tried` 记录判断 znode 在 连接中断以前是否已经创建。

##### 自定义重试
手动创建`KazooRetry`， 可以自定义特定的重试策略

```python
from kazoo.retry import KazooRetry

kr = KazooRetry(max_tries=3, ignore_expire=False)
result = kr(client.get, "/some/path")
```
这个例子将最多重试指令 3 次，并且在会话到期时会抛出异常。

#### Watcher(监视器)
kazoo 可以在节点上设置 watcher，节点或子节点发生变化时触发。  

可以通过两种方式设置 watcher， 第一种是 zookeeper 模式支持的一次性监听事件。不同于本机 zookeeper 监视器，这些监听函数会被 kazoo 调用一次并且不接收会话事件.
使用这种模式需要将监听函数传入下列某个函数:  
- get()
- get_children()
- exists()

当节点变化或被删除，传入`get()` 和 `exists()`的监听函数会被调用，并传给监听函数一个`WatchedEvent`对象 
```python
def my_func(event):
    # check to see what the children are now
    pass

# Call my_func when the children change
children = zk.get_children("/my/favorite/node", watch=my_func)
```

kazoo 提供了一个更高级的 API， 不需要每次触发事件使重新设置 watcher， 它不仅可以监听节点和子节点的变化，还可以查看 ZnodeStat。使用这个 API 注册
的监听函数在每次发生更改时都会立即调用，直到函数返回 False。 如果`allow_session_lost`设置为True，则会话丢失时将不再调用该函数。  
下列函数提供这种功能:
- ChildrenWatch
- DataWatch

这些类可以直接在 KazooClient 实例上使用，通过实例化任返回的实例可以直接调用，也允许它们用作装饰器:
```python
@zk.ChildrenWatch("/my/favorite/node")
def watch_children(children):
    print("Children are now: %s" % children)
# Above function called immediately, and from then on

@zk.DataWatch("/my/favorite")
def watch_node(data, stat):
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
```

#### 事务

zookeeper 3.4 开始允许一次发送多个命令，这些命令将作为一个原子操作，都成功或都失败。
```python
transaction = zk.transaction()
transaction.check('/node/a', version=3)
transaction.create('/node/b', b"a value")
results = transaction.commit()
```
`transaction()` 方法返回 `TransactionRequest` 实例，可以调用它提供的方法去排队在事务中要完成的命令。当事务准备好提交时调用`commit()`方法。
在上面的示例中，`check` 指令只在进行事务是有效，它可以检查 znode 的 version，如果 version 不匹配，事务就会失败。上面的例子表示:`只有在 /node/a 的 version 为 3 的时候，/node/b 才会被创建 `

### 异步用法

kazoo 异步 API 依赖所有异步方法返回的 `IAsyncResult` 对象。它可以使用 `rawlink()` 方法添加回调，像线程或gevent一样的工作方式。  
kazoo 使用插入式的 IHandler 接口，该接口抽象回调系统以确保一致的工作

#### 处理连接
创建连接:
```python
from kazoo.client import KazooClient
from kazoo.handlers.gevent import SequentialGeventHandler

zk = KazooClient(handler=SequentialGeventHandler())

# returns immediately
event = zk.start_async()

# Wait for 30 seconds and see if we're connected
event.wait(timeout=30)

if not zk.connected:
    # Not connected, stop trying to connect
    zk.stop()
    raise Exception("Unable to connect.")
```
在这个例子中，`wait()` 方法是 `start_async()` 方法返回的 `event` 对象上调用的。设置 `timeout` 选项可以优雅的处理无法连接的情况。
当使用 gevent 时应该使用 SequentialGeventHandler， 使用 eventlet 时使用 SequentialEventletHandler。kazoo 要求传入合适的处理程序，默认的处理程序是 SequentialThreadingHandler。
  
 
#### 异步回调
kazoo 所有的异步函数除了 `start_async()` 都会返回一个 `IAsyncResult` 实例，通过这些实例可以查看结果何时就绪，或者连接一个或多个回调函数到将要就绪的结果上。
回调函数将传递给 `IAsyncResult` 实例并调用 `get()` 方法获取值。如果异步函数遇到错误，调用 `get()` 会抛出一个异常，应该获取并处理这个异常
```python
import sys

from kazoo.exceptions import ConnectionLossException
from kazoo.exceptions import NoAuthException

def my_callback(async_obj):
    try:
        children = async_obj.get()
        do_something(children)
    except (ConnectionLossException, NoAuthException):
        sys.exit(1)

# Both these statements return immediately, the second sets a callback
# that will be run when get_children_async has its return value
async_obj = zk.get_children_async("/some/node")
async_obj.rawlink(my_callback)
```

#### zookeeper CURD
异步curd与同步curd工作方式相同，只是返回一个 `IAsyncResult` 对象

##### 新建
- create_async()

##### 读取
- exists_async()
- get_async()
- get_children_async()

##### 更新
- set_async()

##### 删除
- delete_async()

`ensure_path()` 目前没有异步方法对应，`delete_async()` 方法也不能进行递归删除。