from time import strftime
import winsound
import threading
import sqlite3

conn = sqlite3.connect('alarms.db')
c = conn.cursor()

print("This is the alarm clock.")
print("Type 'HELP' for commands")


def get_alarms():
    alarms = []
    for row in c.execute('SELECT time FROM alarms'):
        alarm = str(row).strip("()',")
        alarms.append(alarm)
    print("get_alarms ", alarms)
    return alarms


def main():
    timer()
    while True:
        user_input = input("Enter a command: ")

        if user_input in ["help", "HELP"]:
            print("===========================")
            print("The commands are as follows: ")
            print("===========================")
            print("'TIME' show current time")
            print("'LIST' show alarm list")
            print("'SET' set new alarm")
            print("'DELETE' remove alarm")
            print("'HELP' list commands")
            print("===========================")

        elif user_input in ["time", "TIME"]:
            print("Current time is ", strftime("%H:%M:%S "))

        elif user_input in ["list", "LIST"]:
            show_list()

        elif user_input in ["delete", "DELETE", "del"]:
            show_list()
            delete()
            main()
            print("Alarm deleted ")
#BALEET
        elif user_input in ["qwe"]:
            get_alarms()

        elif user_input in ["set", "SET"]:
            set()
            timer()
            show_list()


def show_list():
    for row in c.execute('SELECT * FROM alarms'):
        print(row[0], " : ", row[1])


def play_alarm():
    print("Wake up!")
    fname = "C:\\Windows\\Media\\Alarm04.wav"
    winsound.PlaySound(fname, winsound.SND_FILENAME)


def get_seconds(alarm_string):
    time = alarm_string.split(":")
    a_hours = int(time[0])
    a_minutes = int(time[1])
    a_seconds = (a_hours * 3600 + a_minutes * 60)

    c_hours = int(strftime("%H"))
    c_minutes = int(strftime("%M"))
    c_seconds = (c_hours * 3600 + c_minutes * 60 + int(strftime("%S")))

    seconds_left = a_seconds - c_seconds
    print(alarm_string, " ", seconds_left)
    return seconds_left


def timer():
    alarm_list = get_alarms()
    for alarm_string in alarm_list:
        seconds_left = get_seconds(alarm_string)
        if seconds_left >= 0:
            alarm_timer = threading.Timer(get_seconds(alarm_string), play_alarm)
            alarm_timer.start()


def insert(new_alarm):
    c.execute('INSERT INTO alarms (time) VALUES (?)', (new_alarm,))


def delete():
    id_list = []
    for ids in c.execute('SELECT id FROM alarms'):
        id_string = str(ids).strip('(,)')
        id_string = int(id_string)
        id_list.append(id_string)
    print(id_list)

    answer = 0
    while not answer:
        try:
            answer = int(input("Pick a number to delete: "))
            if answer not in id_list:
                raise ValueError
        except ValueError:
            answer = 0
            print("That is not an option")
    print(answer)
    answer = str(answer)

    c.execute('DELETE FROM alarms WHERE id = (?)', (answer,))


def set():
    set_hours = 0
    hour_set = False
    while not hour_set:
        try:
            set_hours = int(input("Set hour between 0-23: "))
            if set_hours not in (range(0, 24)):
                raise ValueError
            else:
                hour_set = True
        except ValueError:
            set_hours = 0
            print("That is not an option")

    set_minutes = 0
    minute_set = False
    while not minute_set:
        try:
            set_minutes = int(input("Set minute between 0-59: "))
            if set_hours not in (0 or range(0, 60)):
                raise ValueError
            else:
                minute_set = True
        except ValueError:
            set_minutes = 0
            print("That is not an option")

    set_hours = str(set_hours).zfill(2)
    set_minutes = str(set_minutes).zfill(2)
    new_alarm = """""" + set_hours + ":" + set_minutes + """"""

    print(new_alarm)

    c.execute('INSERT INTO alarms (time) VALUES (?)', (new_alarm,))
    conn.commit()

    print("New alarm set at: ", new_alarm)



main()
