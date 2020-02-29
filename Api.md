# volunteer-certificate
志愿者证书


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

 

 

