import pygame, os, time, mutagen, tkinter
from pygame import mixer
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from mutagen.mp3 import MP3

font1 = "Roboto"
bg1 = "#171717"
bg2 = "#373737"
fg1 = "White"

global play
play = False
global pause
pause = False
global songLength
global loop
loop = False

def playstopsong():
    global play
    if not play:
        playsong()
    else:
        stopsong()
        
def playsong(song = "", sliding = False):
    global songLength
    global loop
    playbtn.config(text = "Stop")
    if song == "":
        song = playlist.get(ACTIVE)
    if sliding == False:
        resumesong()
        sliderPosition = int(songLength)
        slider.config(to = sliderPosition, value = 0)
        if not loop:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.rewind()
    else:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops = 0, start = int(slider.get()))
    global play
    play = True
        
def stopsong():
    resumesong()
    playbtn.config(text = "Play")
    currentsong = playlist.get(ACTIVE)
    pygame.mixer.music.stop()
    slider.config(value = 0)
    global play
    play = False
        
def pauseresumesong():
    global pause
    if not pause:
        pausesong()
    else:
        resumesong()

def pausesong():
    global pause
    pausebtn.config(text = "Resume")
    pygame.mixer.music.pause()
    pause = True

def resumesong():
    global pause
    pausebtn.config(text = "Pause")
    pygame.mixer.music.unpause()
    pause = False

def nextSong():
    nextOne = playlist.curselection() 

    nextOne = nextOne[0]+1
    currentsong = playlist.get(nextOne)

    if currentsong != "":
        playsong(currentsong)

        playlist.selection_clear(0, END)
        
        playlist.activate(nextOne)
        playlist.selection_set(nextOne, last=None)
    else:
        currentsong = playlist.get(0, last=None)
        playsong()

        playlist.selection_clear(0, END)
        
        playlist.activate(0)
        playlist.selection_set(0, last=None)

    slider.config(value = 0)

    
def previousSong():
    prevOne = playlist.curselection() 

    prevOne = prevOne[0]-1
    currentsong = playlist.get(prevOne)

    if currentsong != "":
        playsong(currentsong)

        playlist.selection_clear(0, END)
        
        playlist.activate(prevOne)
        playlist.selection_set(prevOne, last=None)
    else:
        currentsong = playlist.get(END, last=None)
        playsong()

        playlist.selection_clear(0, END)
        
        playlist.activate(END)
        playlist.selection_set(END, last=None)

    slider.config(value = 0)

#Add/Delete songs
def addSong():
    songs = filedialog.askopenfilenames(initialdir='Desktop/', title="Choose A Song", filetypes=(("MP3 Files", "*.mp3"), ))	

    # Loop through song list and replace directory info and mp3
    for song in songs:
	    song.replace(f"C:/Users/plant/Desktop/HollowKnightOSTPlaylist/{song}", "")
	    song.replace(".mp3", "")
	    playlist.insert(END, song)
	
def deleteSong():
	stop()
	song_box.delete(ANCHOR)
	pygame.mixer.music.stop()

def deleteAllSongs():
	stop()
	song_box.delete(0, END)
	pygame.mixer.music.stop()
 
root = Tk()
root.title('MP3 Player')
root.iconphoto(False, PhotoImage(file = "MusicIcon.png"))
root.configure(bg = bg2)
pygame.mixer.init()

playlist = Listbox(root, selectmode = SINGLE, bg = bg1, fg = fg1, font = (font1, 15), width=40)
playlist.pack()

os.chdir('C:/Users/plant/Desktop/HollowKnightOSTPlaylist')
songs = os.listdir()
    
for s in songs:
    playlist.insert(END,s)
    
def songTime():
    currentsong = playlist.get(ACTIVE)

    songMutagen = MP3(currentsong)
    global songLength
    songLength = songMutagen.info.length

    currentTime = pygame.mixer.music.get_pos() / 1000
    convertedCurrentTime = time.strftime('%M:%S', time.gmtime(currentTime))

    songLength = songMutagen.info.length
    convertedSongLength = time.strftime('%M:%S', time.gmtime(songLength))

    currentTime +=1

    global pause
    global play	
    if int(slider.get()) == int(songLength):
        if not loop:
            nextSong()
        else:
            playsong()
    elif pause:
        statusbar.config(text = f'Paused: {currentsong} - {convertedCurrentTime}  of  {convertedSongLength}  ')
    elif not play:
        statusbar.config(text = f'Selecting: {currentsong}')
    elif int(slider.get()) == int(currentTime):
        sliderPosition = int(songLength)
        slider.config(to=sliderPosition, value=int(currentTime))
    else:
        # Update Slider To position
        sliderPosition = int(songLength)
        slider.config(to=sliderPosition, value=int(slider.get()))
            
        convertedCurrentTime = time.strftime('%M:%S', time.gmtime(int(slider.get())))

        statusbar.config(text = f'Playing: {currentsong} - {convertedCurrentTime}  of  {convertedSongLength}  ')

        nextTime = int(slider.get()) + 1
        slider.config(value=nextTime)

    statusbar.after(1000, songTime)

def slide(x):
    playsong("", True)

def shuffle():
    pass

def loopunloop():
    global loop
    if not loop:
        loopsong()
    else:
        unloopsong()

def loopsong():
    global loop
    loop = True

def unloopsong():
    global loop
    loop = False

#UI
mainFrame = Frame(root)
mainFrame.pack(pady = 20)
mainFrame.configure(bg = bg2)
    
frame = Frame(mainFrame)
frame.grid(row = 1, column = 0, pady = 20)
frame.configure(bg = bg2)

trough = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x90\x08\x06\x00\x00\x00"\x18\xbal\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\n\xfc\x00\x00\n\xfc\x01\x99\xdb\xbb\xef\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x00\x1fIDAT8\x8dc\\\xb5j\xd5\x7f\x06\x06\x06\x06&\x06(\x18e\x8c2F\x19\xa3\x8c\x91\xc9\x00\x00\xf7\xe7\x04\x1dd\xcc\xbe\x83\x00\x00\x00\x00IEND\xaeB`\x82'
slider = b'iVBORw0KGgoAAAANSUhEUgAAABoAAAAYCAYAAADkgu3FAAAABHNCSVQICAgIfAhkiAAAAohJREFUSIm1lj1oFEEUx387s3uikLu9L4OFkaiIVUQFDVik0CIoA5YGEa0sLezUJtjYiGXSahFiv0gCASFCQMUgplajgmgSN3vrFcltZm8sbi+uH5cP3fyrx9vh/ea9hfcfiw3keZ4ABgAF9AMHgb3J50XgPfAc8IBppVSzUy2rA0AC14BbwKGNLpPSO+Ae8FApFW8K8jzvMDAGnEpS88Bj27ZXSqXSHcuyckk+NsbExphmGIa1KIr2JfmXwGWl1NuOIM/zztAaQ9FxnK/5fN6xbbsA2Jt0Y4wxa2EYfm80GhUgAJRSaqZ9QKQgx4EJoCilnCoWi0XbtstbgABYlmXlXNctO44zAxSBiaTmz448z+sC3gC9tm1PlEqls6kRbVfN5eXlp2tra+dojf2YUqre7mgY6AVmXdft/w8IgCgUCieB2aTmMIDleV4V+AjsEkJcqVarY/8BWZfv+ze11veBBnBAAEPAbuBJVhCAcrn8IJfLvUpqDwlgEEBK+SIrSFuu655IwkEB9CXJG1mDLMuSSdgngG4A27YrWYOMMVESdotUvuOe+lelOkIACwBa68WsQSktCGAOoFarjewAoD2xOQFMAsRxfDprijGm/TsmBTAOrAAXtNbfsuTUajWR1B4XSqklYBQQ9Xp9GTBZQMIw/BBFkQBGlVJL6V03H0XRkSAIngF/GNdWpbX+4vv+5Orqai+tpToMKT9KVvo00CWlnMrn8/tzudzR7UB837+utT4PXATqwIBS6vUvoAS2bnzAJynlo0qlchuQbKA4jv0gCEbiOL4K9PAX49vUyh3H+VwoFLqklHtSxyyt9WIQBHebzWYPcImWJcBWrDwF2/nHyW/AzJ5bPwBL8fcMWSkkpQAAAABJRU5ErkJggg=='

img_trough = tkinter.PhotoImage(master=root, data=trough)
img_slider = tkinter.PhotoImage(master=root, data=slider)

style = ttk.Style(root)
style.element_create('custom.Scale.trough', 'image', img_trough)
style.element_create('custom.Scale.slider', 'image', img_slider)

style.layout('custom.Horizontal.TScale',
             [('Horizontal.Scale.trough',
               {'sticky': 'nswe',
                'children': [('custom.Horizontal.Scale.slider',
                              {'side': 'left', 'sticky': ''})]})])

style.configure('custom.Horizontal.TScale', background=bg1, foreground=fg1, troughcolor='#73B5FA')
 
slider = ttk.Scale(mainFrame, from_ = 0, to=100, orient = HORIZONTAL, value = 0, command = slide, length = 360, style = "custom.Horizontal.TScale")
slider.grid(row = 0, column = 0, pady = 10)

backbtn = Button(frame, text = "Previous", font = (font1, 20), command = previousSong, bg = bg1, fg = fg1).grid(row = 0, column = 0, padx = 10)
playbtn = Button(frame, text = "Play", font = (font1, 20), command = playstopsong, bg = bg1, fg = fg1)
playbtn.grid(row = 0, column = 1, padx = 10)
pausebtn = Button(frame, text = "Pause", font = (font1, 20), command = pauseresumesong, bg = bg1, fg = fg1)
pausebtn.grid(row = 0, column = 2, padx = 10)
nextbtn = Button(frame, text = "Next", font = (font1, 20), command = nextSong, bg = bg1, fg = fg1).grid(row = 0, column = 3, padx = 10)

le = "🔁"
se = "🔀"

otherFrame = Frame(mainFrame)
otherFrame.grid(row = 2, column = 0)
otherFrame.configure(bg = bg2)

shufflebtn = Button(otherFrame, text = se, font = (font1, 20), command = shuffle, bg = bg1, fg = fg1).grid(row = 1, column = 0, padx = 10)
loopbtn = Button(otherFrame, text = le, font = (font1, 20), command = loopunloop, bg = bg1, fg = fg1).grid(row = 1, column = 1, padx = 10)

statusbar = Label(root, text = '', bd=1, relief=GROOVE, anchor=E)
statusbar.pack(fill=X, side=BOTTOM)

#Menus
menu = Menu(root)
menu.config(bg = bg1, fg = fg1)
root.config(menu = menu)

addSongMenu = Menu(menu, tearoff = False)
menu.add_cascade(label = "Add Song", menu = addSongMenu)
addSongMenu.add_command(label="Add song", command = addSong)

songTime()
root.mainloop()

