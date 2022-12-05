from math import sqrt
from tkinter import *
from tkinter import filedialog, ttk, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import font

def select_img():
    global img, filename, canvas
    # method to find the directory to the image
    filename = filedialog.askopenfilename(initialdir="/Pictures",
                                          title="Select file",
                                          filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    # Created a new frame to contain text button
    add_frame = Frame(frame)
    add_frame.grid(column=0, row=0, pady=10)
    open_img = Image.open(filename)
    # Resize the image to fit the the screen of thw window
    resize_img = open_img.resize((950, 600))
    canvas = Canvas(frame, width=950, height=600)
    img = ImageTk.PhotoImage(resize_img, Image.Resampling.LANCZOS)
    canvas.create_image(475, 300, image=img)
    canvas.grid(column=0, row=1)

    if canvas:
        text_btn = Button(add_frame, text="Add Text", command=Properties)
        text_btn.grid(column=0, row=0, padx=20)
        welcome_label.grid_remove()

def color_chooser():
    global hex_color
    chooser = colorchooser.askcolor()
    hex_color = chooser[1]
    text_color.delete(0, END)
    text_color.insert("end", hex_color)


def add_text(text, font_size, x_position, y_position):
    canvas.create_text(x_position, y_position, text=text, fill=str(hex_color), font=(font, round(font_size)))


def save_image(text, font_size, x_position, y_position):
    img = Image.open(filename)
    img_draw = ImageDraw.ImageDraw(img)
    img_width = img.width
    img_height = img.height
    scaledWidth = img_width / 950
    scaledHeight = img_height / 600
    fontSize_scaled = round(font_size * sqrt(scaledWidth**2 + scaledHeight**2))
    x_scaled = int(x_position) * scaledWidth
    y_scaled = int(y_position) * scaledHeight
    img_font = ImageFont.truetype("arial.ttf", fontSize_scaled)
    left, top, right, bottom = img_font.getbbox(text)
    text_height = bottom - top
    text_width = right - left
    x_position = x_scaled - (text_width/2)
    y_position = y_scaled - (text_height/2)
    img_draw.text((x_position, y_position), text, fill=hex_color, font=img_font)
    # To allow user to choose file path to save the watermarked image
    result = filedialog.asksaveasfilename(initialdir="/",
                                          title="Select file",
                                          filetypes=(('JPEG', ('*.jpg', '*.jpeg', '*.jpe')),
                                                     ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')),
                                                     ('GIF', '*.gif')), initialfile="watermark_img")

    img.save(result + ".JPG")

def edit_text_size(e):
    global text_sizel
    text_sizel.config(text=f"{round(float(e),1)}x")

def Properties():
    # Labelframe to put all the properties
    text_frame = LabelFrame(frame)
    text_frame.grid(column=1, row=1, padx=15)

    properties = Label(text_frame, text="Properties", font=("ariel", 12))
    properties.grid(column=0, row=0)

    # watermark text box
    tf = LabelFrame(text_frame)
    tf.grid(column=0, row=1, pady=(5, 5))
    text_label = Label(tf, text="Text", relief="flat", font=("ariel", 10))
    text_label.grid(column=0, row=0, padx=(2, 12))
    # global text_box
    text_box = Entry(tf, width=28, font=("ariel", 10), borderwidth=0)
    text_box.insert(END, "Watermark")
    text_box.grid(column=1, row=0, ipady=2)

    # watermark text color
    cf = LabelFrame(text_frame)
    cf.grid(column=0, row=2, pady=(5, 5))

    color = Button(cf, text="Color", font=("ariel", 10), command=color_chooser)
    color.grid(column=0, row=0, padx=2)

    global text_color
    text_color = Entry(cf, font=("ariel", 10), width=28, borderwidth=0)
    text_color.grid(column=1, row=0, ipady=3)

    # watermark X position
    xpf = LabelFrame(text_frame)
    xpf.grid(column=0, row=3, pady=(5, 5))

    x_position_label = Label(xpf, text="X Position", font=("Ariel", 10))
    x_position_label.grid(column=0, row=0, padx=(2, 10))

    x_p_entry = Entry(xpf, font=("ariel", 10), width=24, borderwidth=0)
    x_p_entry.grid(column=1, row=0, ipady=3)

    # Y position
    ypf = LabelFrame(text_frame)
    ypf.grid(column=0, row=4, pady=(5, 5))
    y_position_label = Label(ypf, text="Y Position",font=("Ariel", 10))
    y_position_label.grid(column=0, row=0, padx=(2, 9))
    y_p_entry = Entry(ypf, width=28, borderwidth=0 )
    y_p_entry.grid(column=1, row=0, ipady=3)

    # watermark text size
    sf = LabelFrame(text_frame)
    sf.grid(column=0, row=5, pady=(5, 5))

    size = Label(sf, text="Size", font=("ariel", 10))
    size.grid(column=0, row=0, padx=(2, 10))

    size_scale = ttk.Scale(sf, from_=0.0, to=40.0, length=170, value=20.0, command=edit_text_size)
    size_scale.grid(column=1, row=0)

    global text_sizel
    text_sizel = Label(sf, text=f"{size_scale.get()}x")
    text_sizel.grid(column=2, row=0)


    # Button frame for show text and save image button
    bf = Frame(text_frame)
    bf.grid(column=0, row=6, pady=(5, 5))
    # Show text button
    show_btn = Button(bf, text="Show Text", font=("ariel", 10), command=lambda: add_text(text_box.get(), size_scale.get(), x_p_entry.get(), y_p_entry.get()))
    show_btn.grid(column=0, row=0, padx=(5, 5))

    # Button to save the image
    save_btn = Button(bf,
                      text="Save Image",
                      font=("ariel", 10),
                      command=lambda: save_image(text_box.get(),
                                                 size_scale.get(),
                                                 x_p_entry.get(),
                                                 y_p_entry.get()))

    save_btn.grid(column=1, row=0, padx=(10, 5))


window = Tk()
window.title("Watermark App")
window.configure(width=400, height=200)


window.config(padx=30, pady=30)

frame = Frame(window)
frame.grid(column=0, row=0)

welcome_label = Label(frame, text="Watermark It!", font=("Roboto Slab", 20, "bold"))
welcome_label.grid(column=0, row=0)

label1 = Label(frame, text="Make custom watermarks to add to your photo", font=("Arial", 12))
label1.grid(column=0, row=1)

bottom_frame = Frame(frame)
bottom_frame.grid(column=0, row=2, pady=10)

button_1 = Button(bottom_frame, text="Select Image", command=select_img)
button_1.grid(column=0, row=0, padx=25)

exit_button = Button(bottom_frame, text="Exit App", command=window.quit)
exit_button.grid(column=1, row=0)

window.mainloop()
