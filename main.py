from tkinter import *
import tkinter,re
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
import PyPDF2
import pyttsx3
import pydoc

root = Tk()
root.title('chercher et remplacer')
# root.iconbitmap('c:/gui/codemy.ico')
root.geometry("1200x660")

# modifier le nom de ficher
global open_status_name
# noinspection PyRedeclaration
open_status_name = False

global selected
selected = False


# creation de nouveau file
def new_file():
    # suppression de text
    my_text.delete("1.0", END)
    # Update status bars
    root.title('New File - ')
    status_bar.config(text="New File        ")

    global open_status_name
    open_status_name = False


# ouvrir un ficher
def open_file():
    # delete previous text
    my_text.delete("1.0", END)

    # selectionner un ficher
    text_file = filedialog.askopenfilename(initialdir="C:/gui/", title="Open File", filetypes=(("Text Files", "*.txt"), ("Html Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

    # verification si le nom de ficher existe deje

    if text_file:
        # utiliser un autre nom
        global open_status_name
        open_status_name = text_file

    # modification de statu bar
    name = text_file
    status_bar.config(text=f'{name}        ')
    name = name.replace("C:/gui/", "")
    root.title(f'{name} - TextPad!')

    # ouvrir le ficher
    text_file = open(text_file, 'r')
    stuff = text_file.read()

    # affichage du ficher dans le text box
    my_text.insert(END, stuff)

    # fermer le ficher ouver
    text_file.close()


# sauvegarde des ficher
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/gui/", title="Save File", filetypes=( ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        # modification de statu bar
        name = text_file
        status_bar.config(text=f'Saved: {name}        ')
        name = name.replace("C:/gui/", "")
        root.title(f'{name} - Textpad!')

        # sauvegarder apres la modification
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        # fermer le ficher
        text_file.close()


def save_file():
    global open_status_name
    if open_status_name:

        # sauvegarder le ficher
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        # fermer le ficher
        text_file.close()

        # mettre a jour le text
        status_bar.config(text=f'Saved: {open_status_name}        ')
    else:
        save_as_file()


# cut text
def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            selected = my_text.selection_get()
            my_text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)


# copier le text
def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)


# passer le text
def past_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


# def copy_text(e)


# ouvrir un ficher pdf
def open_pdf():
    open_file = filedialog.askopenfilename(
        initialdir="C:/GUI/",
        title="Open pdf file",
        filetypes=(
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        )

    )
    # selectionner un ficher

    if open_file:
        # ouvrir le ficher
        pdf_file = PyPDF2.PdfFileReader(open_file)
        # definir la page a lire
        page = pdf_file.getPage(0)
        # extaire le text dans le ficher pdf
        page_stuff = page.extractText()

        # ajout de text dans le textbox
        my_text.insert(1.0, page_stuff)

#bold text
def bold_it():
    # creation d our font
    bold_font = font.Font(my_text,my_text.cget("font"))
    bold_font.config(weight="bold")

    #configure a tag
    my_text.tag_config("bold", font=bold_font)

    #definir current tags
    current_tags = my_text.tag_names("sel.first","sel.last")
    #voir si la modification a ete effectuer
    if "bold" in current_tags:
        my_text.tag_remove("bold","sel.first","sel.last")
    else:
        my_text.tag_add("bold","sel.first","sel.last")



#italics text
def italics_it():
    # creation d our font
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.config(slant="italic")

    # configure a tag
    my_text.tag_config("italic", font=italics_font)

    # definir current tags
    current_tags = my_text.tag_names("sel.first")
    # voir si la modification a ete effectuer
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")

#change select text
def text_color():

    #pick a color
    my_color = colorchooser.askcolor()[1]
    status_bar.config(text=my_color)
    # creation d our font
    color_font = font.Font(my_text, my_text.cget("font"))
    color_font.config(slant="italic")

    # configure a tag
    my_text.tag_config("colored", font=color_font,foreground=my_color)

    # definir current tags
    current_tags = my_text.tag_names("sel.first")
    # voir si la modification a ete effectuer
    if "colored" in current_tags:
        my_text.tag_remove("colored", "sel.first", "sel.last")
    else:
        my_text.tag_add("colored", "sel.first", "sel.last")

#midificaation de tous le text selectionner
def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)

#chnger de couleur de fond
def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)


#select all text
def select_all(e):
    my_text.tag_add('sel','1.0','end')

def clear():
    my_text.delete(1.0,END)

#mode jour
def night_on():
    main_color ="#000000"
    second_color="#373737"
    text_color="green"

    root.config(bg=main_color)
    status_bar.config(bg=main_color,fg=text_color)
    my_text.config(bg=second_color)
    toolbar_frame.config(bg=main_color)
    #toolbar button
    bold_button.config(bg=second_color)
    italics_button.config(bg=second_color)
    redo_button.config(bg=second_color)
    undo_button.config(bg=second_color)
    color_text_btn.config(bg=second_color)

    #file menu color
    file_menu.config(bg=main_color,fg=text_color)
    edit_menu.config(bg=main_color,fg=text_color)
    color_menu.config(bg=main_color,fg=text_color)
    option_menu.config(bg=main_color,fg=text_color)


#mode nuit
def night_off():
    main_color = "SystemButtonFace"
    second_color = "SystemButtonFace"
    text_color = "black"

    root.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_color)
    my_text.config(bg="white")
    toolbar_frame.config(bg=main_color)
    # toolbar button
    bold_button.config(bg=second_color)
    italics_button.config(bg=second_color)
    redo_button.config(bg=second_color)
    undo_button.config(bg=second_color)
    color_text_btn.config(bg=second_color)

    # file menu color
    file_menu.config(bg=main_color, fg=text_color)
    edit_menu.config(bg=main_color, fg=text_color)
    color_menu.config(bg=main_color, fg=text_color)
    option_menu.config(bg=main_color, fg=text_color)


# voixx
def talk():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[1].id)
    engine.say(my_text.get('1.0','end'))
    engine.runAndWait()
    my_text.delete('1.0',END)

def regx():
    my_text.replace('1.0','end', re.sub("\d+", '<number>',my_text.get('1.0','end')))

def email():
    pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
    user_input =my_text.get('1.0','end')
    if(re.search(pattern, user_input)):
        messagebox.showinfo("email ","valide")
    else:
        messagebox.showinfo("email", "non valide")


# creayion a toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)


# creation main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# creation our scrollbar pour le text box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT,fill=Y)

#horizontal scrollbar
hor_scroll= Scrollbar(my_frame,orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# creation de text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set,wrap="none",xscrollcommand=hor_scroll.set)
my_text.pack()

# configuration our Scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)



def openFindReplaceDialog():
    findReplace = FindReplaceDialog(my_frame, my_text, True)


class FindReplaceDialog(Toplevel):
    def __init__(self, master, textWidget, withdrawInsteadOfDestroy=False, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.transient(master)
        self.resizable(False, False)

        frame = FindReplaceFrame(self, textWidget)
        frame.pack(fill="both", padx=10, pady=10)

        x = master.winfo_rootx() + (master.winfo_width() / 2) - (self.winfo_reqwidth() / 2)
        y = master.winfo_rooty() + (master.winfo_height() / 2) - (self.winfo_reqheight() / 2)
        self.geometry(f'+{int(x)}+{int(y)}')

        if withdrawInsteadOfDestroy:  # Set this to True if you want to reuse the window.
            self.protocol("WM_DELETE_WINDOW", self.withdraw)
            # use `self.deiconify()` to show the dialog again


class FindReplaceFrame(Frame):  # You can use the frame directly instead of creating a Toplevel window
    def __init__(self, master, textWidget, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.textWidget = textWidget
        self.findStartPos = 1.0

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, pad=8)
        self.rowconfigure(1, pad=8)

        Label(self, text="Find: ").grid(row=0, column=0, sticky="nw")
        self.findEntry = Entry(self)
        self.findEntry.grid(row=0, column=1, sticky="new")
        self.findEntry.focus()

        Label(self, text="Replace: ").grid(row=1, column=0, sticky="nw")
        self.replaceEntry = Entry(self)
        self.replaceEntry.grid(row=1, column=1, sticky="new")

        buttonFrame = Frame(self)
        buttonFrame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.findNextButton = Button(buttonFrame, text="Find", command=self.findNext)
        self.findNextButton.grid(row=0, column=0, padx=(0, 5))
        self.replaceButton = Button(buttonFrame, text="Replace", command=self.replace)
        self.replaceButton.grid(row=0, column=1, padx=(0, 5))
        self.replaceAllButton = Button(buttonFrame, text="Replace All", command=self.replaceAll)
        self.replaceAllButton.grid(row=0, column=2)

        self.replaceButton = Button(buttonFrame, text="regix", command=self.regx)
        self.replaceButton.grid(row=0, column=3, padx=(0, 5))


        optionsFrame = Frame(self)
        optionsFrame.grid(row=3, column=0, sticky="nsew")
        self.matchCaseVar = BooleanVar(self, True)
        self.matchCaseCheckbutton = Checkbutton(optionsFrame, text="Match Case", variable=self.matchCaseVar)
        self.matchCaseCheckbutton.grid(row=0, column=0, sticky="nw")

    def regx(self):
        self.textWidgetmy_text.regx('1.0', 'end', re.sub("\d+", '<number>', my_text.get('1.0', 'end')))


    def findNext(self):
        """
            Finds the given search term and selects the text if found.
        """
        key = self.findEntry.get()
        pos = self.textWidget.search(key, INSERT, nocase=not self.matchCaseVar.get())
        if pos:
            endIndex = f'{pos}+{len(key)}c'
            if self.textWidget.tag_ranges(SEL):
                self.textWidget.tag_remove(SEL, SEL_FIRST, SEL_LAST)  # Allow only one selection
            self.textWidget.tag_add(SEL, pos, endIndex)
            self.textWidget.mark_set(INSERT, endIndex)
            self.textWidget.see(endIndex)

    def replace(self):
        """
            If there is a selection, checks if it matches key. If it does, this replaces the given key with the replacement string. Otherwise, call self.findNext()
        """
        key = self.findEntry.get()
        repl = self.replaceEntry.get()
        flags = 0

        selRange = self.textWidget.tag_ranges(SEL)
        if selRange:
            selection = self.textWidget.get(selRange[0], selRange[1])
            if not self.matchCaseVar.get():
                key = key.lower()
                selection = selection.lower()
            if key == selection:
                self.textWidget.delete(selRange[0], selRange[1])
                self.textWidget.insert(selRange[0], repl)
        self.findNext()

    def replaceAll(self):
        """
            Replaces all occurences of `key` with `repl`.
        """
        start = "1.0"
        key = self.findEntry.get()
        repl = self.replaceEntry.get()
        count = 0

        while True:
            pos = self.textWidget.search(key, start, "end")
            if pos:
                self.textWidget.delete(pos, f"{pos}+{len(key)}c")
                self.textWidget.insert(pos, repl)
                start = f"{pos}+{len(repl)}c"
                count += 1
            else:
                # showinfo("", f"Replaced {count} occurences.")
                break


editButton = Button(my_frame, text="Find and Replace",font=("Helvetica", 10), bg='silver', bd=2, command=openFindReplaceDialog)
editButton.pack(side=RIGHT, padx=10, pady=10)

uploadButton = Button(my_frame, text="Upload file",font=("Helvetica", 10), bg='silver',fg='black', bd=2, command=open_pdf)
uploadButton.pack(side=LEFT, padx=10, pady=10)

lireButton = Button(my_frame, text="lire en voix",font=("Helvetica", 10), bg='silver',fg='black', bd=2, command=talk)
lireButton.pack(side=LEFT, padx=10, pady=10)

regxButton = Button(my_frame, text="regex",font=("Helvetica", 10), bg='silver',fg='black', bd=2, command=regx)
regxButton.pack(side=LEFT, padx=10, pady=10)
regxButton = Button(my_frame, text="verifier email",font=("Helvetica", 10), bg='silver',fg='black', bd=2, command=email)
regxButton.pack(side=LEFT, padx=10, pady=10)




# creation de menu
my_menu = Menu(root)
root.config(menu=my_menu)

# ajout de file dans le menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="nouveau ficher ", command=new_file)
file_menu.add_command(label="ouvrir un ficher", command=open_file)
file_menu.add_command(label="ouvrir pdf", command=open_pdf)
file_menu.add_command(label="sauvegarder ", command=save_file)
file_menu.add_command(label="sauvegarder tout", command=save_as_file)
file_menu.add_command(label="sortir", command=root.quit)

# modification  dans le menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="couper", command=lambda: cut_text(False),accelerator="(Ctrl+X)")
edit_menu.add_command(label="copier", command=lambda: copy_text(False),accelerator="(Ctrl+C)")
edit_menu.add_command(label="passer", command=lambda: past_text(False),accelerator="(Ctrl+V)")
edit_menu.add_separator()
edit_menu.add_command(label="selectionner tous",command=lambda :select_all(True),accelerator="(Ctrl+a)")
edit_menu.add_command(label="effacer",command=clear,accelerator="(Ctrl+a)")

# couleur   dans le menu
color_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Couleur", menu=color_menu)
color_menu.add_command(label="couleur text selectionner", command=text_color)
color_menu.add_command(label="couleur tout selectionner", command=all_text_color)
color_menu.add_command(label="couleur de fond", command=bg_color)

#option le menu
option_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Option", menu=option_menu)
option_menu.add_command(label="Mode nuit", command=night_on)
option_menu.add_command(label="Mode jour", command=night_off)


# ajout de statu bar enbas de l'app
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, padx=15)

#Edit binding

#select binding
root.bind('Control-A', select_all)
root.bind('Control-a', select_all)


#creation des bouton

#button bold
bold_button = Button(toolbar_frame,text="Bold",command=bold_it)
bold_button.grid(row=0,column=0,sticky=W,padx=5)

#button italic
italics_button = Button(toolbar_frame,text="Italics",command=italics_it)
italics_button.grid(row=0,column=1,padx=5)

#undo/redo button
undo_button = Button(toolbar_frame,text="Undo",command=my_text.edit_undo)
undo_button.grid(row=0,column=2,padx=5)

redo_button = Button(toolbar_frame,text="Undo",command=my_text.edit_redo)
redo_button.grid(row=0,column=3,padx=5)



# create color
color_text_btn = Button(toolbar_frame,text="Text Color",command=text_color)
color_text_btn.grid(row=0,column=4,padx=5)

root.mainloop()
