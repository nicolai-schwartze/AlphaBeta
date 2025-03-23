#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 21:05:28 2025

@author: nicolai
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class AlphaBeta:
    def __init__(self, root):
        self.root = root

        # set application title
        self.root.title("αβ")

        # set the size of the window
        self.root.geometry("770x500")
        
        # text box for vocabulary
        self.flashcard = tk.Label(root, height=10, width=20, wraplength=150,
                                  text="asdf\nasdfadfasdfasdfasdfasdfsadfsadfasdfsadf",
                                  font=('Courier New', 20),
                                  bd=3, relief=tk.SOLID)
        
        # text box for writing
        self.draw_here = tk.Label(root, height=2, width=10, wraplength=100,
                                  text="draw here:",
                                  font=('Courier New', 15))
        
        # create a canvas widget for drawing
        self.canvas = tk.Canvas(root, bg="white", width=300, height=300, bd=3, relief=tk.SOLID)
        self.canvas.bind("<B1-Motion>", self.draw)
        
        
        # slider for brush size
        self.brush_size = 4;
        self.slider = tk.Scale(root, from_=2, to=6, orient=tk.VERTICAL, 
                               length=300, sliderlength=50, width=30,
                               showvalue=False,
                               bd=3, relief=tk.SOLID)
        self.slider.set(self.brush_size)
        self.slider.bind("<Motion>", self.on_slide)
        
        # text box brush size
        self.brush_size_label = tk.Label(root, height=2, width=5, wraplength=5,
                                  text=str(self.brush_size),
                                  font=('Courier New', 15))
        
        # select character list
        self.selected_characters = tk.StringVar(root)
        self.selected_characters.set("select a character list")
        self.character_lists = ['numbers', 'consonants', 'vowls', 'user defined']
        self.dropdown_menu = ttk.Combobox(root, textvariable=self.selected_characters, 
                                          values=self.character_lists, state="readonly", 
                                          width=25, font=('Courier New', 11))
        self.dropdown_menu.bind("<<ComboboxSelected>>", self.show_selection)
        
        # create widgets layout
        self.dropdown_menu.grid(row=0, column=0, padx=(30,15), pady=(30,5))
        self.draw_here.grid(row=0, column=1, padx=(15,15), pady=(30,5))
        self.brush_size_label.grid(row=0, column=2, padx=(15,30), pady=(30,5))
        self.flashcard.grid(row=1, column=0, padx=(30, 15), pady=(5, 30))
        self.canvas.grid(row=1, column=1, padx=(15, 15), pady=(5, 30))
        self.slider.grid(row=1, column=2, padx=(15, 30), pady=(5, 30))
        
    
    # set brush size
    def on_slide(self, value):
        self.brush_size = self.slider.get()
        self.brush_size_label.config(text=self.brush_size)
        
    # function to draw on the canvas
    def draw(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black")
    
    # select character list
    def show_selection(self, event):
        selection = self.selected_characters.get()
        if selection == "user defined":
            file_path = filedialog.askopenfilename()
            if file_path:
                print(f"You selected the file: {file_path}")
                self.selected_characters.set(file_path)
        else:
            print(f"You selected: {selection}")
            self.selected_characters.set(selection)
            

if __name__ == "__main__":
    # create main window
    root = tk.Tk()
    
    # instanciate application object
    app = AlphaBeta(root)
    
    # run application
    root.mainloop()