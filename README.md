# volunteer-certificate
![Python application](https://github.com/wuhan2020/volunteer-certificate/workflows/Python%20application/badge.svg)
# 安装并启动项目(How to build dev environment):
## Dependency Installation
```shell
python3 -m pip install --user -r requirements.txt
```
## Startup shell

You can use shell script to start or stop the application 
```shell script
cd volunteer-certificate
# start up
./bin/start.sh

# shutdown
./bin/stop.sh

# restart
./bin/restart.sh
```

## Extra data file
You need to put `data.json`, `pic.jpg` in the project root directory.
```shell
cp config/data.json ./
```
Optionally you can make a file `email.json` from the template `config/email.json.config` and edit the configuration; make a file `org.json` from the template `config/org.json.config` and edit the configuration.

To start the server, run the following command in project root directory
```shell
python3 app.py
```
To test whether the server works, you can use `curl`
```shell
curl http://localhost:5000/api/getUserInfo?token=token0
```
# 志愿者证书

## 一、前端接口


### 1.通过token获取用户信息
类型：get请求 

`/api/getUserInfo?token=dsfasgdafgaggsdagdsg`

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
### 2. 用户提交信息：

`/api/submitUserInfo`


入参

```json
{
    "token":"dsfasgdafgaggsdagdsg",  // token
    "name":"new namw"                //修改后的称呼
}
```

结果同 1.
### 3.添加新名字（管理员）
 `/api/addUserData`
 入参

```json
{
    "token":"abc",  // admin-token
    "email":["foo@example.org"]
}
```

结果同 1.
### 4. Upload template image
 `/api/uploadImage`

Required Header:
```
Token: abc
Content-Type: multipart/form-data
```

name="template"
data="image raw content"

Json response, same format as 1.
### 5. Update configuration
`/api/updateOrgConfig`
```json
{
    "token":"abc",  // admin-token
    "name": "org_name",
    "website": "org_website",
    "name_horizontal_pos": "name_horizontal_pos",
    "name_vertical_pos": "name_vertical_pos",
    "email": {
        "username": "org_email_username",
        "password": "org_email_password"
      }
}
```
Json response, same format as 1.
### 6. Email query
`/api/email`
```json
{
   "token":"abc",
   "action": "send", // or query
}
```
Json response, same format as 1.
```
## 二、数据表


| 字段                                                  | 类型                                                | 名称   | 描述                                      |
| ----------------------------------------------------- | ---------- | ------------------------------------------- | ------------ |
| id         | 整型    | 自增主键 |       |
| token | 字符型 | 验证码 | 因为没有用户权限系统，所以用token作为本次活动权限标识，用uuid算法生成唯一串 |
| name       | 字符型    | 称呼 |    |
| email            | 字符型         | 邮箱 |     |
| number        | 字符型     | 证书编号 |  在数据源导入时候已经生成   |
| status           | 整型        | 状态   | 0：初始化 1 已经发送提醒邮件 2：用户已提交 3：图片已经生成 4：证书邮件已发出 |

## 三、数据流
### 第1步，活动组织者提交证书图片模板和相关参数
### 第2步，活动组织者提交组织相关信息、邮箱相关信息
### 第3步，活动组织者提交志愿者邮箱列表
### 第4步. 后端项目批量给用户邮箱发邮件
   将为当前邮箱状态为0的邮箱生成token，并更新本行记录的token为新token
发送邮件给志愿者，每个邮件的关键内容为一个带有 token 的链接，比如：
`https://community.wuhan2020.org.cn/zh-cn/certification/index.html?token=dsfasgdafgaggsdagdsg`

邮件发送完毕后，状态置为 1

### 第5步. 用户打开网页
 调用接口**1.通过token获取用户信息**展示数据

### 第6步. 用户修改并提交数据，证书发到用户邮箱

 调用接口**2.用户提交信息：**提交到后端
 
### 第7步. 后端服务生成图片，发送邮件
  #### 后端更新本行记录：name 为新称呼，状态置为 2
  #### 调用生成图片接口，更新pic_url，更新status 为3
  #### 调用发邮件接口 更新status 为4  
  状态2后每一次断掉可以重试

### 第8步，活动组织者通过指定接口查询用户邮件发送的状态
  比如还有多少封邮件没发完
