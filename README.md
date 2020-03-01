# volunteer-certificate
# 安装并启动项目：

见：https://github.com/wuhan2020/volunteer-certificate/tree/master/API

# 志愿者证书

## 一、前端接口


### 1.通过token获取用户信息
类型：get请求 

`http://127.0.0.1:5000/api/getUserInfo?token=dsfasgdafgaggsdagdsg`

#### 成功：
```json
{
  "code": 0,
  "data": {
      "Email":"xxxx@yeah.net",                  //邮箱,在页面不可以编辑
      "Name":"xxxxx",                           //称呼
   },
   "message": "sucess"
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

`http://localhost:5000/api/submitUserinfo`

类型：post请求  post的Content-Type一定是application/json

入参

```json
{
    "Token":"dsfasgdafgaggsdagdsg",  // token
    "Name":"new namw"                //修改后的称呼
}
```

结果
#### 成功：
```json
   {
      "code":0,      // 成功
      "message": "",
      "data":null
   }
```
#### 失败：
```json
   {
      "code":1,   // 失败
      "message": "网络异常",
      "data":null    
   }
```

 ### 3.添加新用户（管理员）
 `http://127.0.0.1:5000/api/addUserData`

## 二、数据表

按照github 拼音顺序进行排列

| 字段                                                  | 类型                                                | 名称   | 描述                                      |
| ----------------------------------------------------- | ---------- | ------------------------------------------- | ------------ |
| id         | 整型    | 自增主键 |       |
| token | 字符型 | 验证码 | 因为没有用户权限系统，所以用token作为本次活动权限标识 |
| name       | 字符型    | 称呼 |    |
| email            | 字符型         | 产品&&设计 |     |
| pic_url        | 字符型     | 生成证书图片名称 |     |
| status           | 整型        | 状态   | 0：初始化 1 已经发送提醒邮件 2：用户已提交 3：图片已经生成 4：邮件已发出 |

## 三、数据流
 ### 第1步. 后端项目批量给用户邮箱发邮件
   将为当前邮箱状态为0的邮箱生成token（可以定时任务扫描），并更新本行记录的token为新token
   每个邮件的关键内容为确认称呼的ur：
`https://community.wuhan2020.org.cn/volunteer/update-name.html?token=dsfasgdafgaggsdagdsg`

邮件发送完毕后，状态置为 1

 ### 第2步. 用户打开网页
 调用接口**1.通过token获取用户信息**展示数据

 ### 第3步. 用户修改并提交数据

 调用接口**2.用户提交信息：**提交到后端
 
  ### 第4步. 后端服务生成图片，发送邮件
  #### 后端更新本行记录：name 为新称呼，状态置为 2
  #### 调用生成图片接口，更新pic_url，更新status 为3
  #### 调用发邮件接口 更新status 为4
  
  状态2后每一次断掉可以重试（定时任务扫描）
  
