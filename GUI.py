import tkinter as tk

window = tk.Tk()
label = tk.Label(
    text="Assignment EH2745, Laura Laringe",
    foreground="white",  # Set the text color to white
    background="red"  # Set the background color to black
)

entry = tk.Entry(fg="yellow", bg="blue", width=50)

text_box = tk.Text()

text_box.insert(tk.END, "algorithm")

label.pack()
entry.pack()
text_box.pack()
window.mainloop()

entry = tk.Entry(fg="yellow", bg="blue", width=50)