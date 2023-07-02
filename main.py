from tkinter import *
from PIL import ImageTk, Image
import customtkinter
from pytube import YouTube
import requests, shutil
import atexit
import os
import threading
import time


def getInfo():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)
        videoTitle.configure(text= "Title: " + ytObject.author + " - " + ytObject.title, text_color="white")
        videoTime.configure(text="Time: " + str(ytObject.length//60) + ":" + str(ytObject.length%60), text_color="white")
        videoMem.configure(text="Size: " + "{:.2f}".format(ytObject.streams.get_highest_resolution().filesize/1024/1024) + " MB")
        downloadThumb()
        check = True
        while check:
            if os.path.exists("thumbnail.jpg"):
                check = False
                #picture
                image = Image.open("thumbnail.jpg")
                width, height = image.size
                photo = customtkinter.CTkImage(light_image=Image.open(os.path.join("thumbnail.jpg")), size=(width*0.3 , height*0.3))
                img.configure(image=photo)
    except:
        print("YouTube link is invalid")
        videoTitle.configure(text="An error occurred, please check the correctness of the link", text_color="red")

def downloadThumb():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)
        thumbnail_url = ytObject.thumbnail_url
        downloadImage(thumbnail_url,"thumbnail.jpg")
        print("Download Complete!")
    except:
        print("YouTube link is invalid")
        finishLabel.configure(text="An error occurred, please check the correctness of the link", text_color="red")

def downloadImage(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        videoTitle.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")
        video.download()
        print("Download Complete!")
        finishLabel.configure(text="Video downloaded", text_color="white")
    except:
        print("YouTube link is invalid")
        finishLabel.configure(text="An error occurred, please check the correctness of the link", text_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()
    #ProgressBar
    progressBar.set(float(percentage_of_completion) / 100)

def download():
    download_thread = threading.Thread(target=startDownload)
    download_thread.start()
#System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#App frame
app = customtkinter.CTk()
app.geometry("720x720")
app.title("YouTube Downloader")

#Adding UI Elements
title = customtkinter.CTkLabel(app, text="Insert link")
title.pack(padx=10, pady=10)

#Add link input
url_var = StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

#Info button
info = customtkinter.CTkButton(app,text="Get info", command=getInfo)
info.pack(padx=10, pady=10)

#Picture
img = customtkinter.CTkLabel(app, text='')
img.pack(padx=10, pady=10)

#videoTitle
videoTitle = customtkinter.CTkLabel(app, text="")
videoTitle.pack(padx=10, pady=10)

#videoTime
videoTime = customtkinter.CTkLabel(app, text="")
videoTime.pack(padx=10, pady=10)

#videoMemory
videoMem = customtkinter.CTkLabel(app, text="")
videoMem.pack(padx=10, pady=10)

#Download button
download = customtkinter.CTkButton(app,text="Get video", command=download)
download.pack(padx=10, pady=10)


#Finished downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack(padx=10, pady=10)

#Progress %
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app,width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)


#Run app in loop
app.mainloop()

atexit.register(delete_file, "thumbnail.jpg")
