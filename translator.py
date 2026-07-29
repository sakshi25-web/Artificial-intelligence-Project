from tkinter import *
from tkinter import ttk, messagebox, filedialog
from deep_translator import GoogleTranslator

# ---------------------- FUNCTIONS ----------------------

def translate_text():
    try:
        text = input_text.get("1.0", END).strip()

        if text == "":
            messagebox.showwarning("Warning", "Please enter text.")
            return

        source = source_lang.get()
        target = target_lang.get()

        translated = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)

        output_text.delete("1.0", END)
        output_text.insert(END, translated)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_text.get("1.0", END))
    messagebox.showinfo("Copied", "Translated text copied.")


def clear_text():
    input_text.delete("1.0", END)
    output_text.delete("1.0", END)


def save_translation():
    file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if file:
        with open(file, "w", encoding="utf-8") as f:
            f.write(output_text.get("1.0", END))

        messagebox.showinfo("Saved", "Translation saved successfully!")


# ---------------------- LANGUAGE DICTIONARY ----------------------

languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese": "zh-cn",
    "Russian": "ru",
    "Arabic": "ar",
    "Korean": "ko"
}

# ---------------------- WINDOW ----------------------

root = Tk()
root.title("AI Language Translator")
root.geometry("950x700")
root.configure(bg="#EAF4FC")
root.resizable(False, False)

# ---------------------- TITLE ----------------------

Label(
    root,
    text="🌍 AI Language Translator",
    font=("Segoe UI", 26, "bold"),
    fg="#0A3D62",
    bg="#EAF4FC"
).pack(pady=20)

# ---------------------- LANGUAGE FRAME ----------------------

frame = Frame(root, bg="#EAF4FC")
frame.pack()

Label(
    frame,
    text="Source Language",
    bg="#EAF4FC",
    font=("Segoe UI", 11, "bold")
).grid(row=0, column=0, padx=10)

source_combo = ttk.Combobox(
    frame,
    values=list(languages.keys()),
    width=20
)
source_combo.grid(row=0, column=1, padx=10)
source_combo.current(0)

Label(
    frame,
    text="Target Language",
    bg="#EAF4FC",
    font=("Segoe UI", 11, "bold")
).grid(row=0, column=2, padx=10)

target_combo = ttk.Combobox(
    frame,
    values=list(languages.keys()),
    width=20
)
target_combo.grid(row=0, column=3, padx=10)
target_combo.current(1)

source_lang = StringVar(value="en")
target_lang = StringVar(value="hi")

source_combo.configure(textvariable=source_lang)
target_combo.configure(textvariable=target_lang)


def update_source(event):
    source_lang.set(languages[source_combo.get()])


def update_target(event):
    target_lang.set(languages[target_combo.get()])


source_combo.bind("<<ComboboxSelected>>", update_source)
target_combo.bind("<<ComboboxSelected>>", update_target)

# ---------------------- INPUT ----------------------

Label(
    root,
    text="Enter Text",
    bg="#EAF4FC",
    font=("Segoe UI", 12, "bold")
).pack(pady=10)

input_text = Text(
    root,
    height=8,
    width=80,
    font=("Segoe UI", 12)
)
input_text.pack()

# ---------------------- TRANSLATE BUTTON ----------------------

Button(
    root,
    text="🚀 Translate",
    font=("Segoe UI", 13, "bold"),
    bg="#27AE60",
    fg="white",
    padx=15,
    pady=8,
    relief="flat",
    command=translate_text
).pack(pady=20)

# ---------------------- OUTPUT ----------------------

Label(
    root,
    text="Translated Text",
    bg="#EAF4FC",
    font=("Segoe UI", 12, "bold")
).pack()

output_text = Text(
    root,
    height=8,
    width=80,
    font=("Segoe UI", 12)
)
output_text.pack()

# ---------------------- BUTTON FRAME ----------------------

button_frame = Frame(root, bg="#EAF4FC")
button_frame.pack(pady=20)

Button(
    button_frame,
    text="📋 Copy",
    bg="#3498DB",
    fg="white",
    width=12,
    command=copy_text
).grid(row=0, column=0, padx=10)

Button(
    button_frame,
    text="🗑 Clear",
    bg="#E74C3C",
    fg="white",
    width=12,
    command=clear_text
).grid(row=0, column=1, padx=10)

Button(
    button_frame,
    text="💾 Save",
    bg="#2ECC71",
    fg="white",
    width=12,
    command=save_translation
).grid(row=0, column=2, padx=10)

# ---------------------- RUN ----------------------

root.mainloop()