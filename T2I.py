######################
#  ----------------  #
#  |Text2Image GUI|  #
#  ----------------  #
######################

from PIL import Image as ii, ImageFont as iif, ImageDraw as iid
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import os

'''
TODO:
-MIGHT NOT NEED:try catch for when file already exists - maybe while until saved with (n) suffix
-error　testing
-move copyright to help
'''

'''
わたし　は　すごい　です。
ラーフル　パイ
'''

'''
font1 = iif.truetype("SoukouMincho.ttf", fs)
font2 = iif.truetype("YasashisaGothic-TEGAKI.otf", fs)
font3 = iif.truetype("yumin.ttf", fs)
'''

# im.show()
# img_resized = im.resize((100, 20), Image.ANTIALIAS)
# img_resized.show()

IMAGE_TYPES = [
    ("PNG", ".png"),
    ("BMP", ".bmp"),
    ("GIF", ".gif"),
    ("JPEG", ".jpg"),
    ("TIFF", ".tif"),
]


def checkrow(image, row):
    pixels = image.load()
    result = True
    for i in range(image.size[0]):
        if pixels[i, row] != 255:
            result = False
    return result


def checkcol(image, col):
    pixels = image.load()
    result = True
    for i in range(image.size[1]):
        if pixels[col, i] != 255:
            result = False
    return result


def checkleft(image):
    l = 0
    while l < image.size[0]:
        if checkcol(image, l):
            l += 1
        else:
            break
    return l


def checkright(image):
    r = 0
    while r < image.size[0]:
        if checkcol(image, image.size[0] - 1 - r):
            r += 1
        else:
            break
    return r


def checktop(image):
    t = 0
    while t < image.size[1]:
        if checkrow(image, t):
            t += 1
        else:
            break
    return t


def checkbottom(image):
    b = 0
    while b < image.size[1]:
        if checkrow(image, image.size[1] - 1 - b):
            b += 1
        else:
            break
    return b


def autocrop(image):
    l = checkleft(image)
    r = checkright(image)
    t = checktop(image)
    b = checkbottom(image)
    return image.crop((l, t, image.size[0] - r, image.size[1] - b))


def autopad(image, pad):
    # image.show()
    cimage = autocrop(image)
    # cimage.show()
    pimage = ii.new('L', (cimage.size[0] + 2 * pad, cimage.size[1] + 2 * pad), 255)
    pimage.paste(cimage, (pad, pad))
    # pimage.show()
    return pimage


def initialise():
    Label(root, justify=CENTER, text="Text2Image", font=("Times", "22", "bold italic")).grid(row=1)
    global tb, fs
    tb = Text(root, wrap=WORD, font=("Times", "22"), width=50, height=10)
    tb.grid(row=2, padx=5, pady=5)

    frame = Frame(root, padding="0 0 0 0", relief="flat")
    frame.grid(row=3)
    w, h = 125, 5
    Canvas(frame, highlightthickness=0, relief="flat", width=w, height=h).grid(row=0, column=0)
    Canvas(frame, highlightthickness=0, relief="flat", width=w, height=h).grid(row=0, column=1)
    Canvas(frame, highlightthickness=0, relief="flat", width=w, height=h).grid(row=0, column=2)

    iframe1 = Frame(frame, padding="0 0 0 0", relief="flat")
    iframe1.grid(row=1, column=0)
    r = 1
    for text, it in IMAGE_TYPES:
        b = Radiobutton(iframe1, text=text, variable=v, value=it)
        b.grid(row=r, sticky=W)
        r += 1

    iframe2 = Frame(frame, padding="0 0 0 0", relief="flat")
    iframe2.grid(row=1, column=1)
    Label(iframe2, text="Font Size:").grid(row=1, column=0)
    fs = Spinbox(iframe2, width=5, from_=30, to=300)
    fs.grid(row=1, column=1)
    fs.delete(0, "end")
    fs.insert(0, 100)
    Button(iframe2, width=15, text='Font Menu', command=fontMenu).grid(row=2, columnspan=2)

    Button(frame, width=15, text="Generate", command=submit).grid(row=1, column=2)

    Button(root, width=10, text="Help", command=helpMenu).grid(row=4, padx=10, pady=10)
    Canvas(root, highlightthickness=0, relief="flat", width=10, height=5).grid(row=5)

    for child in root.winfo_children():
        child.grid_configure(padx=5, pady=5)
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    for child in iframe1.winfo_children():
        child.grid_configure(padx=5, pady=0)
    for child in iframe2.winfo_children():
        child.grid_configure(padx=5, pady=10)


def submit():
    print(fontVar.get())
    global tb
    inp = tb.get("1.0", 'end-1c').strip().replace("｜", "|")
    inps = []
    if len(inp) != 0:
        # gen(inp).save(inp + v.get())
        inps = inp.split("\n")
    # print(tb.get("1.0",'end-1c').split("、"))
    for i in inps:
        G = gen(i.replace("|", "\n"))
        if i.replace("|", " ").isalnum():
            G.save(i.replace("|", " ") + v.get())
        else:
            ii = ""
            for j in i:
                if j.isalnum():
                    ii += j
                elif j in "| ":
                    ii += " "
            G.save(ii + v.get())
        print("DONE\t\" " + i + " \"")


def helpMenu():
    helpRoot = Toplevel()
    helpRoot.title("Help")
    helpRoot.resizable(FALSE, FALSE)
    Label(helpRoot, justify=CENTER, text="Text2Image Help", font=("Times", "20", "bold italic")).grid(row=0, padx=10, pady=10)
    tHelp = "Enter the text with each phrase on a new line eg:\nわたし　は　すごい　です。\nラーフル　パイ\nthe above text would generate two images\nわたし　は　すごい　です。\nand\nラーフル　パイ\nUse \"|\" for linebreaks\n\nRecommended fonts for Japanese:\n(Serif)\t\tSoukouMincho\n(Sans Serif)\tYasashisaGothic-TEGAKI\n(Handwriting)\tTAsakai_Lig"
    Label(helpRoot, justify=LEFT, text=tHelp, font=("Times", "16")).grid(row=1, padx=10, pady=10)
    Label(helpRoot, justify=RIGHT, text="\nCopyright Rahul Pai Creations 2011-2017", font=("Times", "9", "italic")).grid(row=5)


def gen(s):
    global fs
    thisfs = int(fs.get())
    if fontVar.get() == "DEFAULT" or otherFont.get() == "":
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            path = str(sys._MEIPASS + "\\font\\tasakai_lig.ttf")
            font = iif.truetype(path, thisfs)
        except Exception:
            font = iif.truetype("tasakai_lig.ttf", thisfs)
    elif fontVar.get() == "OTHER":
        font = iif.truetype(otherFont.get(), thisfs)
    else:
        font = iif.truetype(fontVar.get(), thisfs)

    lines = s.split("\n")
    width = len(max(lines, key=len))
    height = len(lines)
    if fontVar.get() != "DEFAULT":
        im = ii.new("L", (thisfs * width + 200, thisfs * height * 10 + 200), 255)
    else:
        '''
Rahul Pai|Rohit Pai
Anirudda Pai|Veena Pai
        '''
        im = ii.new("L", (thisfs * width + 20, thisfs * height + 20), 255)

    draw = iid.Draw(im)
    # text_width, text_height = draw.textsize(s)
    # print(text_width, text_height)
    draw.text((10, 10), s, 0, font=font)
    im = autopad(im, int(thisfs / 4))
    return im


def fontMenu():
    fm = Toplevel()
    fm.title("Select Font")
    fm.resizable(FALSE, FALSE)

    global canvas
    canvas = Canvas(fm, highlightthickness=0, relief="flat")
    canvas.pack(side="left", fill="both")
    fmmf = Frame(canvas, padding="0 0 0 0", relief="flat")
    canvas.create_window((0, 0), window=fmmf, anchor='nw')
    myscrollbar = Scrollbar(fm, orient="vertical", command=canvas.yview)
    myscrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=myscrollbar.set)
    fm.bind("<Configure>", myfunction)

    fonts = os.listdir("C:\\Windows\\Fonts")
    exts = ["ttf", "ttc", "otf", "cff"]
    Label(fm, justify=CENTER, text="Font Menu", font=("Times", "18", "bold italic")).pack(side="top", fill="both")#.grid(row=1, padx=10, pady=10)
    Radiobutton(fmmf, command=reset, text="TAsakai_Lig (Recommended)", variable=fontVar, value="DEFAULT").grid(row=2, sticky=W)
    Radiobutton(fmmf, command=other, text="Other", variable=fontVar, value="OTHER").grid(row=3, sticky=W)
    Label(fmmf, text="Windows Fonts:", font=("Times", "16")).grid(row=4, sticky=W)
    r = 12
    for font in fonts:
        ext = font.split(".")[-1]
        if ext in exts:
            Radiobutton(fmmf, command=reset, text=font.split(".")[0], variable=fontVar, value="C:\\Windows\\Fonts\\" + font).grid(
                row=r, sticky=W)
            r += 1
    for child in fmmf.winfo_children():
        child.grid_configure(padx=5, pady=5)


def other():
    otherFont.set(filedialog.askopenfilename(title="Select file", filetypes=(("Font files", "*.ttf"), ("Font files", "*.ttc"), ("Font files", "*.otf"),("Font files", "*.cff"))).replace("/", "\\"))
    # initialdir="/",
    print(fontVar.get(), otherFont.get())


def reset():
    otherFont.set("RESET")
    print(fontVar.get(), otherFont.get())


def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox(ALL), width=250, height=400)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


root = Tk()
root.title("T2I")
root.resizable(FALSE, FALSE)

v = StringVar()
v.set(".gif")
fontVar = StringVar()
fontVar.set("DEFAULT")
otherFont = StringVar()
otherFont.set("RESET")

initialise()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
