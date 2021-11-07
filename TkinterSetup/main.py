from tkinter import *
from PIL import ImageTk, Image
def btn_clicked():
    global entry1
    global entry0
    print('User_ID : ',entry1.get())
    print('Password: ',entry0.get())
    if entry1.get() == 'Admin' and entry0.get() == 'admin@123':
    	window.destroy()
    	import Home_page
    else:
    	canvas.itemconfig(tagOrId='error', text = 'Invaid Credentials :)')

    print("Button Clicked")

def handle_click_entry0(event):
    global entry0
    global canvas
    change = StringVar(canvas, value='')
    entry0.config(show='*',textvariable = change)

def handle_click_entry1(event):
    global entry1
    global canvas
    change = StringVar(canvas, value='')
    entry1.config(textvariable = change)


window = Tk()

window.geometry("1000x600")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

logo = ImageTk.PhotoImage((Image.open("Button/login_page/logo.png")).resize((500,500), Image.ANTIALIAS))
logo_bg = canvas.create_image(200, 300,image = logo)
line = canvas.create_line(450, 0, 450, 700)

entry0_img = PhotoImage(file = f"Button/login_page/img_textBox0.png")
entry0_bg = canvas.create_image(
    742.0, 308.5,
    image = entry0_img)

default_text_password = StringVar(canvas, value='Password')

entry0 = Entry(
    bd = 0,
    bg = "#ffffff",
    font = ('calibre',15,'normal'),
    highlightthickness = 0,
    textvariable = default_text_password,)

entry0.place(
    x = 550.0, y = 280,
    width = 382.0,
    height = 55)
entry0.bind("<1>", handle_click_entry0)



entry1_img = PhotoImage(file = f"Button/login_page/img_textBox1.png")
entry1_bg = canvas.create_image(
    741.0, 221.9,
    image = entry1_img)

default_text_user = StringVar(canvas, value='User_ID')

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    font = ('calibre',15,'normal'),
    highlightthickness = 0,
    textvariable = default_text_user)


entry1.place(
    x = 550.0, y = 195,
    width = 382.0,
    height = 55)

entry1.bind("<1>", handle_click_entry1)


img0 = PhotoImage(file = f"Button/login_page/img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 678, y = 430,
    width = 132,
    height = 44)

canvas.create_text(
    738.5, 155.0,
    text = "Hassle Free Parking",
    fill = "#000000",
    font = ("Roboto-Light", int(12.0)))

canvas.create_text(
    739.0, 80.5,
    text = " ParKing",
    fill = "#EA4C46",
    font = ("HindSiliguri-Bold", int(38.0),'bold'))

canvas.create_text(
    738.5, 563.0,
    text = "",
    fill = "#000000",
    font = ("Roboto-Thin", int(12.0)))

err_msg = canvas.create_text(
	620.5, 380,
    text = "",
    fill = "Red",
    font = ("Roboto-Thin", int(13.0)),
    tag  = 'error')

canvas.bind('<Return>', btn_clicked)

window.resizable(False, False)
window.mainloop()
