# yuketangHelperSCUTbyRean
A python script used to watch the videos in Rain Classroom(SCUT) automatically modified by Rean



### 说点什么：

#### Notice:

I modified the script based on the script of Cat1007 and referred to the script of Cyber-Ingwen(https://github.com/Cyber-Ingwen/yuketangHelperCQU)

test on 2023/5/10:
![image](https://github.com/Rean-Schwarze/yuketangHelperSCUTbyRean/assets/19246285/416e880f-8171-43c1-826d-7a531a0094c6)
<img width="858" alt="837f1c9e7d3159760fac4361f255b47" src="https://github.com/Rean-Schwarze/yuketangHelperSCUTbyRean/assets/19246285/368733d2-ac6e-43d1-85fb-39ad0b1c4efa">
运行一次可能会有一些视频没刷完的，多运行一两次就可以了（


#### Original texts:

之前也有想到伪造心跳包的方法去快速刷网课，结果上GitHub一搜发现有师兄已经实现了这个思路。

在此十分感谢@[heyblackC](https://github.com/heyblackC)，让我不用再研究包里变量含义了hhhh

以下是原脚本仓库：

https://github.com/heyblackC/yuketangHelper



### 脚本改进：

#### 2023/05/10:
- 使用方面略微优化了一下

#### 2023/01/03:
- 适配现版本雨课堂

#### Original texts:
- 修改一些域名及对应的参数，适配本科生系统
- 修复一个正则表达式匹配Bug
- 修改了一些文本提示



### 食用方法：

1. 安装好python环境

2. 安装pip（最好换一下国内的镜像源）[参考](https://blog.csdn.net/yuzaipiaofei/article/details/80891108)

3. 克隆或下载该仓库

4. 安装vscode以及vscode的python插件，并根据提示使用pip安装所需要的包

   ![image-20210419085901386](https://gitee.com/cat1007/markdown-pics/raw/master/uPic/image-20210419085901386.png)

5. 打开浏览器，登录雨课堂并获取对应的cookie  [参考](https://blog.csdn.net/lenfranky/article/details/90316262)

注：需要登陆获取cookie的网址是"scut.yuketang.cn"，不是"changjiang.yuketang.cn"

6. 修改 `videoHelper.py` 源代码并填入你自己的值

   ![image-20210419090408207](https://gitee.com/cat1007/markdown-pics/raw/master/uPic/image-20210419090408207.png)

7. 右上角绿色三角点击运行

8. 终端按提示输入对应的课程编号并回车

9. 直接爽到起飞🛫️
