from tkinter import *
from tkinter import ttk
from tkinter import font, colorchooser, filedialog, messagebox
import os

root = Tk()  # creating tkinter window
root.geometry('600x500')  # setting window size
root.title('Notepad')  # setting window title
root.wm_iconbitmap('icon.ico')  # setting window icon

main_menu = Menu()

text_url = ''

# file menu

# file menu icons

new_icon = PhotoImage(file='assets/new_file.png')
open_icon = PhotoImage(file='assets/open.png')
save_icon = PhotoImage(file='assets/save.png')
save_as_icon = PhotoImage(file='assets/save.png')
exit_icon = PhotoImage(file='assets/exit.png')

file = Menu(main_menu, tearoff=False)

main_menu.add_cascade(label='File', menu=file)


# create new file
def new_file(event=None):
    global text_url
    text_url = None
    text_editor.delete(1.0, END)
    root.title('Untitled - Notepad')


file.add_command(label='New', image=new_icon, compound=LEFT, accelerator='Ctrl+N',
                 command=root.bind("<Control-n>", new_file))


# open a file
def open_file(event=None):
    global text_url
    text_url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select a file',
                                          filetypes=(('Text Documents (*.txt)', '*.txt'), ('All Files (*.*)', '*.*')))
    try:
        with open(text_url, 'r') as for_read:
            text_editor.delete(1.0, END)
            text_editor.insert(1.0, for_read.read())
    except FileNotFoundError:
        return
    except:
        return
    root.title(os.path.basename(text_url)+" - Notepad")


file.add_command(label='Open', image=open_icon, compound=LEFT, accelerator='Ctrl+O',
                 command=root.bind("<Control-o>", open_file))


# save a file
def save_file(event=None):
    global text_url
    try:
        if text_url:
            content = str(text_editor.get(1.0, END))
            with open(text_url, 'w', encoding='utf-8') as for_write:
                for_write.write(content)
        else:
            text_url = filedialog.asksaveasfile(mode='w', defaultextension='txt', filetypes=(
                ('Text Documents (*.txt)', '*.txt'), ('All Files (*.*)', '*.*')))
            content2 = str(text_editor.get(1.0, END))
            text_url.write(content2)
            text_url.close()
    except:
        return


file.add_command(label='Save', image=save_icon, compound=LEFT, accelerator='Ctrl+S',
                 command=root.bind("<Control-s>", save_file))


# save as new file
def save_as_file(event=None):
    global text_url
    try:
        content = str(text_editor.get(1.0, END))
        text_url = filedialog.asksaveasfile(mode='w', defaultextension='txt',
                                            filetypes=(('Text Documents (*.txt)', '*.txt'), ('All Files (*.*)', '*.*')))
        text_url.write(content)
        text_url.close()
    except:
        return


file.add_command(label='Save as', image=save_as_icon, compound=LEFT, accelerator='Ctrl+Alt+S',
                 command=root.bind("<Control-Alt-s>", save_as_file))


# exit file
def exit_file(event=None):
    global text_url, text_change
    try:
        if text_change:
            msg_box = messagebox.askyesnocancel('Warning', 'Do you want to save this file?')
            if msg_box is True:
                if text_url:
                    content = text_editor.get(1.0, END)
                    with open(text_url, 'w', encoding='utf-8') as for_write:
                        for_write.write(content)
                        root.destroy()
                else:
                    content2 = text_editor.get(1.0, END)
                    text_url = filedialog.asksaveasfile(mode='w', defaultextension='txt', filetypes=(
                        ('Text Documents (*.txt)', '*.txt'), ('All Files (*.*)', '*.*')))
                    text_url.write(content2)
                    text_url.close()
                    root.destroy()
            elif msg_box is False:
                root.destroy()
        else:
            root.destroy()
    except:
        return


file.add_command(label='Exit', image=exit_icon, compound=LEFT, command=exit_file)

# edit menu

# edit menu icons

copy_icon = PhotoImage(file='assets/copy.png')
cut_icon = PhotoImage(file='assets/cut.png')
paste_icon = PhotoImage(file='assets/paste.png')
clear_icon = PhotoImage(file='assets/clear.png')
find_icon = PhotoImage(file='assets/find.png')

edit = Menu(main_menu, tearoff=False)

main_menu.add_cascade(label='Edit', menu=edit)

# copy
edit.add_command(label='Copy', image=copy_icon, compound=LEFT, accelerator='Ctrl+C',
                 command=lambda: text_editor.event_generate("<Control c>"))
# cut
edit.add_command(label='Cut', image=cut_icon, compound=LEFT, accelerator='Ctrl+X',
                 command=lambda: text_editor.event_generate("<Control x>"))
# paste
edit.add_command(label='Paste', image=paste_icon, compound=LEFT, accelerator='Ctrl+V',
                 command=lambda: text_editor.event_generate("<Control v>"))
# clear
edit.add_command(label='Clear', image=clear_icon, compound=LEFT, accelerator='Ctrl+Alt+X',
                 command=root.bind("<Control-Alt-x>", lambda: text_editor.delete(1.0, END)))


# find & replace
def find_func(event=None):
    # find function
    def find():
        word = find_input.get()
        text_editor.tag_remove('match', '1.0', END)
        matches = 0
        if word:
            start_pos = '1.0'
            while True:
                start_pos = text_editor.search(word, start_pos, stopindex=END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                text_editor.tag_add('match', start_pos, end_pos)
                matches = matches + 1
                start_pos = end_pos
                text_editor.tag_config('match', foreground='black', background='yellow')

    # replace function
    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = text_editor.get(1.0, END)
        new_content = content.replace(word, replace_text)
        text_editor.delete(1.0, END)
        text_editor.insert(1.0, new_content)

    find_popup = Toplevel()
    find_popup.geometry('400x150')
    find_popup.title('Find/Replace')
    find_popup.resizable(0, 0)

    # creating a frame to find
    find_frame = ttk.Labelframe(find_popup, text='Find & Replace Word')
    find_frame.pack(pady=20)

    # find & replace label
    text_find = ttk.Label(find_frame, text='Find')
    text_replace = ttk.Label(find_frame, text='Replace')

    # find & replace entry field
    find_input = ttk.Entry(find_frame, width=30)
    replace_input = ttk.Entry(find_frame, width=30)

    # find & replace button
    find_button = ttk.Button(find_frame, text='Find', command=find)
    replace_button = ttk.Button(find_frame, text='Replace', command=replace)

    # find & replace label grid
    text_find.grid(row=0, column=0, padx=4, pady=4)
    text_replace.grid(row=1, column=0, padx=4, pady=4)

    # find & replace entry field grid
    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)

    # find & replace button grid
    find_button.grid(row=2, column=0, padx=4, pady=4)
    replace_button.grid(row=2, column=1, padx=4, pady=4)


edit.add_command(label='Find', image=find_icon, compound=LEFT, accelerator='Ctrl+F',
                 command=root.bind("<Control-f>", find_func))

# view menu

view = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label='View', menu=view)

# tool bar
tool_bar = Label(root)
tool_bar.pack(side=TOP, fill=X)
show_tool_bar = BooleanVar()
show_tool_bar.set(True)

# status bar
status_bar = Label(root, text='Status Bar')
status_bar.pack(side=BOTTOM)
show_status_bar = BooleanVar()
show_status_bar.set(True)


# hide tool bar
def hide_toolbar():
    global show_tool_bar
    if show_tool_bar:
        tool_bar.pack_forget()
        show_tool_bar = False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=TOP, fill=X)
        text_editor.pack(fill=BOTH, expand=True)
        status_bar.pack(side=BOTTOM)
        show_tool_bar = True


# hide status bar
def hide_status_bar():
    global show_status_bar
    if show_status_bar:
        status_bar.pack_forget()
        show_status_bar = False
    else:
        status_bar.pack(side=BOTTOM)
        show_status_bar = True


view.add_checkbutton(label='Tool Bar', onvalue=True, offvalue=0, variable=show_tool_bar, compound=LEFT,
                     command=hide_toolbar)
view.add_checkbutton(label='Status Bar', onvalue=True, offvalue=0, variable=show_status_bar, compound=LEFT,
                     command=hide_status_bar)

# color theme menu

# color theme icons

light_color_icon = PhotoImage(file='assets/light.png')
light_plus_color_icon = PhotoImage(file='assets/light_plus.png')
dark_color_icon = PhotoImage(file='assets/dark.png')

color_theme = Menu(main_menu, tearoff=False)

main_menu.add_cascade(label='Color Theme', menu=color_theme)

# color theme set
theme_choose = StringVar()

colors = (light_color_icon, light_plus_color_icon, dark_color_icon)
color_dict = {
    'Light (Default)': ('#000000', '#ffffff'),
    'Light Plus': ('#474747', '#e0e0e0'),
    'Dark': ('#c4c4c4', '#2d2d2d')
}


# color theme function


def change_color_theme():
    get_theme = theme_choose.get()
    color_tuple = color_dict.get(get_theme)
    fg_color, bg_color = color_tuple[0], color_tuple[1]
    text_editor.config(background=bg_color, fg=fg_color)


count = 0
for i in color_dict:
    color_theme.add_radiobutton(label=i, image=colors[count], variable=theme_choose, compound=LEFT,
                                command=change_color_theme)
    count = count + 1

# font box
font_tuple = font.families()
font_family = StringVar()
font_box = ttk.Combobox(tool_bar, width=20, textvariable=font_family, state='readonly')
font_box["values"] = font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0, column=0, padx=5, pady=5)

# font size box
font_size_variable = IntVar()
font_size = ttk.Combobox(tool_bar, width=15, textvariable=font_size_variable, state='readonly')
font_size.grid(row=0, column=1, padx=5)
font_size["values"] = tuple(range(8, 100, 2))
font_size.current(2)

# bold button
bold_icon = PhotoImage(file='assets/bold.png')
bold_btn = ttk.Button(tool_bar, image=bold_icon)
bold_btn.grid(row=0, column=2, padx=5)

# italic button
italic_icon = PhotoImage(file='assets/italic.png')
italic_btn = ttk.Button(tool_bar, image=italic_icon)
italic_btn.grid(row=0, column=3, padx=5)

# underline button
underline_icon = PhotoImage(file='assets/underline.png')
underline_btn = ttk.Button(tool_bar, image=underline_icon)
underline_btn.grid(row=0, column=4, padx=5)

# font color button
font_color_icon = PhotoImage(file='assets/font_color.png')
font_color_btn = ttk.Button(tool_bar, image=font_color_icon)
font_color_btn.grid(row=0, column=5, padx=5)

# align left button
a_left_icon = PhotoImage(file='assets/left.png')
a_left_btn = ttk.Button(tool_bar, image=a_left_icon)
a_left_btn.grid(row=0, column=6, padx=5)

# align center button
a_center_icon = PhotoImage(file='assets/center.png')
a_center_btn = ttk.Button(tool_bar, image=a_center_icon)
a_center_btn.grid(row=0, column=7, padx=5)

# align right button
a_right_icon = PhotoImage(file='assets/right.png')
a_right_btn = ttk.Button(tool_bar, image=a_right_icon)
a_right_btn.grid(row=0, column=8, padx=5)

# text editor

text_editor = Text(root)
text_editor.config(wrap='word', relief=FLAT)

scroll_bar = Scrollbar(root)
text_editor.focus_set()
scroll_bar.pack(side=RIGHT, fill=Y)
text_editor.pack(fill=BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

text_change = False


# counting words
def word_count(event=None):
    global text_change
    if text_editor.edit_modified():
        text_change = True
        word = len(text_editor.get(1.0, 'end-1c').split())
        char = len(text_editor.get(1.0, 'end-1c').replace(' ', ''))
        status_bar.config(text=f'Character : {char} \t\t\t\t\t\t\t\t Word : {word}')
    text_editor.edit_modified(False)


text_editor.bind('<<Modified>>', word_count)

# font family & function
font_now = 'Arial'
font_size_now = 12

text_editor.configure(font=(font_now, font_size_now))


def change_font(event=None):
    global font_now
    font_now = font_family.get()
    text_editor.configure(font=(font_now, font_size_now))


def change_font_size(event=None):
    global font_size_now
    font_size_now = font_size_variable.get()
    text_editor.configure(font=(font_now, font_size_now))


font_box.bind('<<ComboboxSelected>>', change_font)
font_size.bind('<<ComboboxSelected>>', change_font_size)


# bold function
def bold_func():
    text_get = font.Font(font=text_editor['font'])
    if text_get.actual()['weight'] == 'normal':
        text_editor.configure(font=(font_now, font_size_now, 'bold'))
    if text_get.actual()['weight'] == 'bold':
        text_editor.configure(font=(font_now, font_size_now, 'normal'))


bold_btn.configure(command=bold_func)


# italic function
def italic_func():
    text_get = font.Font(font=text_editor['font'])
    if text_get.actual()['slant'] == 'roman':
        text_editor.configure(font=(font_now, font_size_now, 'italic'))
    if text_get.actual()['slant'] == 'italic':
        text_editor.configure(font=(font_now, font_size_now, 'roman'))


italic_btn.configure(command=italic_func)


# underline function
def underline_func():
    text_get = font.Font(font=text_editor['font'])
    if text_get.actual()['underline'] == 0:
        text_editor.configure(font=(font_now, font_size_now, 'underline'))
    if text_get.actual()['underline'] == 1:
        text_editor.configure(font=(font_now, font_size_now, 'normal'))


underline_btn.configure(command=underline_func)


# font color function
def font_color():
    color_var = colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])


font_color_btn.configure(command=font_color)


# left align function
def align_left():
    text_get_all = text_editor.get(1.0, 'end')
    text_editor.tag_config('left', justify=LEFT)
    text_editor.delete(1.0, END)
    text_editor.insert(INSERT, text_get_all, 'left')


a_left_btn.configure(command=align_left)


# center align function
def align_center():
    text_get_all = text_editor.get(1.0, 'end')
    text_editor.tag_config('center', justify=CENTER)
    text_editor.delete(1.0, END)
    text_editor.insert(INSERT, text_get_all, 'center')


a_center_btn.configure(command=align_center)


# right align function
def align_right():
    text_get_all = text_editor.get(1.0, 'end')
    text_editor.tag_config('right', justify=RIGHT)
    text_editor.delete(1.0, END)
    text_editor.insert(INSERT, text_get_all, 'right')


a_right_btn.configure(command=align_right)

root.config(menu=main_menu)

root.mainloop()
