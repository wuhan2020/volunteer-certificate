from tinydb import TinyDB, Query, where


# class People
# prop name:string 姓名
# prop email:string 邮箱地址
# prop key:string Token
# prop number:string 手机号码
# prop use:int 状态：
#     0: 初始值
#     1: 已发提醒邮件
#     2: 已更新name
#     3: 已生成证书图片
#     4: 已发送证书邮件


def insert_db(name, email, key, number):
    db = TinyDB("data.json")
    People = Query()
    db.insert({"name": name, "email": email, "key": key, "number": number, "use": 0})
    db.close()


def get_number(email):
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.email == email)
    db.close()
    return res[0]["number"]


def update_use(email):
    db = TinyDB("data.json")
    People = Query()
    db.update({'use': "1"}, where("email") == email)
    db.close()