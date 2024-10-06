import pyautogui
import time
import pandas as pd
from datetime import datetime
import webbrowser
import os
import sys
import timeit
from datetime import datetime
import csv

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

'''
Thes are the join button/input box coordinates and regions for different buttons on my mac when chrome opens zoom
You will need to change these as they may be different for your os/laptop combination
This is for performance as finding images is slow so we want to do it minimally.

The easiest way to figure these out for your system wil be to do the following:

print(pyautogui.locateOnScreen('waiting_for_the_host_to_start_this_meeting.png')
which will output this:

Box(left=1712, top=714, width=206, height=42)

Use those for the region:)

To run:
pip install pyautogui
python manage.py
'''
JOIN_X,JOIN_Y = 950,650
SIGN_IN_TO_JOIN_REGION = (1712,714, 206,42)
HOST_HAS_ANOTHER_MEETING_REGION = (1402,466,626,66)
WAITING_FOR_THE_HOST_REGION = (1296,490,834,84)
ENTER_MEETING_PASSWORD_REGION = (1348,816,458,52)
JOIN_WITH_VIDEO_REGION = (2014,1438,288,92)
MEETING_ID_IS_NOT_VALID_REGION =(1372,572,312,36)
LEAVE_MEETING_REGION = (2666,1522,152,66)

pyautogui.PAUSE = 1

def get_meeting_status(password):
   
    if pyautogui.locateOnScreen('waiting_for_the_host_to_start_this_meeting.png',region=WAITING_FOR_THE_HOST_REGION):
        return 'Valid - meeting accessed'
    elif pyautogui.locateOnScreen('enter_meeting_password.png',region=ENTER_MEETING_PASSWORD_REGION):
        if password:
            time.sleep(2)
            pyautogui.typewrite(password+'\t')
            pyautogui.click(JOIN_X,JOIN_Y)
            if pyautogui.locateOnScreen('waiting_for_the_host_to_start_this_meeting.png',region=WAITING_FOR_THE_HOST_REGION):
                return 'Valid - Password supplied and works'
            else:
                return 'Invalid - Password supplied but is wrong'
        else:
            return 'Invalid - Password required but not provided'
    elif pyautogui.locateOnScreen('join_with_video.png',region=JOIN_WITH_VIDEO_REGION):
        return 'Valid - meeting accessed'
    elif pyautogui.locateOnScreen('the_host_has_another_meeting.png',region=HOST_HAS_ANOTHER_MEETING_REGION):
        return 'Valid - the host has another meeting running'
    elif pyautogui.locateOnScreen('sign_in_to_join.png',region=SIGN_IN_TO_JOIN_REGION):
        return 'Invalid - requires sign in to zoom'
    elif pyautogui.locateOnScreen('this_meeting_is_not_valid.png',region=MEETING_ID_IS_NOT_VALID_REGION):
        return 'Invalid - link not valid'
    elif pyautogui.locateOnScreen('leave.png',region=LEAVE_MEETING_REGION):
        return 'Valid - meeting opened'
    else:
        return 'Unknown status - needs a human eyeball'


def open_meeting_and_return_status(id,title,day,link,email,password):
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open(link)
    time.sleep(4)
    meeting_status = get_meeting_status(password)
    df.loc[df['id'] == id,'meeting_status'] = meeting_status
    os.system("pkill zoom.us")
    return meeting_status


start = timeit.default_timer()
df = pd.read_csv('meetings.csv')
df['password'] = df.description.str.extract(r'([Pp]assword: \w\S*\S)', expand=False)
df['password'] = df['password'].str.replace('password: ', '')
df['password'] = df['password'].str.replace('Password: ', '')
df['meeting_status'] = 'Unknown'
df = df.fillna('')


with open('meetings_with_status.csv', 'w') as csvfile: 
         writer = csv.writer(csvfile) 
         writer.writerow(['id','title','day','link','time','description','email','password','status']) 
         for index, row in df.iterrows():
            id, title, day, link, start_time, description, email,password = row[0], row[1], row[2],\
                row[3], row[4], row[5], row[6],row[7]
            status=open_meeting_and_return_status(id,title,day,link,email,password)
            writer.writerow([id, title, day, link, start_time, description, email,password,status])
            if index%50==0 and index>0:
                os.system("pkill Chrome")



stop = timeit.default_timer()
total_time = stop - start
mins, secs = divmod(total_time, 60)
hours, mins = divmod(mins, 60)

sys.stdout.write("Total running time: %d:%d:%d.\n" % (hours, mins, secs))