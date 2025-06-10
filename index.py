import os
import json
from tkinter import *
from tkinter import ttk
from datetime import datetime
import hash

root = Tk()
root.title("hHash")
root.geometry("570x510")
root.configure(bg="#3c3c3c")

# Стили
style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.TLabel", background="#3c3c3c", foreground="white", font=("Arial", 16, "bold"))
style.configure("d.TLabel", background="#3c3c3c", foreground="white", font=("Arial", 12, "bold"))
style.configure("Custom.TButton", background="#424242", foreground="white", font=("Arial", 11), relief="flat")
style.configure("copy.TButton", background="#6A6A6A", foreground="white", font=("Arial", 11), relief="flat")
style.configure("Custom.TCombobox", fieldbackground="#424242", background="#424242", foreground="white", borderwidth=0, padding=0, relief="flat", selectbackground="#424242", selectforeground="white",)
style.configure("Custom.Treeview", background="#424242", foreground="white", font=("Arial", 12), fieldbackground="#424242", relief="flat", borderwidth=0, padding=0,)
style.configure("Custom.Treeview.Heading", background="#525252", foreground="white", font=("Arial", 12, "bold"), relief="flat")
style.configure("Custom.Treeview", rowheight=30)

style.map("Custom.Treeview.Heading",
    background=[('selected', "#565656")],
    foreground=[('selected', 'white')]
)

style.map("Custom.Treeview",
    background=[('selected', "#515151")],
    foreground=[('selected', 'white')]
)
style.map("Custom.TCombobox",
    fieldbackground=[('readonly', '#424242')],
    background=[('readonly', '#424242')],
    foreground=[('readonly', 'white')],
    bordercolor=[('focus', '#424242')]
)
style.map("Custom.TButton",
    background=[("active", "#6D6D6D")],
    foreground=[("active", "white")]
)
style.map("copy.TButton",
    background=[("active", "#5F5F5F")],
    foreground=[("active", "white")]
)


def add_record(new_record, file_path="history.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_record)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



def on_hash():
    input_text = text_input.get("1.0", "end")
    hash_type_value = hash_type.get()
    hashed = hash.convertTohash(input_text, hash_type_value)
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    if hashed:
        data = {
            "input": input_text,
            "hash_type": hash_type_value,
            "output": hashed,
            "timestamp": formatted_date
        }
        add_record(data)
        text_output.configure(state="normal")
        text_output.delete("1.0", "end")
        text_output.insert("1.0", hashed)
        text_output.configure(state="disabled")

def clear_input():
    text_input.delete("1.0", END)
    text_output.delete("1.0", END)

def copyTextInput():
    original_hash = text_output.get("1.0", END)
    root.clipboard_clear()
    root.clipboard_append(original_hash)

title_label = ttk.Label(root, text="hHash", style="Custom.TLabel")
title_label.place(x=15, y=10)

text_input = Text(root, width=34, height=9, bg="#424242", fg="white", insertbackground="white", wrap="word", borderwidth=0)
text_input.place(x=15, y=50)

text_output = Text(root, width=34, height=9, bg="#424242", fg="white", insertbackground="white", state="disabled", wrap="word", borderwidth=0)
text_output.place(x=305, y=50)

button = ttk.Button(root, text="❐", command=copyTextInput, style="copy.TButton", width=2)
button.place(x=512, y=136)

clear_button = ttk.Button(root, text="Очистить", style="Custom.TButton", command=clear_input)
clear_button.place(x=15, y=200, width=90, height=35)

convert_button = ttk.Button(root, text="Конвертировать", style="Custom.TButton", command=on_hash)
convert_button.place(x=125, y=200, width=135, height=35)

hash_type = ttk.Combobox(root, values=["MD5", "SHA1", "sha224", "SHA256", "sha384", "shake_128", "blake2s", "blake2b", "shake_128"], state="readonly", style="Custom.TCombobox")
hash_type.set("SHA256")
hash_type.place(x=305, y=200, width=245, height=35)

history_label = ttk.Label(root, text="История операций", style="d.TLabel")
history_label.place(x=15, y=275)

columns = ("name", "type", "hash", "copy")
tree = ttk.Treeview(root, columns=columns, show="headings", style="Custom.Treeview", padding=5)
tree.place(x=15, y=300, width=535, height=200)
 
tree.heading("name", text="Название", anchor=W)
tree.heading("type", text="Тип", anchor=W)
tree.heading("hash", text="Хеш", anchor=W)
tree.heading("copy", text="", anchor=CENTER)
 
tree.column("#1", stretch=NO, width=180)
tree.column("#2", stretch=NO, width=90)
tree.column("#3", stretch=NO, width=190)
tree.column("#4", stretch=NO, width=60, anchor="center")

history_path = os.path.join(".", "history.json")

with open(history_path, "r", encoding="utf-8") as file:
    data = json.load(file)
    
tree.tag_configure('sth', background='#424242', foreground='white',)

def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text

def on_tree_click(event):
    col = tree.identify_column(event.x)
    row = tree.identify_row(event.y)
    if col == "#4" and row:
        original_hash = row_data[row]["output"]
        root.clipboard_clear()
        root.clipboard_append(original_hash)
        print(f"Скопирован хеш: {original_hash}")


row_data = {}

for idx, item in enumerate(data):
    row_id = f"row{idx}"
    tree.insert("", "end", iid=row_id, values=(
        truncate_text(item['input'], 15),
        item['hash_type'],
        truncate_text(item['output'], 20),
        "❐"
    ))
    row_data[row_id] = item


style.configure("Vertical.TScrollbar", gripcount=0, background="#424242", darkcolor="#333333", lightcolor="#555555", troughcolor="#222222", bordercolor="#424242", arrowcolor="white")

vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")
vsb.place(x=500, y=300, height=100)

tree.configure(yscrollcommand=vsb.set)

tree.bind("<Button-1>", on_tree_click)

root.mainloop()