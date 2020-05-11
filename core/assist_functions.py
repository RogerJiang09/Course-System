import pickle

def input_for_list(list):
    while True:
        user_choice = input('>>>:')
        if not user_choice.isdigit():
            print('输入错误，请输入相应序号')
        elif 0 <= (int(user_choice) - 1) < len(list):
            return list[int(user_choice) - 1][1]
        else:
            print('输入错误，请重新输入')

def register_check(corresponding_info):
    with open('data/%s_info.pickle' % corresponding_info,'rb') as f:
        user_info = pickle.load(f)
    while True:
        user_name = input('请输入用户名：')
        if user_name in user_info.keys():
            print('用户名已存在，请重新输入')
        else:
            break

    while True:
        password = input('请输入密码：')
        password_confirmation = input('请再次输入密码：')
        if password != password_confirmation:
            print('密码不相同，请重新输入')
        else:
            return user_info,user_name,password