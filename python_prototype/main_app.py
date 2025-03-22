#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 21:05:28 2025

@author: nicolai
"""

import tkinter as tk

# create the main window
root = tk.Tk()
root.title("Drawing App")

# set the size of the window
root.geometry("400x400")

# create a canvas widget
canvas = tk.Canvas(root, bg="white", width=300, height=300)
canvas.pack(pady=20)

# function to draw on the canvas
def draw(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black")

# bind the draw function to mouse movement
canvas.bind("<B1-Motion>", draw)

# run the application
root.mainloop()