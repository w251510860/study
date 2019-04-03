celer练习
---
### 1、启动celery
```bash
celery -A cele worker --loglevel=info
```
查看配置信息
```terminal
 -------------- celery@bogon v4.2.1 (windowlicker)
---- **** ----- 
--- * ***  * -- Darwin-18.2.0-x86_64-i386-64bit 2019-04-03 11:32:16
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         cele:0x10eccf518
- ** ---------- .> transport:   redis://localhost:6379/4
- ** ---------- .> results:     redis://localhost:6379/5
- *** --- * --- .> concurrency: 8 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . cele.add

[2019-04-03 11:32:16,419: INFO/MainProcess] Connected to redis://localhost:6379/4
[2019-04-03 11:32:16,434: INFO/MainProcess] mingle: searching for neighbors
[2019-04-03 11:32:17,470: INFO/MainProcess] mingle: all alone
[2019-04-03 11:32:17,506: INFO/MainProcess] celery@bogon ready.
```
其中:
- app 是 worker 对应的应用名
- transport 是指在前面制定的消息队列地址 
- results 是指 任务执行结果存储的地方，如果这里没有指定，默认是关闭的。
- concurrency 是 worker 的数量，默认和处理器的核心数相同。

### 2、另外开启一个终端,进入python shell
```terminal
Python 3.6.7 (default, Mar 29 2019, 19:19:40) 
[GCC 4.2.1 Compatible Apple LLVM 10.0.0 (clang-1000.11.45.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from cele import add
>>> add
<@task: cele.add of cele at 0x1085f0470>
>>> add.delay(1, 2)
<AsyncResult: 38d41789-d6ae-4c2d-90ab-459e21486542>
>>> f =  add.delay(1, 2)
>>> f
<AsyncResult: ebb8dbd5-43dc-4038-b87b-a6faa6be2a2c>
>>> f.status
'SUCCESS'
>>> f.result
3
>>> 
```
###3.celery配置
可以直接在内部配置
```python
from celery import Celery
app = Celery('cele', broker='redis://localhost:6379/4', backend='redis://localhost:6379/5')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
)
```
也可以使用config.py
```python
from celery import Celery
app = Celery('cele', broker='redis://localhost:6379/4', backend='redis://localhost:6379/5')
app.config_from_object('config')
```
### 4、使用定时任务

可以通过在配置文件中编写 beat_schedule 属性，来配置周期性任务，上面的示例配置了一个每十秒执行一次的周期任务，任务为 cele.add，参数为 (3, 4)。当然你也可以将这个配置写到单独的配置文件中进行读取。这种配置的方式可以支持多个参数
- task： 指定任务的名字
- schedule : 设定任务的调度方式，可以是一个表示秒的整数，也可以是一个 timedelta 对象，或者是一个 crontab 对象（后面介绍），总之就是设定任务如何重复执行
- args： 任务的参数列表
- kwargs：任务的参数字典
- options：所有 apply_async 所支持的参数

启动beat命令(-B):
```bash
celery -A cele worker -l info -B
```
查看终端，每10秒执行一次

### 5、Celery的任务

任务是 Celery 里不可缺少的一部分，它可以是任何可调用对象。每一个任务通过一个唯一的名称进行标识， worker 通过这个名称对任务进行检索。任务可以通过 app.task 装饰器进行注册，需要注意的一点是，当函数有多个装饰器时，为了保证 Celery 的正常运行，app.task 装饰器需要在最外层。
```python
@app.task
@decorator1
@decorator
def say(world):
    print(world)
```
app.task装饰器可以传入参数，可以通过 name 显式的设定任务的名字，serializer 设定任务的序列化方式,另外bind比较常用,当设置了bind参数，则会为这个任务绑定一个Task实例，通过第一个 self 参数传入，可以通过这个 self 参数访问到 Task 对象的所有属性
```python
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
@app.task(bind=True)
def sum_a_b(self, x, y):
    logger.info(f'self.request.id -> {self.request.id}')
    return x + y
```
执行结果:
```bash
[2019-04-03 14:00:52,205: INFO/Beat] Scheduler: Sending due task 10-seconds (cele.sum_a_b)
[2019-04-03 14:00:52,273: INFO/MainProcess] Received task: cele.sum_a_b[a608aed4-d63e-4cf6-8808-120e849d3a80]  
[2019-04-03 14:00:52,277: INFO/ForkPoolWorker-9] cele.sum_a_b[a608aed4-d63e-4cf6-8808-120e849d3a80]: self.request.id -> a608aed4-d63e-4cf6-8808-120e849d3a80
[2019-04-03 14:00:52,290: INFO/ForkPoolWorker-9] Task cele.sum_a_b[a608aed4-d63e-4cf6-8808-120e849d3a80] succeeded in 0.013145555996743497s: 7
```
### 6、任务执行

可以通过 delay 使用 Celery 执行一个任务，实际上 delay 是 apply_async 的一个快捷方式，而相较于 delay，apply_aysnc 支持对于任务执行过程的更精确的控制。
```python
>>> f = cele.add.apply_async((1,2), countdown=10)
>>> f.state
'PENDING'
>>> f.state
'SUCCESS'
>>> f.result
3
```
其中第一个参数就是传入add方法的值,countdown表示延时执行.函数原型如下:
```python
task.apply_async(args[, kwargs[, …]])
```
其中 args 和 kwargs 分别是 task 接收的参数，当然它也接受额外的参数对任务进行控制。除此 countdown 之外，可以通过 expires 设置任务过期时间，当 worker 接收到一个过期任务，它的状态会标记为 REVOKE；也可以通过设置 retry=True，在任务执行失败时进行重试。

对于未注册的函数，可以调用 Task 对象的 send_task 方法向任务队列添加一个任务，通过 name 参数设定任务名进行标识，和 apply_aysnc 一样返回一个 AsyncResult 对象。

所以总结一下，在 Celery 中执行任务的方法一共有三种： 
1. delay， 用来进行最简单便捷的任务执行； 
2. apply_async， 对于任务的执行附加额外的参数，对任务进行控制； 
3. app.send_task， 可以执行未在 Celery 中进行注册的任务。

### 7、任务的链式执行

在 Celery 中，可以通过调用 apply_async 时传递 link 参数设置任务执行完成后的后续任务，当然这个任务也会由 Celery 交给 worker 执行。这里有一点需要注意，任务执行的返回值将会以参数的形式传递给这个后续任务，而这里的后续任务需要是一个 signature 对象。下面的例子等价于 add(add(3, 4), 5)
```python
>>> f = add.apply_async((3, 4), link=add.s(5))
```
```bash
9-04-03 14:23:02,845: INFO/MainProcess] Received task: cele.add[da3653b0-6801-487b-ab91-49d7d84af771]  
[2019-04-03 14:23:05,852: INFO/MainProcess] Received task: cele.add[ff200a14-709c-4546-b470-35c13bc1d0c6]  
[2019-04-03 14:23:05,852: INFO/ForkPoolWorker-8] Task cele.add[da3653b0-6801-487b-ab91-49d7d84af771] succeeded in 3.005446976996609s: 7
[2019-04-03 14:23:08,855: INFO/ForkPoolWorker-2] Task cele.add[ff200a14-709c-4546-b470-35c13bc1d0c6] succeeded in 3.00184818499838s: 12
```
### 8、工作流
实际使用过程中，可能需要处理大量有关或无关的任务，所以 Celery 提供了一组函数，用来对任务执行流程进行控制。而其中的基本任务单元就是前面提到的 signature 对象。

#### 8.1 chain - 任务的链式执行
chain 函数接受一个任务的列表，Celery 保证一个 chain 里的子任务会依次执行，在 AsynResult 上执行 get 会得到最后一个任务的返回值。和 link 功能类似，每一个任务执行结果会当作参数传入下一个任务，所以如果你不需要这种特性，采用 immutable signature 来取消。
```python
>>> from cele import add
>>> from celery import chain
>>> r = chain(add.s(1,2), add.s(3), add.s(4))
>>> r().get()10
```
```bash
[2019-04-03 14:41:25,070: INFO/MainProcess] Received task: cele.add[10ff63ac-6ab0-4b0c-986b-b19104a6a243]  
[2019-04-03 14:41:28,128: INFO/MainProcess] Received task: cele.add[0ffce8b7-7729-47ab-ac9d-3d98db8dacb5]  
[2019-04-03 14:41:28,133: INFO/ForkPoolWorker-8] Task cele.add[10ff63ac-6ab0-4b0c-986b-b19104a6a243] succeeded in 3.0562840409984346s: 3
[2019-04-03 14:41:31,185: INFO/MainProcess] Received task: cele.add[8f0380f8-9ee7-4b6c-95cd-31c774b80b99]  
[2019-04-03 14:41:31,189: INFO/ForkPoolWorker-2] Task cele.add[0ffce8b7-7729-47ab-ac9d-3d98db8dacb5] succeeded in 3.0580888880031125s: 6
[2019-04-03 14:41:34,204: INFO/ForkPoolWorker-4] Task cele.add[8f0380f8-9ee7-4b6c-95cd-31c774b80b99] succeeded in 3.016101899000205s: 10
```
#### 8.2 group - 任务的并发执行
group 函数也接受一个任务列表，这些任务会同时加入到任务队列中，且执行顺序没有任何保证。在 AsynResult 上执行 get 会得到一个包含了所有返回值的列表。
```python
>>> r = group(add.s(1,2), add.s(3,4), add.s(4,5))
>>> r().get()
[3, 7, 9]
```
```bash
[2019-04-03 14:47:19,869: INFO/MainProcess] Received task: cele.add[f809abe6-7653-4d99-b733-462ffef194c4]  
[2019-04-03 14:47:19,873: INFO/MainProcess] Received task: cele.add[1f619668-0a54-4ae2-8114-500b8505dad0]  
[2019-04-03 14:47:19,875: INFO/MainProcess] Received task: cele.add[90f4ffaf-79c9-4ab1-978e-ba0d5ea6c334]  
[2019-04-03 14:47:22,886: INFO/ForkPoolWorker-8] Task cele.add[f809abe6-7653-4d99-b733-462ffef194c4] succeeded in 3.007032347999484s: 3
[2019-04-03 14:47:22,902: INFO/ForkPoolWorker-1] Task cele.add[1f619668-0a54-4ae2-8114-500b8505dad0] succeeded in 3.021867982999538s: 7
[2019-04-03 14:47:22,905: INFO/ForkPoolWorker-3] Task cele.add[90f4ffaf-79c9-4ab1-978e-ba0d5ea6c334] succeeded in 3.0250510959995154s: 9
```
#### 8.3 chord - 带回调的 group
chord 基本功能和 group 类似，只是有一个额外的回调函数。回调函数会在前面的任务全部结束时执行，其参数是一个包含了所有任务返回值的列表。在 AsynResult 上执行 get 会得到回调函数的返回值。
```python
# 首先定义sum_result函数
@app.task
def sum_result(values):
    return sum(values)
    
# 执行python shell
>>> from celery import chord
>>> from cele import add
>>> from cele import sum_result
>>> r = chord((add.s(i, i) for i in range(10)), sum_result.s())
>>> r().get()
90
```
```bash
[2019-04-03 14:53:23,173: INFO/MainProcess] Received task: cele.add[291186ba-d0ea-48ca-9d83-c8895dd14106]  
[2019-04-03 14:53:23,177: INFO/MainProcess] Received task: cele.add[9bdfd3b7-ed3c-4612-997f-c59c2d87deb1]  
[2019-04-03 14:53:23,178: INFO/MainProcess] Received task: cele.add[a3f58ef4-72a7-48f6-81f6-8d6d3b8baf2b]  
[2019-04-03 14:53:23,179: INFO/MainProcess] Received task: cele.add[cf6f7b20-08ee-4685-98f4-c5ba9e74db55]  
[2019-04-03 14:53:23,181: INFO/MainProcess] Received task: cele.add[48063fce-b165-4733-b47b-1834a2ef8f58]  
[2019-04-03 14:53:23,183: INFO/MainProcess] Received task: cele.add[6017c347-46d2-4c5c-9bb8-7bfb8bdf4dbc]  
[2019-04-03 14:53:23,185: INFO/MainProcess] Received task: cele.add[4e6ddc70-23b8-4583-b090-313c32ec020f]  
[2019-04-03 14:53:23,187: INFO/MainProcess] Received task: cele.add[4435df86-b62c-405c-9999-cd87fd03bdc1]  
[2019-04-03 14:53:23,190: INFO/MainProcess] Received task: cele.add[dfd55412-868c-4333-a9c7-52fdcfce92f7]  
[2019-04-03 14:53:23,191: INFO/MainProcess] Received task: cele.add[31c9f54d-582b-4065-88d7-6d2724f67e04]  
[2019-04-03 14:53:26,209: INFO/ForkPoolWorker-8] Task cele.add[291186ba-d0ea-48ca-9d83-c8895dd14106] succeeded in 3.02926247600044s: 0
[2019-04-03 14:53:26,215: INFO/ForkPoolWorker-1] Task cele.add[9bdfd3b7-ed3c-4612-997f-c59c2d87deb1] succeeded in 3.0341229700024996s: 2
[2019-04-03 14:53:26,233: INFO/ForkPoolWorker-6] Task cele.add[48063fce-b165-4733-b47b-1834a2ef8f58] succeeded in 3.04575261699938s: 8
[2019-04-03 14:53:26,235: INFO/ForkPoolWorker-4] Task cele.add[cf6f7b20-08ee-4685-98f4-c5ba9e74db55] succeeded in 3.0515222889989673s: 6
[2019-04-03 14:53:26,235: INFO/ForkPoolWorker-7] Task cele.add[6017c347-46d2-4c5c-9bb8-7bfb8bdf4dbc] succeeded in 3.0473983810006757s: 10
[2019-04-03 14:53:26,236: INFO/ForkPoolWorker-3] Task cele.add[a3f58ef4-72a7-48f6-81f6-8d6d3b8baf2b] succeeded in 3.052023955999175s: 4
[2019-04-03 14:53:26,244: INFO/ForkPoolWorker-2] Task cele.add[4435df86-b62c-405c-9999-cd87fd03bdc1] succeeded in 3.0522270219989878s: 14
[2019-04-03 14:53:26,244: INFO/ForkPoolWorker-5] Task cele.add[4e6ddc70-23b8-4583-b090-313c32ec020f] succeeded in 3.053115093996894s: 12
[2019-04-03 14:53:29,216: INFO/ForkPoolWorker-8] Task cele.add[dfd55412-868c-4333-a9c7-52fdcfce92f7] succeeded in 3.0030292000010377s: 16
[2019-04-03 14:53:29,269: INFO/ForkPoolWorker-1] Task cele.add[31c9f54d-582b-4065-88d7-6d2724f67e04] succeeded in 3.050735311997414s: 18
[2019-04-03 14:53:29,269: INFO/MainProcess] Received task: cele.sum_result[9a9eb1c2-7ff3-497c-a3a4-19dee625abd4]  
[2019-04-03 14:53:29,272: INFO/ForkPoolWorker-3] Task cele.sum_result[9a9eb1c2-7ff3-497c-a3a4-19dee625abd4] succeeded in 0.0007041489989205729s: 90
```
#### 8.4 chunks - 将大量任务分解为小块任务
chunks 是在 app.task 对象上的方法，它将多个任务分成几块执行，每一块是一个单独的任务由一个 worker 执行。
```python
>>> from celery import chunks
>>> add.chunks(zip(range(100), range(100)), 10)().get()
[[0, 2, 4, 6, 8, 10, 12, 14, 16, 18], [20, 22, 24, 26, 28, 30, 32, 34, 36, 38], [40, 42, 44, 46, 48, 50, 52, 54, 56, 58], [60, 62, 64, 66, 68, 70, 72, 74, 76, 78], [80, 82, 84, 86, 88, 90, 92, 94, 96, 98], [100, 102, 104, 106, 108, 110, 112, 114, 116, 118], [120, 122, 124, 126, 128, 130, 132, 134, 136, 138], [140, 142, 144, 146, 148, 150, 152, 154, 156, 158], [160, 162, 164, 166, 168, 170, 172, 174, 176, 178], [180, 182, 184, 186, 188, 190, 192, 194, 196, 198]]
```
```bash
[2019-04-03 14:56:29,696: INFO/MainProcess] Received task: celery.starmap[3051696a-3aa4-49a6-83c7-0d4019dcefb2]  
[2019-04-03 14:56:29,703: INFO/MainProcess] Received task: celery.starmap[0bc2a312-4c00-4267-9979-1bd46594db40]  
[2019-04-03 14:56:29,705: INFO/MainProcess] Received task: celery.starmap[fad8a12b-6517-44fa-a164-a7cb0bbb4b3c]  
[2019-04-03 14:56:29,706: INFO/MainProcess] Received task: celery.starmap[3a4d5e1a-07fc-49f0-ad3f-5ab7babf808f]  
[2019-04-03 14:56:29,708: INFO/MainProcess] Received task: celery.starmap[bf6a3e54-241b-4ddc-bf8a-a904bb72e49c]  
[2019-04-03 14:56:29,711: INFO/MainProcess] Received task: celery.starmap[f9e28bc7-68c5-436c-8d3d-363319e387ff]  
[2019-04-03 14:56:29,713: INFO/MainProcess] Received task: celery.starmap[949ae6d5-3a1e-4bad-997b-46a2fe6b4ac6]  
[2019-04-03 14:56:29,714: INFO/MainProcess] Received task: celery.starmap[16ef9bfb-a7ae-472d-a978-70428f4e5d3f]  
[2019-04-03 14:56:29,716: INFO/MainProcess] Received task: celery.starmap[ad249ca6-6255-4a3d-baac-7a7f0b7b32aa]  
[2019-04-03 14:56:29,718: INFO/MainProcess] Received task: celery.starmap[79f2a98c-0d6d-4d91-9ce6-c86ce1a77366]

```
程序代码参考 [烟火君博客](https://blog.csdn.net/preyta/article/list/2?t=1)