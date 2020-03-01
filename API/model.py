from tinydb import TinyDB, Query, where


# class People
# prop name:string 姓名
# prop email:string 邮箱地址
# prop key:string Token
# prop number:string 手机号码
# prop status:int 状态：
#     0: 初始值
#     1: 已发提醒邮件
#     2: 已更新name
#     3: 已生成证书图片
#     4: 已发送证书邮件

def gen_token(seed):
    # pass
    return seed


def insert_people(email, number, name='', key=None):
    db = TinyDB("data.json")
    People = Query()
    if key:
        print('Warning: It is not safe to specify the key value. '
              'Just let it be None and it will be generated automatically')
    else:
        key = gen_token(email)
    db.insert({"name": name, "email": email, "key": key, "number": number, "status": 0})
    db.close()


def get_number(email):
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.email == email)
    db.close()
    return res[0]["number"]


def update_status(email):
    db = TinyDB("data.json")
    People = Query()
    db.update({'status': "1"}, where("email") == email)
    db.close()