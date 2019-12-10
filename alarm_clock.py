from time import strftime
import winsound
import threading
import sqlite3

conn = sqlite3.connect('alarms.db')
c = conn.cursor()

print("This is the alarm clock.")
print("Type 'HELP' for commands")


def main():
    # start timers outside the loop
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

        elif user_input in ["set", "SET"]:
            set_alarm()
            timer()
            show_list()

        elif user_input in ["delete", "DELETE", "del"]:
            show_list()
            delete_alarm()
            print("Alarm deleted ")
            main()


def timer():
    # get list of alarms
    alarm_list = get_alarms()

    # loop through rows in alarm_list
    for alarm_string in alarm_list:

        # get seconds left until alarm for each row
        seconds_left = get_seconds(alarm_string)

        # create and start timer
        if seconds_left >= 0:
            # after x seconds call 'play_alarm'
            alarm_timer = threading.Timer(seconds_left, play_alarm)
            alarm_timer.start()


def get_alarms():
    # create empty alarms list
    alarms = []

    # get alarm times from database and add them to alarms list
    for row in c.execute('SELECT time FROM alarms'):
        alarm = str(row).strip("()',")  # remove unnecessary characters
        alarms.append(alarm)

    return alarms


def get_seconds(alarm_string):
    # split alarm_string into array
    time = alarm_string.split(":")

    # alarm seconds
    a_hours = int(time[0])
    a_minutes = int(time[1])
    a_seconds = (a_hours * 3600 + a_minutes * 60)

    # current seconds
    c_hours = int(strftime("%H"))
    c_minutes = int(strftime("%M"))
    c_seconds = (c_hours * 3600 + c_minutes * 60 + int(strftime("%S")))

    # calculate seconds left until alarm
    seconds_left = a_seconds - c_seconds
    return seconds_left


def play_alarm():
    print("Wake up!")
    # alarm sound location
    fname = "C:\\Windows\\Media\\Alarm04.wav"
    # play alarm sound
    winsound.PlaySound(fname, winsound.SND_FILENAME)


def show_list():
    # get list of alarms from database and print them out
    for row in c.execute('SELECT * FROM alarms'):
        print(row[0], " : ", row[1])


def set_alarm():
    # get input from user and check that it's valid
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

    # get input from user and check that it's valid
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

    # create new_alarm from user inputs
    set_hours = str(set_hours).zfill(2)
    set_minutes = str(set_minutes).zfill(2)
    new_alarm = """""" + set_hours + ":" + set_minutes + """"""

    # insert new_alarm into database
    c.execute('INSERT INTO alarms (time) VALUES (?)', (new_alarm,))
    conn.commit()

    print("New alarm set at: ", new_alarm)


def delete_alarm():
    # get ids from database, reformat them and add them to id_list
    id_list = []
    for ids in c.execute('SELECT id FROM alarms'):
        id_string = str(ids).strip('(,)')
        id_string = int(id_string)
        id_list.append(id_string)
    print(id_list)

    # get id as user input and check that it's valid
    answer = 0
    while not answer:
        try:
            answer = int(input("Pick a number to delete: "))
            if answer not in id_list:
                raise ValueError
        except ValueError:
            answer = 0
            print("That is not an option")
    answer = str(answer)

    # remove from database
    c.execute('DELETE FROM alarms WHERE id = (?)', (answer,))


main()
