import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
from itertools import cycle
import time
import threading

#create the main window
root = tk.Tk()
root.title("Image Slideshow")
root.geometry("1000x700")

#create a frame for the image
box = tk.Frame(root, bg="#69defe", bd=25, relief=tk.RIDGE)
box.place(relx=0.5, rely=0.5, anchor='center', relheight=1, relwidth=1) \

#title label
tk.Label(box, text="Image Slideshower", bg="#000000", font=("Consolas", 30), fg="white").pack(pady=5, fill="x")

# Image Label (centered)
label = tk.Label(box, bg="#69defe")
label.place(relx=0.5, rely=0.5, anchor="center")

# Placeholder for images
photo_images = []
slideshow = None
stop_flag = None #used tom stop the loop if needed

def choose_images(): #creating a function to choose images
    global photo_images, slideshow
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.jpg *.png *.jpeg *.gif *.bmp")]
    )
    
    if not file_paths:
        return  # User cancelled
    
    display_size = (700, 600) # Size of the image to be displayed

    # Load, resize and store images
    images = []
    for path in file_paths:
        image = Image.open(path)
        image = ImageOps.exif_transpose(image)
        image.thumbnail(display_size, Image.LANCZOS)  # Resize to fit, maintaining aspect ratio
        photo = ImageTk.PhotoImage(image)
        images.append(photo)

    photo_images.clear()
    photo_images.extend(images)
    slideshow = cycle(photo_images)

def update_image(): #function to update the image
    global stop_flag
    while not stop_flag:
        for img in slideshow:
            if stop_flag:
                break
            label.config(image=img)
            label.image = img # prevent garbage collection
            label.update()
            time.sleep(3) #timer to change the image every 3 seconds

def start_slideshow(): #creating a function for start the slide show
    if not photo_images:
        return
    global stop_flag
    stop_flag = False
    threading.Thread(target=update_image, daemon=True).start()

def stop_slideshow(): #creating a function for stop the slide show
    global stop_flag
    stop_flag = True

# Buttons
#button to select the images
select_button = tk.Button(box, bg="#3D3F41", fg="white", bd=5, text="Choose Images", command=choose_images, font=("Arial", 14), width=15)
select_button.place(relx=0.2, rely=0.95, anchor='s') #place the button in the bottom left corner

#button to start the slideshow
play_button = tk.Button(box, bg="#75FB75", bd=5, text="Play", command=start_slideshow, font=("Arial", 14), width=15)
play_button.place(relx=0.4, rely=0.95, anchor='s') #place the button in the bottom center

#button to stop the slideshow
stop_button = tk.Button(box, bg="#FA0B0B", bd=5, text="Stop", command=stop_slideshow, font=("Arial", 14), width=15)
stop_button.place(relx=0.6, rely=0.95, anchor='s') #place the button in the bottom center

#button to exit the program
exit_button = tk.Button(box, bg="#F2EFEF", bd=5, text="Exit", command=root.destroy, font=("Arial", 14), width=15)
exit_button.place(relx=0.8, rely=0.95, anchor='s') #place the button in the bottom right corner

box.update_idletasks() #update the window to get the size of the buttons

root.mainloop() #start the main loop of the program
