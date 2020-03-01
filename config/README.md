
<!--
 * @Editors: Muxxs
 -->
# How to build test environment
## Dependency Installation
```shell
python3 -m pip install --user -r requirements.txt
```
## Extra data file
You need to put `data.json`, `pic.jpg` in the project root directory.
```shell
cp config/data.json ./
```
Optionally you can make a file `email.json` and edit the configuration.
```shell
cp config/email.json.config email.json
```
To start the server, run the following command in project root directory
```shell
python3 app.py
```
To test whether the server works, you can use `curl`
```shell
curl -X POST -d '{"key":"key1", "email":"your_email", "name":"your_name"}' http://127.0.0.1:5000/send
```
# 证书API使用文档



### **1、验证Key**

### 地址：

    http://url/key

    method=POST json

KEY是每个证书生成的依据，每个人一个KEY，根据KEY打开自己独有的URL。

#### Data Map:

字段  | 说明
-----|-----
key  | 用户提交url时的key



#### 返回值表:

#### 成功：
```json
{
  "code": 0,
  "data": {
      "email":"xxxx@yeah.net",                  //邮箱,在页面不可以编辑
      "name":"xxxxx",                           //称呼
   },
   "message": "success"
}
```

#### 失败
```json
{
    "code": 1,
    "data": "",
    "message": "user not in server"
}
```

---
### **2、生成并发送证书**

### 地址：

    http://url/send

    method=POST json


字段  | 说明
-----|-----
email| 用户提交的email
name | 用户提交的要生成证书的姓名
key  | 用户所使用的key


#### 返回值表:

返回值  | 说明
-------|-----
0      | Key验证错误
2      | 图片制作成功、邮件发送成功
3      | Key已经被使用过
4      | 邮箱地址有误（功能正在完善）
5      | 图片生成或邮箱发送有误（极端情况，目前没出现过。）
