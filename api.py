from threading import Thread
import time
import datetime
import icons

from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

import utils

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            query = request.form["search_query"]
        except KeyError:
            query = ""
        try:
            results = utils.search(query)
        except IndexError:
            return render_template("index.html", results=False, index=True)
        results = [(i, icons.get_icons(i)) for i in results]
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
    result = request.args.get('result')
    result = utils.get_course(result)
    return render_template('generate_code.html', result=result)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    print("运行结束")
