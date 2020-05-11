Weblog 统计系统
---
## 程序文件结构
+ Weblog
    + weblog.py --> 程序运行文件
    + weblog_data.txt --> 数据存储文件
    + README.MD
---
## 程序实现功能
首页：
+ 登陆（提供登陆端口给三方用户）
+ 注册（提供学生自主注册端口）
+ 退出程序

开放三个端口
+ 学生端
    + 查看可选课程（查看现有课程）
    + 选择课程（选择课程加入自己的列表并同时产生学费进入学生账户）
    + 显示所选课程（显示学生选择的课程详情）
    + 查看成绩（查看所有课程的成绩）
    + 交学费（显示欠费余额，并提供简易缴费功能）
    + 退出

+ 教师端
    + 课程选择（选择课程加入教师列表，规定所教课程不可兼教课程）
    + 显示所教课程详细信息（显示教授课程的详情）
    + 查看班级学生（显示教授课程的学生）
    + 移除学生（从班级移除学生）
    + 登入及修改学生成绩（显示学生姓名及成绩，可登入或修改成绩）
    + 退出

+ 管理员端
    + 创建新账号（可创建三方账号）
    + 创建课程（创建新课程）
    + 查看所有课程信息（查看先有所有课程信息）
    + 查看所有学生选课信息（查看学生选课信息）
    + 查看所有教师任课信息（查看老师任课信息）
    + 教师调配（老师任课调配，拥有绝对的话语权）
    + 退出

## 程序的启动方式
+ 通过终端或python解释器启动run.py文件
---
## 登陆用户信息
+ 程序直接启动无需登陆
    + 启动后可通过:用户名<Roger> 密码<qwe123> 进入管理端
    + 启动后可通过:用户名<Alex> 密码<qwe123> 进入教师端
    + 启动后可通过:用户名<Jiang> 密码<qwe123> 进入学生端
---
## 程序运行效果
通过序号进行操作
### 学生端
![学生端](https://i.loli.net/2020/05/03/ixYpKOLhG3mnPoe.jpg)

### 教师端
![教师端](https://i.loli.net/2020/05/03/B6URgpa27OH3VXY.jpg)

### 管理员端
![管理员端](https://i.loli.net/2020/05/03/QuHMlgi2t7JNcPG.jpg)
---
## 程序运行流程图
+ Homepage flowchart
![homepage_flowchart](https://i.loli.net/2020/05/03/cbP5Mykr89FRUZV.jpg)
+ 教师 flowchart
![教师flowchart](https://i.loli.net/2020/05/03/zPxCo3YByFJLkf6.jpg)
+ 管理员 flowchart
![管理员flowchart](https://i.loli.net/2020/05/03/dzakAs593VUQJle.jpg)
+ 学生 flowchart
![学生flowchart](https://i.loli.net/2020/05/03/qbisDFohSl8BgQu.jpg)