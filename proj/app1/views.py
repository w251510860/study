from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from app1 import tasks
from django.shortcuts import HttpResponse
import time
import django.dispatch
from django.dispatch import receiver


# Create your views here.
def index(request, *args, **kwargs):
    res = tasks.add.delay(1, 3)

    # 任务逻辑
    return JsonResponse({'status': 'successful', 'task_id': res.task_id})


# 定义一个信号
work_done = django.dispatch.Signal(providing_args=['path', 'time'])


def create_signal(request):
    url_path = request.path
    print("我已经做完了工作。现在我发送一个信号出去，给那些指定的接收器。")

    # 发送信号，将请求的url地址和时间一并传递过去
    work_done.send(create_signal, path=url_path, time=time.strftime("%Y-%m-%d %H:%M:%S"))
    return HttpResponse("200,ok")


@receiver(work_done, sender=create_signal)
def my_callback(sender, **kwargs):
    print("我在%s时间收到来自%s的信号，请求url为%s" % (kwargs['time'], sender, kwargs["path"]))
