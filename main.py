import os
import shutil
from tkinter import *
from tkinter import filedialog
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import sys
from PIL import Image, ImageTk

def app_folder_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.mixer.init()
folder = app_folder_path("music")
os.makedirs(folder, exist_ok=True)
mp3_files = [file for file in os.listdir(folder) if file.endswith(".mp3")]
currSongIndex = 0
looping = False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def add_songs():
    global mp3_files
    selected_files = filedialog.askopenfilenames(
        title = "Choose MP3 Files",
        filetypes = [("MP3 Files", "*.mp3")]
    )
    if not selected_files:
        return
    os.makedirs(folder, exist_ok=True)
    for file_path in selected_files:
        song_name = os.path.basename(file_path)
        destination = os.path.join(folder, song_name)
        shutil.copy(file_path, destination)
    refresh()

def refresh():
    global mp3_files
    mp3_files = [file for file in os.listdir(folder) if file.endswith(".mp3")]
    songList.delete(0, "end")
    for song in mp3_files:
        songList.insert("end", song)

def select_song(event):
    selected = songList.curselection()
    if selected:
        song_name = songList.get(selected[0])
        currentSongLabel.config(text=song_name)

def play_song(songIndex, loop=False):
    global currSongIndex

    currSongIndex = songIndex
    looping = loop
    song_name = mp3_files[currSongIndex]
    file_path = os.path.join(folder, song_name)

    pygame.mixer.music.load(file_path)

    if looping:
        pygame.mixer.music.play(loops=-1)
        currentSongLabel.config(text=f"Now Looping: {song_name}")
    else:
        pygame.mixer.music.play()
        currentSongLabel.config(text=f"Now Playing: {song_name}")

def playClickedSong(event=None):
    selected = songList.curselection()
    if selected:
        song_index = selected[0]
        play_song(song_index, False)

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()

def stop():
    pygame.mixer.music.stop()
    currentSongLabel.config(text="No song playing")

def skip():
    global currSongIndex
    currSongIndex += 1
    if currSongIndex >= len(mp3_files):
        currSongIndex = 0
    play_song(currSongIndex, False)

def loop():
    play_song(currSongIndex, loop=True)

#GUI
mpWindow = Tk()

#Primary Setting - Do not Modify!!!
mpWindow.geometry("350x500")
mpWindow.title("MP3 Player")
icon = PhotoImage(file=resource_path("button icons/mp3Window_Icon.png"))
mpWindow.iconphoto(True, icon)
mpWindow.config(background="#312F2F")
mpWindow.resizable(False, False)


#Song List scrollable
currentSongLabel = Label(
    mpWindow,
    text="No song selected",
    font=("Consolas", 13),
    fg="white",
    bg="#312F2F",
    anchor="center"
)
currentSongLabel.place(x=35, y=300, width=280, height=25)

songListFrame = Frame(mpWindow, bg="#535050")
songListFrame.place(x=30, y=45, width=290, height=240)
songList = Listbox(
    songListFrame,
    bg="#1F1E1E",
    fg="white",
    selectbackground="#B3D0B6",
    selectforeground="black",
    font=("Consolas", 11),
    borderwidth=0,
    highlightthickness=0,
    activestyle="none"
)
songList.pack(side=LEFT, fill=BOTH, expand=True)
scrollBar = Scrollbar(songListFrame)
scrollBar.pack(side=RIGHT, fill=Y)
songList.config(yscrollcommand=scrollBar.set)
scrollBar.config(command=songList.yview)

for song in mp3_files:
    songList.insert(END, song)

songList.bind("<<ListboxSelect>>", playClickedSong)


#Pause, Resume, Stop, Skip, Loop buttons
#remember to give buttons their function, already defined
pIcon = Image.open(resource_path("button icons/pauseButton_Icon.png"))
pIcon = pIcon.resize((60, 45))
pauseIcon = ImageTk.PhotoImage(pIcon)
pauseButton = Button(
    mpWindow,
    image = pauseIcon,
    command=pause,
    borderwidth=0,
    highlightthickness=0
)
pauseButton.place(x=43, y=400)

rIcon = Image.open(resource_path("button icons/resumeButton_Icon.png"))
rIcon = rIcon.resize((60, 45))
resumeIcon = ImageTk.PhotoImage(rIcon)
resumeButton = Button(
    mpWindow,
    image = resumeIcon,
    command=resume,
    borderwidth=0,
    highlightthickness=0
)
resumeButton.place(x=145, y=400)

sIcon = Image.open(resource_path("button icons/stopButton_Icon.png"))
sIcon = sIcon.resize((60, 45))
stopIcon = ImageTk.PhotoImage(sIcon)
stopButton = Button(
    mpWindow,
    image = stopIcon,
    command=stop,
    borderwidth=0,
    highlightthickness=0
)
stopButton.place(x=248, y=400)

skipI = Image.open(resource_path("button icons/skipButton_Icon.png"))
skipI = skipI.resize((60, 45))
skipIcon = ImageTk.PhotoImage(skipI)
skipButton = Button(
    mpWindow,
    image = skipIcon,
    command=skip,
    borderwidth=0,
    highlightthickness=0
)
skipButton.place(x=248, y=340)

lIcon = Image.open(resource_path("button icons/loopButton_Icon.png"))
lIcon = lIcon.resize((60, 45))
loopIcon = ImageTk.PhotoImage(lIcon)
loopButton = Button(
    mpWindow,
    image = loopIcon,
    command=loop,
    borderwidth=0,
    highlightthickness=0
)
loopButton.place(x=43, y=340)

aIcon = Image.open(resource_path("button icons/addButton_Icon.png"))
aIcon = aIcon.resize((30, 30))
addIcon = ImageTk.PhotoImage(aIcon)
addSongsButton = Button(
    mpWindow,
    image = addIcon,
    command = add_songs,
    borderwidth=0,
    highlightthickness=0
)
addSongsButton.place(x=320, y=0)

mpWindow.mainloop()