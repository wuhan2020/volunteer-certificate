# volunteer-certificate
志愿者证书

## xin 的设计见 https://github.com/wuhan2020/volunteer-certificate/blob/master/README.md




### 1.获取token 接口：（应该是在后端统一脚本发邮件，这个接口不需要暴露给前端）
`http://127.0.0.1:5000/api/getUserToken/nwljy/nwljy111@yeah.net`
### 成功：
```json
{
    "code": 0,
    "data": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiVXNlciIsInVzZXJfaWQiOiI1ZTVhNzY2YTJiZWIxYjkyNzhkMWMzMGMiLCJleHAiOjE1ODI5ODg3NjB9.AkAWKkca3BqIFHNiqM8Cw9C1fX-ujyfZNS83T4tIu5U",
    "message": "sucess"
}
```
### 错误
```json
{
    "code": 1,
    "data": "",
    "message": "user not in server"
}
```
### 2.生成idcard接口：

`http://localhost:5000/api/createIdCard`

```json
{
    "Token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiVXNlciIsInVzZXJfaWQiOiI1ZTVhMDhmMmVkMmZhNzBhMTJiNTIyZmYiLCJleHAiOjE1ODI5NjA2Mzl9.1-YngMcYcfF7NvL4PQpzNOua_p_V4VcQq6cup5LYigw",
    "Email":"nwljy111@yeah.net",
    "Name":"nwljy"
}
```

### 3.获取已经生成图片接口

`http://127.0.0.1:5000/api/getImage`

```json
{
    "Token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1
