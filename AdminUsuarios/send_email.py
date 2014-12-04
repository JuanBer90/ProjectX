#!/usr/bin/python
# -*- coding: UTF8-*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from projectx.settings import BASE_DIR
import urllib



# me == my email address
# you == recipient's email address

def SendMail(password="",username="",correo=""):

    me = "soporte.projectx@gmail.com"
    you = correo
    my_password = "IS2final"
   
        
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Bienvenido/a"
    msg['From'] = me
    msg['To'] = you
    
    
    # Create the body of the message (a plain-text and an HTML version).
    text = ""
    f = open(str(BASE_DIR)+'/templates/mensaje_bienvenida.txt', 'r')
    html=f.read()
    vector=html.split("<li><b>Username:</b>")
    html=vector[0]+"<li><b>USERNAME: </b>"+username+vector[1]
    vector=html.split("<li><b>Password:</b>")
    html=vector[0]+"<li><b>PASSWORD:  </b>"+password+vector[1]

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
   
    msg.attach(part1)
    msg.attach(part2)
    
    s = smtplib.SMTP("smtp.gmail.com:587")
    s.starttls()
    s.login(me, my_password)
    s.sendmail(me, you, msg.as_string())
    s.quit()
    
def SendPassword(password="",username="",correo=""):

    
    me = "soporte.projectx@gmail.com"
    you = correo
    my_password = "IS2final"
   
        
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Recuperacion de Password"
    msg['From'] = me
    msg['To'] = you
    
    
    # Create the body of the message (a plain-text and an HTML version).
    text = ""
    f = open(str(BASE_DIR)+'/templates/mensaje_password.txt', 'r')
    html=f.read()
    print html
    vector=html.split("username")
    print len(vector),"   longituuuuud"
    html=vector[0]+username+vector[1]
    vector=html.split("<li><b>Password:</b>")
    html=vector[0]+"<li><b>Password: </b>"+password+vector[1]

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
   
    msg.attach(part1)
    msg.attach(part2)
    
    s = smtplib.SMTP("smtp.gmail.com:587")
    s.starttls()
    s.login(me, my_password)
    s.sendmail(me, you, msg.as_string())
    s.quit()
    
