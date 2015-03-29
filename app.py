# coding: utf8

import re

from flask import Flask, request, render_template
from dbmixin import DBMixin

app = Flask(__name__)
app.debug = True

# db & collection
db = DBMixin().db
topic_collection = db.result_topic
page_collection = db.result_page

@app.route("/", methods=["GET", "POST"])
def index():
    """index
    """
    keyword = request.form.get("keyword", "")
    is_order_update_time = int(request.form.get(
        "is_order_update_time", 0))
    where = {}
    if keyword:
        regx = re.compile(".*%s.*" % keyword, re.IGNORECASE)
        where["title"] = {"$regex": regx}
    # 更新时间排序
    if is_order_update_time:
        topics = page_collection.find(where) \
            .sort([("last_update_time", -1)]).limit(300)
    else:
        topics = topic_collection.find(where) \
            .sort([("order_by", -1)]).limit(300)
    return render_template(
        "index.html",
        topics=topics,
        is_order_update_time=is_order_update_time,
        keyword=keyword)

if __name__ == "__main__":
    app.run()
