
# Twitch-Follower-Checker

This is a very simple program that uses **[Python](https://www.python.org/)** and **[pyTwitchAPI](https://github.com/Teekeks/pyTwitchAPI)** to retrieve the list of users in a streamer's chat and then checks each one of these users to see if they follow the broadcaster or not.

## Important note
Using this program requires basic knowledge of Python. This code was written in a short time and there is a lot of room for improvement. if you find any bugs, don't hesitate to let me know, I currently don't have any plans on further developing this bot but I would fix the bugs.
|                |Question                          |Answer                         |
|----------------|-------------------------------|-----------------------------|
|1|Does this bot find fake views?|No, This bot only checks the streamer's user in chat and finds out which one of them follows that broadcaster. This information may be used along with other statistics to show if someone's views are artificially adjusted.|
|2          |Is this allowed?            |This program uses publicly available Twitch API.|
|3          |Why do I need to login?|The Twitch API has a lower rate limit of Application tokens compared to User tokens. By logging in, the app uses your user token to do things more quickly.|

## Prerequisites
In order to run this code you need to:
- Have **Python** running properly on your computer (if you don't know how to do this, use a beginner's guide)
- Install **pyTwitchAPI** for **Python**, you can install using pip:
>```pip install twitchAPI```
- Register an Application on Twitch and save its App ID and Secret
> Go to [Twitch Dev Console](https://dev.twitch.tv/console) and register your application. Use ```http://localhost:17563``` as the redirect URL.

## Basic Usage
After setting up everything from the previous section, all you need to do is to replace the APP_ID and APP_SECRET in line 85:

```twitch = Twitch(APP_ID_HERE,APP_SECRET_HERE)```

and replace the streamer's name with the person you want to check in line 88:

```streamer_name = "shroud"```

You can now run the python file and wait for it to generate the related text files.
