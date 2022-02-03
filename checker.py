from twitchAPI.twitch import Twitch
from json import loads
import requests
from auth import authenticate


#  configure the following APP_ID and APP_SECRET
twitch = Twitch('APP_ID_HERE', 'APP_SECRET_HERE')
authenticate(twitch)


def write_user_in_chat(streamer_name):
    """
    Prints and save a list of users that are currently in
    the chat of the streamer.

    :param streamer_name: Streamer name that is used
    in the API call

    :return: A list of the current chatters
    """
    r = requests.get("https://tmi.twitch.tv/group/user/{}/chatters".format(streamer_name))
    parsed = loads(r.content)
    f = open("{}.txt".format(streamer_name), "w")
    f.write("{}".format(parsed['chatters']['viewers']))
    f.close()
    return parsed['chatters']['viewers']


def read_login_list(streamer_name):
    f = open("{}.txt".format(streamer_name), "r")
    data = f.readlines()
    f.close()
    logins = data[0][1:-1].replace(" ", "").replace("\'", "").split(',')
    return logins


def convert_to_id(login_list_input):
    num = int((len(login_list_input))/100)
    temp_list = []
    for i in range(num):
        my_list = twitch.get_users(logins=login_list_input[i*100:(i+1)*100])['data']
        for user in my_list:
            temp_list.append([user['login'], user['id']])
    my_list = twitch.get_users(logins=login_list_input[num*100:])['data']
    for user in my_list:
            temp_list.append([user['login'], user['id']])
    return temp_list


def write_login_and_id(id_list_input, streamer_name):
    f = open("{}-id-list.txt".format(streamer_name), "w")
    str = ""
    print(len(id_list_input))
    for user in id_list_input:
        str += "{} {}\n".format(user[0], user[1])
    f.write(str)
    f.close()


def check_follows(id_list_input, streamer_id, streamer_name):
    """
    Checks and prints if IDs are a follower of the streamer
     or not.
    :param id_list_input: a list of IDs
    :param streamer_id: the id of the streamer
    :param streamer_name: to use it in the txt file
    """
    str = ""
    i = 0
    for user in id_list_input:
        print(i)
        i += 1
        try:
            req = twitch.get_users_follows(from_id=user[1], to_id=streamer_id)
            print(req)
            if req['total'] == 1:
                temp_str = "{}|{}|{}\n".format(user[0], user[1], "yes")
                print(temp_str)
                str += temp_str
            else:
                temp_str = "{}|{}|{}\n".format(user[0], user[1], "no")
                print(temp_str)
                str += temp_str
        except:
            print("Twitch API error")
            break
    f = open("{}-follow-list.txt".format(streamer_name), "w")
    f.write(str)
    f.close()


def read_login_id(streamer_name):
    """
    make a list of username and its id

    :param streamer_name: to open the id list txt file
    :return: the list of username and its id
    """
    id = []
    f = open("{}-id-list.txt".format(streamer_name), "r")
    lines = f.readlines()
    for line in lines:
        data = line.replace("\n", "").split(" ")
        id.append([data[0], data[1]])
    f.close()
    return id


def run():
    streamer_name = input("The Streamer Name: ")
    streamer_id = int(twitch.get_users(logins=[streamer_name])['data'][0]['id'])

    users_in_chat = write_user_in_chat(streamer_name)
    print(users_in_chat)
    login_list = read_login_list(streamer_name)
    login_id_list = convert_to_id(login_list)
    write_login_and_id(login_id_list, streamer_name)
    id_list = read_login_id(streamer_name)
    check_follows(id_list, streamer_id, streamer_name)


if __name__ == "__main__":
    run()
