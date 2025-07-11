"""
This script is intended to help setup cronjobs to automate dumpcap captures. It collects required parameters from
the user and outputs cronjob entry lines so that the user can copy-paste them after running 'crontab -e'. It also
has a final line to automate 'archiver.sh' to run daily at a user-given time.

@author: Damian Najera
@version: 1.1
"""
import calendar
import os
import readline
from calendar import month, monthrange
from datetime import date, timedelta
from shutil import copy
from subprocess import getoutput

# Grab network interfaces using tshark
interfaces = getoutput("dumpcap -D")
interface_list = interfaces.split("\n")
for n in range(len(interface_list)):  # put interfaces into a list
    interface_list[n] = interface_list[n].split(" ")[1]

# Prompt user for interface to use
print(interfaces, "\n")
while True:
    try:
        interface_num = \
            int(input("What interface would you like to capture traffic on? Input the corresponding number: "))
        if 0 < interface_num <= len(interface_list):  # Valid selection
            interface = interface_list[interface_num - 1]
            break
        else:
            print("Invalid selection!")
    except ValueError:
        print("Need to enter the corresponding number to the interface!")

valid_date = False
start_year = 0
start_month = 0
start_day = 0
start_date = ""
# Prompt user for Start Date
while not valid_date:
    try:
        while True:
            start_year = int(input("Input the Start Date year: "))
            if 2000 <= start_year <= 3000:
                break
            else:
                print("Invalid calendar year!")
        while True:
            start_month = int(input("Input the Start Date month: "))
            if 1 <= start_month <= 12:
                break
            else:
                print("Invalid calendar month!")
        print(month(start_year, start_month))
        while True:
            start_day = int(input("Input the Start Date day: "))
            if 1 <= start_day <= monthrange(start_year, start_month)[1]:
                valid_date = True
                start_date = date(start_year, start_month, start_day)
                break
            else:
                print("Not a valid day in specified month and year!")
    except (ValueError, calendar.IllegalMonthError, calendar.IllegalWeekdayError):
        print("Need to enter a valid calendar year!")

# Prompt user for day number for Start Date
valid_entry = False
start_day_number = 1
while not valid_entry:
    try:
        days_start_at_1 = input("Is this day Day 1? (Y/N) ")
        start_day_number = 1
        if days_start_at_1.lower() == "n":
            while True:
                start_day_number = int(input("What day # is it? "))
                if start_day_number > 0:
                    valid_entry = True
                    break
                else:
                    print("Invalid input! Enter a valid number!")
        elif days_start_at_1.lower() == "y":
            valid_entry = True
        else:
            print("Invalid input! Enter \"Y\" for Yes or \"N\" for No")
    except Exception as e:
        print(e)

valid_date = False
end_year = 0
end_month = 0
end_day = 0
end_date = ""
days_between = 0
# Prompt user for End Date
while not valid_date:
    try:
        while True:
            end_year = int(input("Input the End Date year: "))
            if 2000 <= end_year <= 3000:
                break
            else:
                print("Invalid calendar year!")
        while True:
            end_month = int(input("Input the End Date month: "))
            if 1 <= end_month <= 12:
                break
            else:
                print("Invalid calendar month!")
        print(month(end_year, end_month))
        while True:
            end_day = int(input("Input the End Date day: "))
            if 1 <= end_day <= monthrange(end_year, end_month)[1]:
                end_date = date(end_year, end_month, end_day)
                days_between = (end_date - start_date).days
                if days_between > 0:
                    valid_date = True
                    break
                else:
                    print("End Date must be after Start Date!")
            else:
                print("Not a valid day in specified month and year!")
    except (ValueError, calendar.IllegalMonthError, calendar.IllegalWeekdayError):
        print("Need to enter a valid End Date!")

# Prompt user for Start Time
while True:
    try:
        start_time = input("Input the start time for each day's capture in 24 hr format (ex. 14:00): ")
        start_hour = start_time.split(":")[0]
        start_min = start_time.split(":")[1]
        if 0 <= int(start_hour) <= 23 and 0 <= int(start_min) <= 59 and \
                (1 <= len(start_hour) <= 2) and (len(start_min) == 2):
            if len(start_hour) == 1:
                start_hour = "0" + start_hour
            break
        else:
            print("Invalid time!")
    except (IndexError, ValueError):
        print("Invalid input! Input time in 24 hr format with a colon (ex. 14:00)")

# Prompt user for Duration
while True:
    try:
        hours = input("Input the number of hours that each capture should run: ")
        if int(hours) > 0:
            seconds = str(int(hours) * 60 * 60)
            break
        else:
            print("Invalid number of hours! Enter a value greater than 0")
    except ValueError:
        print("Invalid input!")

# Prompt user for root directory of capture
root_dir = ""
successful_path = False
while not successful_path:
    readline.set_completer_delims(' \t\n=')
    readline.parse_and_bind("tab: complete")
    root_dir = input("Input the absolute path where data will be captured and organized: ")
    if not os.path.exists(root_dir) or os.path.isfile(root_dir):
        print("Path invalid!")
    else:
        successful_path = True
        if root_dir[-1] != "/":
            root_dir += "/"

# Prompt user for file size of each pcap
while True:
    file_size = input("Input how many kilobytes a PCAP should be before splitting: ")
    try:
        if int(file_size) > 0:
            break
        else:
            print("Invalid value for kilobytes!")
    except Exception as e:
        print(e)

# Prompt user for filename
output_filename = input("Input the base filename for the PCAPs, without extension (.pcap will be added): ")

# Prompt user for zip time
while True:
    zip_time = input("A zip will be created for each pcap. What time should zipping occur? Enter in 24 hr format (ex. "
                     "13:00): ")
    try:
        zip_hour = zip_time.split(":")[0]
        zip_min = zip_time.split(":")[1]
        if 0 <= int(zip_hour) <= 23 and 0 <= int(zip_min) <= 59 and (1 <= len(zip_hour) <= 2) and (len(zip_min) == 2):
            if len(zip_hour) == 1:
                zip_hour = "0" + zip_hour
            break
        else:
            print("Invalid time!")
    except (IndexError, ValueError):
        print("Invalid input! Input time in 24 hr format with a colon (ex. 14:00)")

# Prompt user about initializing directories, initialize if prompted to do so
while True:
    create_directories = \
        input("Would you like this script to initialize the directories in the specified capture directory? (Y/N) ")
    try:
        if create_directories.lower() == "y" or create_directories.lower() == "n":
            directory_paths = []
            for day in range(days_between + 1):
                curr_path = root_dir + "day" + str(start_day_number + day) + "/"
                directory_paths.append(curr_path)
                if create_directories.lower() == "y" and not os.path.isdir(curr_path):
                    os.mkdir(curr_path)
            break
        else:
            print("Invalid input! Enter \"Y\" for Yes or \"N\" for No")
    except Exception as e:
        print(e)

# Verify that archiver.sh is inside the user-specified root directory for captures. Offer to copy it there if it is not.
if not os.path.isfile(root_dir + "archiver.sh"):
    while True:
        copy_archiver = input("archiver.sh script is required to be in the specified capture directory in order to "
                              "schedule zipping. Would you like this script to copy it there now? (Y/N) ")
        if copy_archiver.lower() == "n":
            print("archiver.sh will not be copied to " + root_dir)
            print("Scheduled zipping will not work")
            break
        if copy_archiver.lower() == "y":
            if os.path.isfile(os.getcwd() + "/archiver.sh"):
                copy(os.getcwd() + "/archiver.sh", root_dir)
                print("archiver.sh.sh successfully copied to " + root_dir)
                break
            else:
                print("archiver.sh not found! Please ensure archiver.sh is in the same directory as this script!")
        else:
            print("Invalid input! Enter \"Y\" for Yes or \"N\" for No")

# Iterate through directory path and create capture entries
print("\nUse 'crontab -e' and append the following lines to the file:\n")
for path in directory_paths:
    delta = timedelta(days=1)
    cron_line = start_min + " " + start_hour + " " + str(start_date.day) + " " + str(start_date.month) + " * "
    cmd = "dumpcap -P -i " + interface + " -a duration:" + seconds + " -b filesize:" + file_size + " -w " + path + \
          output_filename + "_" + path.split("/")[-2] + ".pcap"
    cron_line += cmd
    print(cron_line)
    start_date += delta
cron_line = zip_min + " " + zip_hour + " * * * " + root_dir + "archiver.sh " + root_dir + \
            " >> " + root_dir + "archiver_error_log.txt 2>&1"
print(cron_line)
