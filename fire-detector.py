import cv2
import numpy as np
import smtplib
import playsound
import threading
from IPython.display import display, clear_output
import matplotlib.pyplot as plt

Alarm_Status = False
Email_Status = False
Fire_Reported = 0

def play_alarm_sound_function():
    while True:
        playsound.playsound('alarm-sound.mp3', True)

'''def send_mail_function():
    recipientEmail = "Enter_Recipient_Email"
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("Enter_Your_Email", "Enter_Your_Password")
        server.sendmail("Enter_Your_Email", recipientEmail,
                        "⚠️ Warning: Fire Accident Detected in ABC Company")
        print(f"Email sent to {recipientEmail}")
        server.close()
    except Exception as e:
        print("Email error:", e)'''


# Video source: file or webcam (0 = default cam)
video = cv2.VideoCapture(0)  # Change to "video_file.mp4" if you have a video

while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (640, 360))
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = np.array([18, 50, 50], dtype="uint8")
    upper = np.array([35, 255, 255], dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame, frame, mask=mask)
    no_red = cv2.countNonZero(mask)

    if int(no_red) > 15000:
        Fire_Reported += 1

    # Show frame inside Jupyter
    clear_output(wait=True)
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    display(plt.gcf())

    if Fire_Reported >= 1:
        if not Alarm_Status:
            threading.Thread(target=play_alarm_sound_function).start()
            Alarm_Status = True
        '''if not Email_Status:
            threading.Thread(target=send_mail_function).start()
            Email_Status = True'''

    # Exit condition (press 'q' in webcam window) – in Jupyter we simulate with break after some frames
    if Fire_Reported > 5:  # <- adjust to stop automatically
        break

video.release()
cv2.destroyAllWindows()