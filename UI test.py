import tkinter as tk
from tkinter import PhotoImage

root = tk.Tk()
root.title('hexapod leg mover')
root.geometry('720x720')

canvas = tk.Canvas(root, width=720, height=720)
canvas.grid(column=0, row=0)



controlFrame = tk.Frame(root)
controlFrame.grid(row=0, column=0)

#bgImage = PhotoImage(file='backgrounds/hexapodBro200x200.png')

#canvas.create_image(0,0, image=bgImage, anchor='nw')

endButton = tk.Button(controlFrame, text='quit', command=root.destroy)
endButton.grid(column=5, row=5)

entry = tk.Entry(controlFrame)
entry.grid(column=0, row=0)
#canvas.create_window(300, 150, window=entry, width=200)

label = tk.Label(controlFrame, text='leg 1')
label.grid(column=0, row=1)


root.mainloop()