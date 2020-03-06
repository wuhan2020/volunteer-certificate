from tinydb import TinyDB, Query, where


# class People
# prop name:string 姓名
# prop email:string 邮箱地址
# prop token:string Token
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


def insert_people(email, name, number='', token=None):
    db = TinyDB("data.json")
    People = Query()
    exist_list = db.search(People.email == email)
    if len(exist_list):
        raise KeyError('Duplicate entry for key email')
    if token:
        print('Warning: It is not safe to specify the token value. '
              'Just let it be None and it will be generated automatically')
    else:
        token = gen_token(email)
    db.insert({"name": name, "email": email, "token": token, "number": number, "status": 0})
    db.close()


def get_number(email):
    db = TinyDB("data.json")
    People = Query()
    res = db.search(People.email == email)
    db.close()
    return res[0]["number"]


def update_status(email, status=1):
    db = TinyDB("data.json")
    People = Query()
    db.update({'status': status}, where("email") == email)
    db.close()

def update_status_and_token(email, status=1, token=""):
    db = TinyDB("data.json")
    People = Query()
    db.update({'status': status,'token': token}, where("email") == email)
    db.close()
