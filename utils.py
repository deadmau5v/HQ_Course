import requests
from fake_useragent import UserAgent
import os

data = os.listdir("data")
data = [i.split(".")[0] for i in data]


def search(query):
    results = [item for item in data if query in item]
    return results


def get_course(name):
    if not os.path.exists(f"data/{name}.wakeup_schedule"):
        return "不存在该班级信息"
    file = ""
    with open(f"data/{name}.wakeup_schedule", "r", encoding="utf-8") as f:
        for i in f.readlines():
            file += i
    headers = {"User-Agent": UserAgent().random,
               "Host": "i.wakeup.fun",
               "version": "238"}
    r = requests.post(url="https://i.wakeup.fun/share_schedule", headers=headers, data={"schedule": file})
    data = (f"这是来自「WakeUp课程表」的课表分享，30分钟内有效哦，如果"
            f"失效请再获取一次叭。为了保护隐私我们选择不监听你的剪贴板，"
            f"请复制这条消息后，打开【WakeUp】的主界面，右上角第二个按钮 -> 从分享口"
            f"令导入，按操作提示即可完成导入~分享口令为「{r.json()['data']}」")
    return data
