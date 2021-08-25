# 简单TG视频上传脚本


## 效果
逐个上传指定文件夹内（子文件夹的除外）的所有mp4视频  
并自定义视频封面(随机时间)  
到指定的群组/频道  
以视频命名为文字说明  


## 环境
- `python 3.9+`
- `Pyrogram`
- `ffmpeg`

## 安装教程
下载安装`python 3.9+`和`ffmpeg`   
还有本项目的`tgup.py`  
再安装`pyrogram`
```
pip3 install pyrogram
```


## 创建TG API
-官方教程  
https://core.telegram.org/api/obtaining_api_id  
  
-简略教程  
到 https://my.telegram.org/apps 里登录，并创建按需填写即可  
注意：如果提示`Error`错误，请更换IP再试  
创建完毕，请记录 `App api_id` `App api_hash` `App title` 三个项值  


## 配置
编辑`tgup.py`文件  
根据已创建的TG API对应修改值  
`API_ID` → `App api_id`  
`API_HASH` → `App api_hash`  
`API_NAME` → `App title`  
`target` → 修改你上传目的地（频道/群组）（注意必须是邀请url格式，即使是公开频道也可以创建额外的邀请url）
  
修改` 24行` 的SOCKS5代理地址与端口  

## 用法
```
python3 tgup.py 文件夹路径
```
-例
```
python3 tgup.py D:\test\MP4
```

## 注  
首次运行需要登录，对应填写电话号码、验证码、二次密码（如有），即可，之后无需再登录  
如果你想切换用户，请删掉py脚本目录里的`xxx.session`，重写运行即可
