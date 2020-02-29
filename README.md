# volunteer-certificate
志愿者证书


### 获取token 接口：
`http://127.0.0.1:5000/api/getUserToken/nwljy/nwljy111@yeah.net`

### 生成idcard接口：

`http://localhost:5000/api/createIdCard`

```
{
    “Token”:”eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiVXNlciIsInVzZXJfaWQiOiI1ZTVhMDhmMmVkMmZhNzBhMTJiNTIyZmYiLCJleHAiOjE1ODI5NjA2Mzl9.1-YngMcYcfF7NvL4PQpzNOua_p_V4VcQq6cup5LYigw”,
    “Email”:”nwljy111@yeah.net”,
    “Name”:”nwljy”
}
```

### 获取已经生成图片接口

`http://127.0.0.1:5000/api/getImage`

```
{
    “Token”:”eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiVXNlciIsInVzZXJfaWQiOiI1ZTVhMDU2OTllOGRmNWVjMDc2ZDlhZWYiLCJleHAiOjE1ODI5NTk3MzV9.kcgtrvLVb3Z8GILkPm0iDWRhSY6LSc78u6Ey61T5GmA”,
    “Email”:”nwljy111@yeah.net”,
    “Name”:”nwljy”,
    “ImageId”:”5e5a0909ed2fa70a12b52304”
}
```

注意：除了获取token接口外 其他接口都是post
