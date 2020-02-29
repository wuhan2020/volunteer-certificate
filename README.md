# volunteer-certificate
志愿者证书


### 获取token 接口：
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
### 生成idcard接口：

`http://localhost:5000/api/createIdCard`

```json
{
    "Token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiVXNlciIsInVzZXJfaWQiOiI1ZTVhMDhmMmVkMmZhNzBhMTJiNTIyZmYiLCJleHAiOjE1ODI5NjA2Mzl9.1-YngMcYcfF7NvL4PQpzNOua_p_V4VcQq6cup5LYigw",
    "Email":"nwljy111@yeah.net",
    "Name":"nwljy"
}
```

### 获取已经生成图片接口

`http://127.0.0.1:5000/api/getImage`

```json
{
    "Token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiVXNlciIsInVzZXJfaWQiOiI1ZTVhMDU2OTllOGRmNWVjMDc2ZDlhZWYiLCJleHAiOjE1ODI5NTk3MzV9.kcgtrvLVb3Z8GILkPm0iDWRhSY6LSc78u6Ey61T5GmA",
    "Email":"nwljy111@yeah.net",
    "Name":"nwljy",
    "ImageId":"5e5a0909ed2fa70a12b52304"
}
```

注意：除了获取token接口外 其他接口都是post
返回值都是：
失败：
```json
{"code":1,"message": "user not in server","data":""}//deta 没值
```
成功：
```json
{"code":0,"message": "111","data":"111"} //deta 有值
```
 post的Content-Type一定是application/json
