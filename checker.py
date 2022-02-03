from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from json import loads
import requests

def authenticate():
    target_scope = [AuthScope.BITS_READ]
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    token, refresh_token = auth.authenticate()
    twitch.set_user_authentication(token, target_scope, refresh_token)

def write_user_in_chat(streamer_name):
    r = requests.get("https://tmi.twitch.tv/group/user/{}/chatters".format(streamer_name))
    parsed = loads(r.content)
    print(parsed['chatters']['viewers'])
    f = open("{}.txt".format(streamer_name), "w")
    f.write("{}".format(parsed['chatters']['viewers']))
    f.close()
    
def read_login_list(streamer_name):
    f = open("{}.txt".format(streamer_name), "r")
    data = f.readlines()
    f.close()
    logins=data[0][1:-1].replace(" ","").replace("\'","").split(',')
    return logins

def convert_to_id(login_list_input):
    num = int((len(login_list_input))/100)
    temp_list=[]
    for i in range(num):
        my_list=twitch.get_users(logins=login_list_input[i*100:(i+1)*100])['data']
        for user in my_list:
            temp_list.append([user['login'], user['id']])
    my_list=twitch.get_users(logins=login_list_input[num*100:])['data']
    for user in my_list:
            temp_list.append([user['login'], user['id']])
    return temp_list

def write_login_and_id(id_list_input, streamer_name):
    f = open("{}-id-list.txt".format(streamer_name), "w")
    str = ""
    print(len(id_list_input))
    for user in id_list_input:
        str += "{} {}\n".format(user[0],user[1])
    f.write(str)
    f.close()

def check_follows(id_list_input, streamer_id, streamer_name):
    str = ""
    i = 0
    for user in id_list_input:
        print(i)
        i+=1
        try:
            req=twitch.get_users_follows(from_id=user[1],to_id=streamer_id)
            print(req)
            if req['total']==1:
                temp_str="{}|{}|{}\n".format(user[0],user[1],"yes")
                print(temp_str)
                str += temp_str
            else:
                temp_str="{}|{}|{}\n".format(user[0],user[1],"no")
                print(temp_str)
                str += temp_str
        except:
            print("Twitch API error")
            break
    f = open("{}-follow-list.txt".format(streamer_name), "w")
    f.write(str)
    f.close()

def read_login_id(streamer_name):
    id=[]
    f = open("{}-id-list.txt".format(streamer_name), "r")
    lines=f.readlines()
    for line in lines:
        data=line.replace("\n","").split(" ")
        id.append([data[0],data[1]])
    f.close()
    return id
    
###############################################################################

twitch = Twitch('APP_ID_HERE','APP_SECRET_HERE')
authenticate()

streamer_name = input("The Streamer Name: ")
streamer_id = int(twitch.get_users(logins=[streamer_name])['data'][0]['id'])

write_user_in_chat(streamer_name)
login_list=read_login_list(streamer_name)
login_id_list=convert_to_id(login_list)
write_login_and_id(login_id_list, streamer_name)
id_list = read_login_id(streamer_name)
check_follows(id_list, streamer_id, streamer_name)

###############################################################################
