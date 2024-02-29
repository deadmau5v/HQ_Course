import datetime

import requests
from fake_useragent import UserAgent
import os

path = "./data"

dataSet = list(map(lambda x: x.replace(".wakeup_schedule", ""), os.listdir(path)))


def search(query):
    query = query.replace("班", "")

    res = {}
    for i in dataSet:
        num = 0
        if i[0] == query[0]:
            num += 4

        for word in query:

            if word in i:
                if word.isdigit():
                    num += 1
                else:
                    num += 5

            if num != 0:
                res[i] = num
    res = sorted(res.items(), key=lambda x: x[1], reverse=True)
    res = filter(lambda x: x[1] > 9, res)
    return [i[0] for i in res]


class CourseCode:
    def __init__(self):
        self.code = None
        self.time = None
        self.classes = None


allCourseCode: list[CourseCode] = []


def get_course(name):
    if not os.path.exists(f"{path}/{name}.wakeup_schedule"):
        return "不存在该班级信息"

    for i in allCourseCode:
        if i.classes == name and (datetime.datetime.now() - i.time).seconds < 1700:
            return (f"这是来自「WakeUp课程表」的课表分享，30分钟内有效哦，如果"
                    f"失效请再获取一次叭。为了保护隐私我们选择不监听你的剪贴板，"
                    f"请复制这条消息后，打开【WakeUp】的主界面，右上角第二个按钮 -> 从分享口"
                    f"令导入，按操作提示即可完成导入~分享口令为「{i.code}」")
        if i.classes == name and (datetime.datetime.now() - i.time).seconds > 1700:
            allCourseCode.remove(i)

    with open(f"{path}/{name}.wakeup_schedule", "r", encoding="utf-8") as f:
        file = f.read()

    headers = {"User-Agent": UserAgent().random,
               "Host": "i.wakeup.fun",
               "version": "238"}
    r = requests.post(url="https://i.wakeup.fun/share_schedule", headers=headers, data={"schedule": file})
    code = r.json()['data']
    data = (f"这是来自「WakeUp课程表」的课表分享，30分钟内有效哦，如果"
            f"失效请再获取一次叭。为了保护隐私我们选择不监听你的剪贴板，"
            f"请复制这条消息后，打开【WakeUp】的主界面，右上角第二个按钮 -> 从分享口"
            f"令导入，按操作提示即可完成导入~分享口令为「{code}」")
    c = CourseCode()
    c.time = datetime.datetime.now()
    c.code = code
    c.classes = name
    allCourseCode.append(c)
    return data
