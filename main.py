import winreg
import os
import pyttsx3
import datetime
import shutil
import sys

os.system("cls")  # Clear
RED = '\033[31m'   # mode 31 = red forground
RESET = '\033[0m'  # mode 0  = reset


def foo(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['version'] = winreg.QueryValueEx(
                    asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(
                    asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            try:
                software['InstallLocation'] = winreg.QueryValueEx(
                    asubkey, "InstallLocation")[0]
            except EnvironmentError:
                software['InstallLocation'] = 'undefined'
            try:
                software['DisplayIcon'] = winreg.QueryValueEx(
                    asubkey, "DisplayIcon")[0]
            except EnvironmentError:
                software['DisplayIcon'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list


def specialCase(app):

    if ('text' in app) and ('editor' in app):
        os.system("start notepad")
        reply("Opening notepad...")
        return True
    if ('text editor' in app) or ('editor' in app):
        os.system("start notepad")
        reply("Opening notepad...")
        return True
    if ('vs editor' in app) or ('vs code' in app) or (('code' in app) and ('vs' in app)):
        os.system("code")
        reply("Opening Visual Studio code")
        return True
    elif ('play' in app) and (("music" in app) or "song" in app) or ('music player' in app) or (('music' in app) and ("player" in app)):
        os.system("start vlc")
        reply("Opening VLC player, you can play music from here...")
        return True
    elif ('play' in app) and (('video' in app) or ('vid' in app)) or (('player' in app) or ("video" in app)):
        os.system("start vlc")
        reply("Opening VLC player, you can play video from here...")
        return True
    elif ('browser' in app) or ('browse' in app):
        runApp("chrome")
        return True
    elif ('.' in app) and ('in' in app):
        # silly programming:
        u = app.split(".")
        u1 = u[0].split()
        u2 = u[1].split()
        url = u1[len(u1)-1] + '.' + u2[0]
        if "in" in u1:
            inx = u1.index('in')
            while inx < len(u1):
                if (u1[inx] == "the" or u1[inx] == "a" or u1[inx] == 'in'):
                    inx = inx + 1
                else:
                    # runApp(u1[inx], url)
                    reply("Opening " + url + " in " + u1[inx])
                    os.system('start ' + u1[inx] + " " + url)
                    break
            pass
        elif "in" in u2:
            inx = u2.index('in')
            while inx < len(u2):
                if (u2[inx] == "the" or u2[inx] == "a" or u2[inx] == 'in'):
                    inx = inx + 1
                else:
                    # runApp(u2[inx], url)
                    reply("Opening " + url + " in " + u2[inx])
                    os.system('start ' + u2[inx] + " " + url)
                    break
            pass
        return True
    elif '.' in app:

        u = app.split(".")
        u1 = u[0].split()
        u2 = u[1].split()
        url = u1[len(u1)-1] + '.' + u2[0]
        os.system("start chrome " + url)
        reply("Opening " + url + " in chrome ...")
        return True
    return False


# RUN APP


def runApp(app, exFile=""):

    x = os.system(app + " " + exFile)
    if x == 1:
        job = False
        for software in software_list:

            # or software['name'].casefold().find(app.casefold()):
            if (app.casefold() in software['name'].casefold()):
                if ".exe" in software['DisplayIcon']:
                    software['DisplayIcon'].replace("\\", '/')
                    # file = software['DisplayIcon'].replace(",0", '')
                    file = software['DisplayIcon'].split(',')[0]
                    reply("Sure sir")
                    reply("Opening " + software['name'] + " ...")
                    try:
                        os.startfile(file + " " + exFile)
                        job = True
                        pass
                    except:
                        job = False
                        pass

                    return True
                else:
                    reply("Sorry! I am unable to find the programm in your computer")
                break
        if not job:
            reply("Sorry! I am unable to find the programm in your computer")
    elif x == 0:
        reply("Opening " + app)
        pass
    else:
        reply("Sorry! I am unable to find the programm in your computer")

# Request type


def reqtype(req):
    y = req.split()
    # Here i can't use (note in req) because when the in put conatain notepad it return true
    if ("not" in y) or ("don't" in y) or ("dont" in y):
        return 'neg'
    else:
        return "pos"

# REQUEST


def request(req):
    # REQUEST COMBINATIONS
    # opne chrome
    # opne the chrome
    # please run firefox
    # please run the firefox for me
    # can  you run firefox
    # can  you run the firefox for me
    if 'pos' == reqtype(req):
        if ("run" in req) or ("open" in req) or ("execute" in req) or ("start" in req):
            # Getting tha app
            if not specialCase(req):
                wordsList = req.split()
                inx = -1
                for p in ["run", "open", "execute", 'start']:
                    try:
                        inx = wordsList.index(p)
                        if inx != -1:
                            inx = inx + 1
                            break
                        pass
                    except:
                        pass

                while inx < len(wordsList):
                    if (wordsList[inx] == "the" or wordsList[inx] == "a" or wordsList[inx] == 'in' or wordsList[inx] == 'me' or wordsList[inx] == 'for'):
                        inx = inx + 1
                    else:
                        runApp(wordsList[inx])
                        break

    else:
        reply("OK")
        pass

# ACTION


def action(command):
    command = command.casefold()
    # Normal Chat

    if ("who are you" in command) or ("who r u" in command) or ("who are u" in command) or ("who r you" in command) or ("who you" in command) or ("who u" in command):
        reply("Hello sir! I am your IIEC RISE challenge assistance. developed by Navneet Chandra Maurya.")
    elif ("your name" in command) or ("ur name" in command):
        reply("Hello sir! I am your IIEC RISE challenge assistance. developed by Navneet Chandra Maurya.")
    elif ("how are you" in command) or ("how r u" in command) or ("how are u" in command) or ("how r you" in command):
        reply("I am fine. How are you?")
        reply("I hope you are helthy.")
    elif ("hello" in command) or ("hi" in command) or ("hey navi" in command):
        time = datetime.datetime.now()
        reply("Hi sir!")
        reply("today is " + time.strftime('%d') + " " + time.strftime('%B') + " " + time.strftime('%Y') +
              " and the time is " + time.strftime('%I') + " hours " + time.strftime("%M") + " minutes ")
        reply("Have a greate day :)")
    elif ("namaste" in command) or ("namasty" in command):
        time = datetime.datetime.now()
        reply("Namaste sir!")
        reply("today is " + time.strftime('%d') + " " + time.strftime('%B') + " " + time.strftime('%Y') +
              " and the time is " + time.strftime('%I') + " hours " + time.strftime("%M") + " minutes ")
        reply("Have a greate day :)")
    elif "thanks" in command or ((("thanks" in command) or ("thank" in command)) and (('you' in command) or ('u' in command))):
        reply("My pleasure")
    elif ("i am fine" in command) or ("i am good" in command) or ("i'm good" in command) or ("i'm fine" in command):
        reply("that's greate, Keep smiling.")
    # Work with programms
    elif ("please" in command) or ("plz" in command) or ("can you" in command) or ("can u" in command) or ("want open" in command) or ("want to opne" in command):
        request(command)
    elif ("open" in command) or ("run" in command) or ("execute" in command) or ("start" in command):
        request(command)
    elif ("play" in command):
        specialCase(command)
    elif ("date" in command) or ("time" in command):
        time = datetime.datetime.now()
        reply("The current time is " + time.strftime('%I') + " hours " + time.strftime("%M") + " minutes " +
              " and date is " + time.strftime('%d') + " " + time.strftime('%B') + " " + time.strftime('%Y'))
        return True
    elif ("exit" in command) or ("quit" in command) or ("by" in command) or ("bay" in command):
        if reqtype(command) == "pos":
            reply("See you soon :)")
            exit()
            pass
    else:
        reply("Sorry!, I couldn't understand")


def stdout(message):
    sys.stdout.write(message)
    sys.stdout.write('\b' * len(message))   # \b: non-deleting backspace
    print()


def printRight(message):
    term = shutil.get_terminal_size((80, 20))
    # if (term-10) < len(message):
    #     (term - 10)
    #     pass
    stdout(message.rjust(term.columns))
    sys.stdout.flush()
    print()


# GET COMMAND


def getCommand(forWhat):
    print()
    print(forWhat, end="")
    inp = input()
    return inp

# Send responce


def reply(message):
    print('\033[92m', end="")
    printRight(message + " <<")
    pyttsx3.speak(message)
    print('\033[0m', end="")
    return True


# GETTING LIST OF INSTALLE APP FROM RESITORY
software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(
    winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)

# START =>>>
#  GETTING INPUT FROM USER
columns = shutil.get_terminal_size((80, 20)).columns
print('-'*columns)
msg = 'WLCOME TO THE IIEC-RISE CHALLENGE ASSISTANCE'
reply(msg + " " * int((columns - len(msg))/2))
reply("Developed By: Navneet Chandra Maurya")
print("Tested onlyon: Windows")
print("Honestly:")
print("This program developed with the inspiration by IIEC RISE community")
#
print("Took help from : ")
print("https://tackoverflow.com")
print("https://docs.python.org/3/")
print("https://www.devdungeon.com/content/colorize-terminal-output-python")
print("Common commands:")
print(">>> hi, hello, hey or namaste")
print(">>> who r you")
print(">>> how r you")
print(">>> play music")
print(">>> play video")
print(">>> opne chrome")
print(">>> Open google.com in firefox OR any other browser")
print(">>> date")
print(">>> please open the firefox for me")
print(">>> can  you run the firefox for me")
print("*Many app can be open which are added to environment variable and also others")
print("*Want to know:")
print("'pass' keyword which is added to my code by editor.")
print("Dont't know too much about 'try except' keywords in python")
print('\nThank you, sir, for this great initiative. I am also thankful to all IIEC-RISE members who are working hard for us to grow up our skills.')
print('-'*columns)
#
reply("Namaste sir!")
reply("I am your IIEC-RISE challenge assistance")
reply("You can call me Navi")
reply("What can I do for you ?")
command = getCommand(">>> ")
action(command)
command = ""
# Chat
while True:
    command = getCommand(">>> ")
    if command != "":
        action(command)
        pass

