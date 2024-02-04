import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import filedialog, Menu, Label, Listbox, Button, Scale, Frame, Scrollbar
import pygame
import os
import random
import time

root = tk.Tk()  # initialize the window
root.title('Turbo Player')

# Set the icon for the application
icon_path = 'TC 3d.ico'
root.iconbitmap(icon_path)

# Set the background image
background_image_path = r'D:\MP\s.jpg'

# Open and convert the image using Pillow
background_image = Image.open(background_image_path)
background_image = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

root.resizable(True, True)

pygame.mixer.init()  # to load, play, pause, unpause the music

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False

control_frame = Frame(root)
control_frame.pack()

volume_scale = Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                     label="Volume", command=lambda x: pygame.mixer.music.set_volume(int(x) / 100))
volume_scale.set(50)  # Set initial volume to 50%
volume_scale.grid(row=0, column=10, padx=7, pady=10)

status_label = Label(root, text="Now Playing: ", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

# Create a Frame to hold the Listbox, Scrollbar, and Image
content_frame = Frame(root)
content_frame.pack(pady=10)

# Create a Label for displaying the image
image_label = Label(content_frame)
image_label.pack(side=tk.RIGHT, padx=10)

repeat_mode = False

def load_music():
    global current_directory, songs, current_song
    current_directory = filedialog.askdirectory()

    for song in os.listdir(current_directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3' or ext == '.wav':
            songs.append(os.path.join(current_directory, song))

    for song in songs:
        songlist.insert("end", os.path.basename(song))

    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]

def add_songs_to_playlist():
    global songs, current_directory
    additional_songs = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
    if additional_songs:
        current_directory = os.path.dirname(additional_songs[0])
        songs.extend(additional_songs)
        songlist.delete(0, tk.END)  # Clear the existing list
        for song in songs:
            songlist.insert(tk.END, os.path.basename(song))

def play_music():
    global current_song, paused, current_directory

    # Use the full path to the song
    song_path = os.path.join(current_directory, current_song)
    status_label.config(text="Now Playing: " + os.path.basename(current_song))

    # Initialize folder_image outside the if block
    folder_image = None

    # Load the folder image from the current directory if it exists
    folder_image_path = os.path.join(current_directory, "Folder.jpg")
    if os.path.exists(folder_image_path):
        original_folder_image = Image.open(folder_image_path)

        # Resize the folder image to a fixed size
        fixed_size = (400, 400)  # Adjust the size as needed
        resized_folder_image = original_folder_image.resize(fixed_size, Image.ADAPTIVE)

        folder_image = ImageTk.PhotoImage(resized_folder_image)

    if not paused:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        if folder_image:
            image_label.configure(image=folder_image)
            image_label.image = folder_image  # Keep a reference to avoid garbage collection
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def prev_music():
    global current_song, paused, current_directory

    try:
        songlist.selection_clear(0, tk.END)
        prev_index = (songs.index(current_song) - 1) % len(songs)
        songlist.selection_set(prev_index)
        current_song = songs[prev_index]
        current_directory = os.path.dirname(current_song)  # Set the current directory for the new song
        play_music()
    except:
        pass

def next_music():
    global current_song, paused, current_directory

    try:
        songlist.selection_clear(0, tk.END)
        next_index = (songs.index(current_song) + 1) % len(songs)
        songlist.selection_set(next_index)
        current_song = songs[next_index]
        current_directory = os.path.dirname(current_song)  # Set the current directory for the new song
        play_music()
    except:
        pass

def shuffle_music():
    global songs, current_song
    random.shuffle(songs)
    songlist.delete(0, tk.END)
    for song in songs:
        songlist.insert(tk.END, song)
    songlist.selection_set(songs.index(current_song))

def Repeat_music():
    global repeat_mode
    repeat_mode = not repeat_mode
    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # Reset end event
    if repeat_mode:
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # Set end event to loop the song
    else:
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Reset end event for normal behavior

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
organise_menu.add_command(label='Add Songs', command=add_songs_to_playlist)
menubar.add_cascade(label='Organise', menu=organise_menu)


# Set the background color of the Listbox to match the root window background
listbox_bg_color = root.cget("bg")

# Create a Frame to hold the Listbox and Scrollbars
listbox_frame = Frame(root)
listbox_frame.pack(pady=10)

# Create a Scrollbar for the Listbox
vertical_scrollbar = Scrollbar(listbox_frame, orient=tk.VERTICAL)

# Create a Canvas as the background
canvas = tk.Canvas(content_frame, bg="black", height=50, width=400)
canvas.pack(expand=tk.YES, fill=tk.BOTH)

# Add text to the Canvas
canvas.create_text(200, 30, text="Turbo Player", font=("Helvetica", 16), fill="white")

# Set up the Listbox with Scrollbars on the Canvas
songlist = Listbox(content_frame, fg="white", font="bold", bg="black", height=10, width=10,
                   highlightthickness=10, selectbackground=listbox_bg_color, yscrollcommand=vertical_scrollbar.set)
vertical_scrollbar = Scrollbar(content_frame, orient=tk.VERTICAL, command=songlist.yview)
songlist.config(yscrollcommand=vertical_scrollbar.set)

# Configure the Scrollbar to work with the Listbox
vertical_scrollbar.config(command=songlist.yview)

# Pack the Listbox and Scrollbar on the Canvas
songlist_window = canvas.create_window(5, 5, anchor=tk.SW, window=songlist)

vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#Location of the .img files
play_btn_image = ImageTk.PhotoImage(file='play.png')
pause_btn_image = ImageTk.PhotoImage(file='pause.png')
next_btn_image = ImageTk.PhotoImage(file='next.png')
previous_btn_image = ImageTk.PhotoImage(file='previous.png')
shuffle_btn_image = ImageTk.PhotoImage(file='arrow.png')
Repeat_btn_image = ImageTk.PhotoImage(file='Repeat.png')

#Functioning/Working and appearance of the button
play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music)
previous_btn = Button(control_frame, image=previous_btn_image, borderwidth=0, command=prev_music)
shuffle_btn = Button(control_frame, image=shuffle_btn_image, borderwidth=0, command=shuffle_music)
Repeat_btn = Button(control_frame, image=Repeat_btn_image, borderwidth=0, command=Repeat_music)

#Sequence and padding
play_btn.grid(row=0, column=2, padx=7, pady=10)
pause_btn.grid(row=0, column=3, padx=7, pady=10)
next_btn.grid(row=0, column=4, padx=7, pady=10)
previous_btn.grid(row=0, column=1, padx=7, pady=10)
shuffle_btn.grid(row=0, column=0, padx=7, pady=10)
Repeat_btn.grid(row=0, column=5, padx=7, pady=10)

songlist.pack_propagate(False)  # Prevent Listbox from affecting its parent's geometry
songlist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

control_frame = Frame(root)
control_frame.pack()

root.mainloop()
