# -*- codeing = utf-8 -*-

import logging
import random
import datetime
import platform
from pathlib import Path
from sys import argv, exit
from subprocess import check_output, DEVNULL
from io import BytesIO
from pyrogram import Client


#填写这些，参见 https://core.telegram.org/api/obtaining_api_id
API_NAME = "test"
API_ID = 123456
API_HASH = "xxxxx"

#上传目的地（群组/频道）（必须邀请链接格式）
target = 'https://t.me/joinchat/xxxxxx'

video_format = ['*.mp4', '*.mov']
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARN)


def get_metedata(file): #获取视频信息和缩略图
    files_copy = file
    if platform.system().lower() == 'windows':
        files_copy = f'"{str(files_copy)}"' #win
    elif platform.system().lower() == 'linux':
        files_copy = f"'{str(files_copy)}'" #Linux
    cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {files_copy}'
    width, height = check_output(cmd, shell=True).decode().split('x')
    cmd_time = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {files_copy}'
    time = int(float(check_output(cmd_time, shell=True).strip()))
    if 2 < time :
        time_random = datetime.timedelta(seconds=int(random.randint(2, time - 1)))
        cmd_thumb = f'ffmpeg -ss {time_random} -i {files_copy} -f image2 -frames:v 1 -'
    else:
        cmd_thumb = f'ffmpeg -ss 0:01 -i {files_copy} -f image2 -frames:v 1 -'
    thumb = BytesIO(check_output(cmd_thumb, shell=True, stderr=DEVNULL))
    thumb.name = 'thumb.jpg'
    return int(width), int(height), time, thumb


def tgup_video_one(files): #单视频文件上传
    with Client(API_NAME, int(API_ID), API_HASH) as client:
        try:
            chat = client.get_chat(target)
            def callback(current, total):
                print('\r[{:0>5.2f}%] {}'.format(current / total * 100, files), end='')
            width, height, time, thumb = get_metedata(files)
            filename = str(files).replace(argv[1], "").replace('\\', '')
            client.send_video(chat.id, str(files), caption=f'{filename}', width=width, height=height, thumb=thumb, duration=time, progress=callback)
            print(f"\n上传完毕-{str(files)}")
        except:
            print(f'上传出错-{str(files)}')
            client.send_message('me', f'上传出错-{str(files)}')

if __name__ == "__main__":
    if len(argv) == 1: #判断参数
        print(f'Usage: {argv[0]} 文件夹')
        exit()
    if len(argv) == 2: #判断参数
        for tpV in video_format:  # 判断视频格式
            for file in Path(argv[1]).glob(tpV):  #获取视频文件列表
                tgup_video_one(file)
