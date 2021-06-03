# import libraries
import sys
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import base64

from PIL import Image, ImageTk
from Decode import decode
from tkinter.filedialog import askopenfile, Label
from tkinter.messagebox import showinfo

from cryptography.fernet import Fernet

from Substitution import Substitution

np.set_printoptions(threshold=sys.maxsize)

root = tk.Tk()


canvas = tk.Canvas(root, width=1500, height=700)
canvas.grid(columnspan=2)

image = Image.open('Insert-Photo-Here.jpg')
res_image = image.resize((300, 300))
img = ImageTk.PhotoImage(res_image)
label = Label(image=img)
label.image = img

label.place(relx=0.25, rely=0.2, anchor='n')

label1 = Label(image=img)
label1.image = img
label1.place(relx=0.75, rely=0.2, anchor='n')

var = tk.IntVar()



def encode():
    myLabel = Label(root, text=var.get()).place(relx=0.5, rely=0.5, anchor='n')
    choice = var.get()
    if choice ==1:
        alphabet = Substitution.alphabet
        key = 'dskjwtzlecpaxfbovhumiryqgn'  # key previously generated using makeKey function from Susbtitution_encryption.Substitution class
        message = e1.get()
        message = Substitution.encrypt(message,key,alphabet)
    elif choice ==0:
        message = e1.get()

    dest = e2.get()
    file = askopenfile(mode='rb', title='Choose a file')
    img = Image.open(file)
    width, height = img.size
    array = np.array(list(img.getdata()))
    res_image = img.resize((300, 300))
    image2 = ImageTk.PhotoImage(res_image)
    label.configure(image=image2)
    label.image = image2

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")


# decoding function
def decode():
    file = askopenfile(mode='rb', title='Choose a file')
    img = Image.open(file)
    array = np.array(list(img.getdata()))
    res_image = img.resize((300, 300))
    image2 = ImageTk.PhotoImage(res_image)
    label1.configure(image=image2)
    label1.image = image2

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        print("Hidden Message:", message[:-5])
        text_box.insert(1.0, message[:-5])
    else:
        print("No Hidden Message Found")
        text_box.insert(1.0, "No Hidden Message Found")


# instructions

instruction1 = tk.Label(root, text="Hide the text in a picture", font="Raleway")
instruction1.place(relx=0.25, rely=0.1, anchor='n')

instruction2 = tk.Label(root, text="Read the text hidden in the picture", font="Raleway")
instruction2.place(relx=0.75, rely=0.1, anchor='n')

instruction3 = tk.Label(root, text="Type in the text you want to hide", font="Raleway")
instruction3.place(relx=0.25, rely=0.65, anchor='n')

instruction4 = tk.Label(root, text="Hidden text:", font="Raleway")
instruction4.place(relx=0.75, rely=0.65, anchor='n')

instruction5 = tk.Label(root, text="What sould be the name of encrypted file (REMEMBER ABOUR PROVIDING IMAGE FORMAT)",
                        font="Raleway")
instruction5.place(relx=0.25, rely=0.75, anchor='n')

# user input

e1 = Entry(root)
e1.place(relx=0.25, rely=0.70, anchor='n')

e2 = Entry(root)
e2.place(relx=0.25, rely=0.8, anchor='n')

# buttons
button_hide_text = tk.Button(root, text="Hide text", command=lambda: encode())
button_hide_text.place(relx=0.25, rely=0.9, anchor='s')

button_read_text = tk.Button(root, text="Read text", command=lambda: decode())
button_read_text.place(relx=0.75, rely=0.9, anchor='s')

# checkbox

check_box = tk.Checkbutton(root, text="Encode message before hiding", variable=var)
check_box.deselect()
check_box.place(relx=0.38, rely=0.7, anchor='n')
# textbox
text_box = tk.Text(root, height=2, width=30, padx=15, pady=15)
text_box.place(relx=0.75, rely=0.8, anchor='s')

root.mainloop()
