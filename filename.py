import tkinter as tk

def say_hello():
    label.config(text="Hello Nyxnick 🚀")

app = tk.Tk()
app.title("My First GUI")
app.geometry("300x200")

button = tk.Button(app, text="Click Me", command=say_hello)
button.pack(pady=20)

label = tk.Label(app, text="")
label.pack()

app.mainloop()
