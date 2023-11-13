import sentry_sdk

sentry_sdk.init(
    dsn="https://20e970bb8e56bb1008408177647fd700@o4506190326071296.ingest.sentry.io/4506190445674496",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
# 捕捉异常平台

from threading import Thread
import time
import datetime

from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix


import utils



app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

ip_list = []
is_over = False


def clear_ip(t=1):
    global ip_list
    while True:
        if is_over:
            break
        ip_list.clear()
        time.sleep(t)


Thread(target=clear_ip).start()


@app.route("/", methods=["GET", "POST"])
def index():
    if ip_list.count(request.remote_addr) > 100:
        return "", 403
    if ip_list.count(request.remote_addr) > 20:
        ip_list.append(request.remote_addr)
        return "访问次数过多 请稍后再试"
    ip_list.append(request.remote_addr)

    if request.method == "POST":
        try:
            query = request.form["search_query"]
        except KeyError:
            query = ""
        results = utils.search(query)
        if query.strip() == '' or query is None or "这是来自「WakeUp课程表」的课表分享" in query:
            return render_template("index.html", msg="请输入班级")
        print(
            f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 某人搜索了 {query} 他的IP {request.remote_addr}")
        with open("search.log", "a", encoding="utf-8") as f:
            f.write(
                f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 某人搜索了 {query} 他的IP {request.remote_addr}\n")
        return render_template("index.html", results=results)
    return render_template("index.html", results=False, index=True)


# 渲染生成代码的页面
@app.route('/generate_code', methods=['GET'])
def generate_code():
    if ip_list.count(request.remote_addr) > 100:
        return "", 403
    if ip_list.count(request.remote_addr) > 20:
        ip_list.append(request.remote_addr)
        return "访问次数过多 请稍后再试"
    for i in range(5):
        ip_list.append(request.remote_addr)

    result = request.args.get('result')
    result = utils.get_course(result)
    return render_template('generate_code.html', result=result)


if __name__ == "__main__":
    app.run(debug=False)
    print("运行结束")
    is_over = True
