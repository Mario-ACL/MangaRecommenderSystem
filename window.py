import tkinter as tk

window = tk.Tk()
window.title("MangaRecommenderSystem")

# Create a frame with padding
mainframe = tk.Frame(window, padx=250, pady=250)
mainframe.grid(column=0, row=0, sticky=(tk.N+tk.W+tk.E+tk.S))

# Configure the column and row weights to make the frame expandable
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# Add widgets to the frame with stickiness
tk.Label(mainframe, text="Hello World!").grid(column=0, row=0, sticky=(tk.W+tk.E))
tk.Button(mainframe, text="Quit", command=window.destroy).grid(column=1, row=0, sticky=(tk.W+tk.E))

window.mainloop()
