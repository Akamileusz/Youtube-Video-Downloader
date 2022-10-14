import io
import os
import tkinter as tk
from pytube import YouTube
import urllib
from PIL import ImageTk, Image

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry = ('1280x1280')
        self.root.iconbitmap('icon.ico')
        self.root.minsize(width='1280', height='1024')
        self.root.resizable(False,False)
        self.root.title('Gówno')

        self.FONT_ENTRY = ('Courier', 20)

        self.yt_photo = tk.PhotoImage(file='s.png')
        self.button_mp4_img = tk.PhotoImage(file='download_button_mp4.png')
        self.button_mp3_img = tk.PhotoImage(file='download_button_mp3.png')

        self.build_elements()

        self.root.mainloop()

    def build_elements(self):

        self.photo = tk.Label(self.root, image=self.yt_photo)
        self.photo.grid(row=0, column=0, sticky=tk.NW, padx=20, pady=15)
        self.photo.place(relx=0.35, rely=0.1, anchor=tk.CENTER)

        self.title = tk.Label(self.root, text='Downloader', font=('Courier', 30))
        self.title.grid(row=0, column=2, sticky=tk.NE, pady=60)
        self.title.place(relx=0.6, rely=0.1, anchor=tk.CENTER)

        self.entry_box = tk.Entry(self.root, font=self.FONT_ENTRY, width=60)
        self.entry_box.grid(row=0, column=0)
        self.entry_box.place(relx=0.45, rely=0.2, anchor=tk.CENTER)

        self.button = tk.Button(self.root, text='Convert', font=('Arial', 15, 'bold'), height=1, command=self.convert)
        self.button.grid(row=0, column=0)
        self.button.place(relx=0.85, rely=0.2, anchor=tk.CENTER)

        self.video_title = tk.Label(self.root, text='', font=('Helvetica', 25))
        self.video_title.grid(row=0, column=0)
        self.video_title.place(relx=0.5, rely=0.28, anchor=tk.CENTER)

        self.time_label = tk.Label(self.root, text=f'', font=('Helvetica', 25))
        self.time_label.grid(row=0, column=0)
        self.time_label.place(relx=0.35, rely=0.74, anchor=tk.CENTER)

        self.author_label = tk.Label(self.root, text='', font=('Helvetica', 25))
        self.author_label.grid(row=0, column=0)
        self.author_label.place(relx=0.65, rely=0.74, anchor=tk.CENTER)


    def build_buttons(self):

        self.button_mp4 = tk.Button(self.root, image=self.button_mp4_img, command=self.download_mp4)
        self.button_mp4.grid(row=0,column=0)
        self.button_mp4.place(relx=0.25, rely=0.85, anchor=tk.CENTER)

        self.button_mp3 = tk.Button(self.root, image=self.button_mp3_img, command=self.download_mp3)
        self.button_mp3.grid(row=0, column=0)
        self.button_mp3.place(relx=0.75, rely=0.85, anchor=tk.CENTER)


    def convert(self):

        self.url = str(self.entry_box.get())
        self.url1 = YouTube(self.url)
        self.video = self.url1.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        self.audio = self.url1.streams.filter(only_audio=True).first()
        self.title_video = self.url1.title
        self.length_video = self.url1.length
        self.thumbnail_url = self.url1.thumbnail_url
        self.author_video = self.url1.author

        self.build_thumbnail()
        self.build_misc()

        self.video_title.config(text=self.title_video)
        self.build_buttons()


    def build_thumbnail(self):

        self.raw_data = urllib.request.urlopen(self.thumbnail_url).read()
        self.img = Image.open(io.BytesIO(self.raw_data))
        self.img = self.img.resize((480, 360))
        self.thumbnail_img = ImageTk.PhotoImage(self.img)
        self.thumbnail = tk.Label(self.root, image=self.thumbnail_img)
        self.thumbnail.grid(row=0, column=0)
        self.thumbnail.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


    def build_misc(self):

        minutes = self.length_video / 60
        seconds = self.length_video % 60
        hours = minutes / 60

        if minutes >= 60:
            minutes = minutes % 60

        self.time = '%d:%02d:%02d' % (hours, minutes, seconds)

        self.time_label.config(text=f'Duration: {self.time}')
        self.author_label.config(text=('By ' + self.author_video))


    def download_mp4(self):
        self.video.download()

    def download_mp3(self):
        self.filename = self.audio.download()
        os.rename(self.filename, f'{self.filename[0:-4]}' + '.mp3')


Window()
