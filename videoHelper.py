# -*- coding: utf-8 -*-
# version 4
# developed by zk chen
# modified by Cat1007
# modified by Rean on 2024/07/01, referring to Cyber-Ingwen
# applicable to the ykt of SCUT
import random
import time
import requests
import re
import json

# 以下的csrftoken和sessionid需要改成自己登录后的cookie中对应的字段！！！！而且脚本需在登录雨课堂状态下使用
# 登录上雨课堂（注意需要登陆的是"https://scut.yuketang.cn/"这个网址），然后按F12-->选Application-->找到雨课堂的cookies，寻找csrftoken、sessionid字段，并复制到下面两行即可
csrftoken = ""  # 需改成自己的
sessionid = ""  # 需改成自己的
auto_video = True  # 是否自动刷视频
auto_discuss = True  # 是否自动讨论
university_id = "2627"
url_root = "https://scut.yuketang.cn/"
learning_rate = 4  # 学习速率 我觉得默认的这个就挺好的

# 以下字段不用改，下面的代码也不用改动
user_id = ""

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=' + csrftoken + '; sessionid=' + sessionid + '; university_id=' + university_id + '; platform_id=3',
    'x-csrftoken': csrftoken,
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'university-id': university_id,
    'xtbz': 'ykt'
}

leaf_type = {
    "video": 0,
    "homework": 6,
    "exam": 5,
    "recommend": 3,
    "discussion": 4
}


def one_video_watcher(video_id, video_name, cid, user_id, classroomid, skuid):
    video_id = str(video_id)
    classroomid = str(classroomid)
    url = url_root + "video-log/heartbeat/"
    get_url = url_root + "video-log/get_video_watch_progress/?cid=" + str(
        cid) + "&user_id=" + user_id + "&classroom_id=" + classroomid + "&video_type=video&vtype=rate&video_id=" + str(
        video_id) + "&snapshot=1&term=latest&uv_id=" + university_id + ""
    progress = requests.get(url=get_url, headers=headers)
    if_completed = '0'
    try:
        if_completed = re.search(r'"completed":(.+?),', progress.text).group(1)
    except:
        pass
    if if_completed == '1':
        print("【" + video_name + "】" + "已经学习完毕，跳过")
        return 1
    else:
        print("【" + video_name + "】" + "，尚未学习，现在开始自动学习")
        time.sleep(2)

    # 默认为0（即还没开始看）
    video_frame = 0
    val = 0
    learning_rate = 20
    t = time.time()
    timestap = int(round(t * 1000))
    while val != "1.0" and val != '1':
        heart_data = []
        for i in range(50):
            heart_data.append(
                {
                    "i": 5,
                    "et": "loadeddata",
                    "p": "web",
                    "n": "ws",
                    "lob": "cloud4",
                    "cp": video_frame,
                    "fp": 0,
                    "tp": 0,
                    "sp": 1,
                    "ts": str(timestap),
                    "u": int(user_id),
                    "uip": "",
                    "c": cid,
                    "v": int(video_id),
                    "skuid": skuid,
                    "classroomid": classroomid,
                    "cc": video_id,
                    "d": 4976.5,
                    "pg": "4512143_tkqx",
                    "sq": 2,
                    "t": "video"
                }
            )
            video_frame += learning_rate
            max_time = int((time.time() + 3600) * 1000)
            timestap = min(max_time, timestap + 1000 * 15)
        data = {"heart_data": heart_data}
        r = requests.post(url=url, headers=headers, json=data)
        # print(r.text)
        try:
            error_msg = json.loads(r.text)["message"]
            if "anomaly" in error_msg:
                video_frame = 0
        except:
            pass
        try:
            delay_time = re.search(r'Expected available in(.+?)second.', r.text).group(1).strip()
            print("由于网络阻塞，万恶的雨课堂，要阻塞" + str(delay_time) + "秒")
            time.sleep(float(delay_time) + 0.5)
            video_frame = 0
            print("恢复工作啦～～")
            submit_url = url_root + "mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=" + university_id
            r = requests.post(url=submit_url, headers=headers, data=data)
        except:
            pass
        progress = requests.get(url=get_url, headers=headers)
        tmp_rate = re.search(r'"rate":(.+?)[,}]', progress.text)
        if tmp_rate is None:
            return 0
        val = tmp_rate.group(1)
        print("学习进度为：" + str(float(val) * 100) + "%/100%" + " last_point: " + str(video_frame))
        time.sleep(0.7)
    print("视频" + video_id + " " + video_name + "学习完成！")


def get_videos_ids(classroom_id):
    get_homework_ids = url_root + "v2/api/web/logs/learn/" + \
                       classroom_id + "?actype=-1&page=0&offset=20&sort=-1"
    homework_ids_response = requests.get(url=get_homework_ids, headers=headers)
    homework_json = json.loads(homework_ids_response.text)
    if homework_json['data']['prev_id'] == -1:
        print('该课程尚无内容！程序退出....')
        exit(1)
    if homework_json['errcode'] != 0:
        print(homework_json)
        exit(1)
    courseware_id = []
    homework_dic = {}
    for i in homework_json['data']['activities']:
        courseware_id.append(i['courseware_id'])
        homework_dic[i['courseware_id']] = i['title']
    data = {
        'cid': classroom_id,
        'new_id': courseware_id
    }


# 自动复读讨论题
def auto_repeat_discussion(classroom_id, sku_id, leaf_id, title):
    sleep_time = 3
    # 获取讨论题论坛id
    params = {
        'classroom_id': classroom_id,
        'sku_id': sku_id,
        'leaf_id': leaf_id,
        'topic_type': 4,
        'channel': 'xt'
    }
    discussion_response = requests.get(url=url_root + "v/discussion/v2/unit/discussion/",
                                       params=params, headers=headers).json()['data']
    forum_id = discussion_response['id']
    to_user = discussion_response['user_id']

    # 获取评论列表
    params = {
        'offset': 0,
        'limit': 10,
        'web': 'web'
    }
    comments = requests.get(url=url_root + "v/discussion/v2/comment/list/" + str(forum_id) + "/",
                            params=params, headers=headers).json()['data']['new_comment_list']['results']
    if len(comments) == 0:
        print("暂无评论，跳过")
        return
    else:
        comment_text = comments[0]['content']['text']

        # 发送评论
        json_data = {
            'to_user': to_user,
            'topic_id': forum_id,
            'content': {
                'text': comment_text,
                'upload_images': [],
                'accessory_list': [],
            },
        }

        comment_response = requests.post(url=url_root + "v/discussion/v2/comment/",
                                         json=json_data, headers=headers).json()
        if comment_response['success']:
            print("【" + title + "】评论成功！")
            time.sleep(sleep_time)


if __name__ == "__main__":
    your_courses = []

    # 首先要获取用户的个人ID，即user_id,该值在查询用户的视频进度时需要使用
    user_id_url = url_root + "v2/api/web/userinfo"
    id_response = requests.get(url=user_id_url, headers=headers)
    try:
        user_id = re.search(r'"user_id":(.+?)}',
                            id_response.text).group(1).strip()
    except:
        print("也许是网路问题，获取不了user_id,请试着重新运行")
        raise Exception(
            "也许是网路问题，或者cookie填写错误，获取不了user_id,请试着重新运行!!! please re-run this program!")

    # 然后要获取教室id
    params = {
        'identity': '2',
    }
    response = requests.get(
        url_root + "v2/api/web/courses/list", params=params, headers=headers).json()
    if response['errmsg'] != 'Success':
        print("csrftoken或者sessionid有问题请检查！")
        exit(1)
    index = 0
    # 获取课程id 和 课程名字
    for i in response['data']['list']:
        your_courses.append(i['classroom_id'])
        print("编号：" + str(index + 1) + " 课名：" + str(i["course"]['name']) + "（" + i['name'] + "）")
        index += 1

    flag = True
    while flag:
        number = input("你想刷哪门课呢？请输入编号。\n")
        # 输入不合法则重新输入
        if not (number.isdigit()) or int(number) > len(your_courses):
            print("输入不合法！")
            continue
        else:
            flag = False  # 输入合法则不需要循环
            discussion_ids = []
            # 指定序号的课程刷一遍
            number = int(number) - 1
            cid = str(your_courses[number])
            homework_dic = get_videos_ids(cid)
            headers['classroom-id'] = cid
            headers['xtbz'] = 'ykt'
            headers['Referer'] = url_root + "v2/web/studentLog/" + cid
            skuid = requests.get(url=url_root + "v2/api/web/classrooms/" +
                                     cid + "?role=5", headers=headers).json()['data']['free_sku_id']
            get_url = url_root + "c27/online_courseware/schedule/score_detail/single/%s/0/" % skuid
            ret = requests.get(url=get_url, headers=headers).json()
            print("\n正在获取视频列表……")
            for i in ret['data']['leaf_level_infos']:
                if i['leaf_type'] != leaf_type['video']:
                    # 添加讨论题id
                    if i['leaf_type'] == leaf_type['discussion']:
                        discussion_ids.append({'id': i['id'], 'title': i['leaf_level_title']})
                        continue
                    else:
                        continue
                get_url = url_root + 'mooc-api/v1/lms/learn/leaf_info/%s/%s/' % (
                    cid, i['id'])
                getccid = requests.get(url=get_url, headers=headers).json()
                skuid = getccid['data']['sku_id']
                user_id = getccid['data']['user_id']
                ccid = getccid['data']['content_info']['media']['ccid']
                course_id = getccid['data']['course_id']
                print(i['leaf_chapter_title'] + " - " + i['leaf_level_title'])
            confirm = input("以上为视频列表，请确认是否刷此课（Y/N）：")
            if confirm == "Y" or confirm == 'y':
                if auto_video:
                    print("---------------------------开始刷视频-------------------------------")
                    for i in ret['data']['leaf_level_infos']:
                        if i['leaf_type'] != leaf_type['video']:
                            continue
                        get_url = url_root + 'mooc-api/v1/lms/learn/leaf_info/%s/%s/' % (
                            cid, i['id'])
                        getccid = requests.get(url=get_url, headers=headers).json()
                        skuid = getccid['data']['sku_id']
                        user_id = getccid['data']['user_id']
                        ccid = getccid['data']['content_info']['media']['ccid']
                        course_id = getccid['data']['course_id']
                        one_video_watcher(i['id'], i['leaf_chapter_title'] + " - " + i['leaf_level_title'],
                                          course_id, str(user_id), cid, skuid)
                    print("---------------------------刷视频结束-------------------------------")

                # 自动讨论
                if auto_discuss:
                    print("---------------------------开始自动复读-------------------------------")
                    for item in discussion_ids:
                        auto_repeat_discussion(cid, skuid, item['id'], item['title'])
                    print("---------------------------自动复读结束-------------------------------")
            else:
                flag = True
                continue
        print("---------------------------已完成-------------------------------")
