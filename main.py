import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


BACKGROUND_COLOR = '#2B3A55'
IMG_PATH = None
LOGO_PATH = None
LOGO_SCALE = 1
LOGO_COORD = None
LOGO_SIZE = None
FILE_SAVE = False
SAVE_DIR = None


# =============== Funcs =============#
def update_img(img):
    label = tk.Label(image=img)
    label.image = img
    canvas.itemconfig(img_bg, image=img)


def load_img():
    global IMG_PATH
    img_open = tk.filedialog.askopenfile(mode='r')
    path = img_open.name
    IMG_PATH = path
    image = ImageTk.PhotoImage(Image.open(IMG_PATH))
    update_img(image)
    

def load_logo():
    global LOGO_PATH, LOGO_COORD, LOGO_SIZE
    logo_open = tk.filedialog.askopenfile(mode='r')
    path = logo_open.name
    LOGO_PATH = path
    logo = Image.open(LOGO_PATH)
    img = Image.open(IMG_PATH)
    LOGO_SIZE = logo.size
    logo_xcor = img.size[0] - logo.size[0]
    logo_ycor = img.size[1] - logo.size[1]
    LOGO_COORD = (logo_xcor - 20 , logo_ycor - 20)
    reload()


def reload():
    global LOGO_SIZE, FILE_SAVE, SAVE_DIR
    img = Image.open(IMG_PATH)
    logo = Image.open(LOGO_PATH)
    logo = logo.resize(size=(LOGO_SIZE[0], LOGO_SIZE[1]))
    img.paste(logo, LOGO_COORD, mask=logo)

    if FILE_SAVE:
        img.save(SAVE_DIR)
        FILE_SAVE = False
        SAVE_DIR = None
    else:
        image = ImageTk.PhotoImage(image=img)
        return update_img(image)


def move_left():
    global LOGO_COORD
    xcor = LOGO_COORD[0] - 10

    LOGO_COORD = (xcor, LOGO_COORD[1])
    reload()


def move_right():
    global LOGO_COORD
    xcor = LOGO_COORD[0] + 10

    LOGO_COORD = (xcor, LOGO_COORD[1])
    reload()


def move_up():
    global LOGO_COORD
    ycor = LOGO_COORD[1] - 10

    LOGO_COORD = (LOGO_COORD[0], ycor)
    reload()


def move_down():
    global LOGO_COORD
    ycor = LOGO_COORD[1] + 10

    LOGO_COORD = (LOGO_COORD[0], ycor)
    reload()


def scale_logo():
    global LOGO_SIZE
    w_factor = int((LOGO_SIZE[0] / 10) + LOGO_SIZE[0])
    H_factor = int((LOGO_SIZE[1] / 10) + LOGO_SIZE[1])
    LOGO_SIZE = (w_factor, H_factor)
    reload()

def descale_logo():
    global LOGO_SIZE
    w_factor = int(LOGO_SIZE[0] - (LOGO_SIZE[0] / 10))
    H_factor = int(LOGO_SIZE[1] - (LOGO_SIZE[1] / 10))
    LOGO_SIZE = (w_factor, H_factor)
    reload()


def save_as():
    global FILE_SAVE, SAVE_DIR
    img_save = tk.filedialog.asksaveasfile(
        mode='w', 
        defaultextension='.png',
        filetypes=[
            ("PNG", ".png"),
            ("JPG", ".jpg")
        ]
    )
                                                       
    FILE_SAVE = True
    SAVE_DIR = img_save.name
    return reload()


def set_logo_pos(event):
    global LOGO_COORD, LOGO_SIZE
    img = Image.open(IMG_PATH)
    pos = logo_pos.get(logo_pos.curselection())
    match pos:
        case 'bottom right':
            LOGO_COORD = ((img.size[0] - LOGO_SIZE[0]), (img.size[1] - LOGO_SIZE[1]))
        case 'bottom left':
            LOGO_COORD = (0, (img.size[1] - LOGO_SIZE[1]))
        case 'top left':
            LOGO_COORD = (0, 0)
        case 'top right':
            LOGO_COORD = ((img.size[0] - LOGO_SIZE[0]), 0) 
    reload()


# =============== UI =============#
#window
window = tk.Tk()
window.title('Logo Stamp')
window.config(padx=50, pady=40, bg=BACKGROUND_COLOR)

#canvas
canvas = tk.Canvas(width=1500, height=800, bg=BACKGROUND_COLOR, highlightthickness=0)
img = ImageTk.PhotoImage(Image.open('placeholder.jpg'))
img_bg = canvas.create_image(750, 400, image=img)
canvas.grid(row=0, column=0, columnspan=200)

#buttons
picture = tk.Button(highlightthickness=0, bg='grey', text='Load Image', command=load_img)
picture.grid(row=1, column=90)

logo = tk.Button(highlightthickness=0, bg='grey', text='Load Logo', command=load_logo)
logo.grid(row=1, column=91)

left = tk.Button(highlightthickness=0, bg='yellow', text='⬅', command=move_left)
left.grid(row=1, column=96)

right = tk.Button(highlightthickness=0, bg='yellow', text='➡', command=move_right)
right.grid(row=1, column=97)

up = tk.Button(highlightthickness=0, bg='yellow', text='⬆', command=move_up)
up.grid(row=1, column=98)

down = tk.Button(highlightthickness=0, bg='yellow', text='⬇', command=move_down)
down.grid(row=1, column=99)

scale = tk.Button(highlightthickness=0, bg='green', text='➕', command=scale_logo)
scale.grid(row=1, column=104)

descale = tk.Button(highlightthickness=0, bg='green', text='➖', command=descale_logo)
descale.grid(row=1, column=105)

save = tk.Button(highlightthickness=0, bg='white', text='Save as', command=save_as)
save.grid(row=1, column=110)

logo_pos = tk.Listbox(height=4)
positions = ['bottom right', 'bottom left', 'top right', 'top left']
for item in positions:
    logo_pos.insert(positions.index(item), item)
logo_pos.bind('<<ListboxSelect>>', set_logo_pos)
logo_pos.grid(row=1, column=100, sticky=tk.S)

# ----------------
window.mainloop()
#----------------


