#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 21:05:28 2025

@author: nicolai
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import io
from test_logic import FlashCardDeck
from ocr_checker import ImageProcessor
import time

class AlphaBeta:
    def __init__(self, root):
        self.root = root

        # set application title
        self.root.title("αβ")

        # set the size of the window
        self.root.geometry("770x500")
        
        # text box for vocabulary
        self.flashcard = tk.Label(root, height=10, width=20, wraplength=150,
                                  text="select\nflashcard\nlist",
                                  font=('Courier New', 20),
                                  bd=3, relief=tk.SOLID, bg="white")
        
        # text box for writing
        self.draw_here = tk.Label(root, height=2, width=10, wraplength=100,
                                  text="draw here:",
                                  font=('Courier New', 15))
        
        # create a canvas widget for drawing
        self.canvas = tk.Canvas(root, bg="white", width=300, height=300, 
                                bd=3, relief=tk.SOLID)
        self.canvas.bind("<B1-Motion>", self.draw)
        
        
        # slider for brush size
        self.brush_size = 3;
        self.slider = tk.Scale(root, from_=1, to=5, orient=tk.VERTICAL, 
                               length=300, sliderlength=50, width=30,
                               showvalue=False,
                               bd=3, relief=tk.SOLID)
        self.slider.set(self.brush_size)
        self.slider.bind("<Motion>", self.on_slide)
        
        # text box brush size
        self.brush_size_label = tk.Label(root, height=2, width=7, wraplength=70,
                                  text="brush:"+str(self.brush_size),
                                  font=('Courier New', 15))
        
        # select character list
        self.selected_characters = tk.StringVar(root)
        self.selected_characters.set("select a character list")
        self.character_lists = ['numbers', 'consonants', 'vowls', 'user defined']
        self.dropdown_menu = ttk.Combobox(root, textvariable=self.selected_characters, 
                                          values=self.character_lists, state="readonly", 
                                          width=25, font=('Courier New', 11))
        self.dropdown_menu.bind("<<ComboboxSelected>>", self.show_selection)
        
        # button area 
        self.button_frame = tk.Frame(root)
        self.clear_button = tk.Button(self.button_frame, text="clear", bg="red",
                                      width=8, height=2,
                                      font=('Courier New', 15),
                                      command=self.clear_action)
        self.submit_button = tk.Button(self.button_frame, text="submit", bg="green",
                                       width=8, height=2,
                                       font=('Courier New', 15),
                                       command=self.submit_action)
        
        # pack the buttons side by side
        self.submit_button.pack(side=tk.RIGHT, padx=(30,0))
        self.clear_button.pack(side=tk.LEFT, padx=(0,30))

        # create widgets layout
        self.dropdown_menu.grid(row=0, column=0, padx=(30,15), pady=(30,5))
        self.draw_here.grid(row=0, column=1, padx=(15,15), pady=(30,5))
        self.brush_size_label.grid(row=0, column=2, padx=(15,50), pady=(30,5))
        self.flashcard.grid(row=1, column=0, padx=(30, 15), pady=(5, 30))
        self.canvas.grid(row=1, column=1, padx=(15, 15), pady=(5, 30))
        self.slider.grid(row=1, column=2, padx=(15, 50), pady=(5, 30))
        self.button_frame.grid(row=2, column=1)
        
        # create ocr object instance for evaluation
        self.image_processor = ImageProcessor()
        
        
    # set brush size
    def on_slide(self, value):
        self.brush_size = self.slider.get()
        self.brush_size_label.config(text="brush:"+str(self.brush_size))
        
    # function to draw on the canvas
    def draw(self, event):
        x1, y1 = (event.x - self.brush_size+1), (event.y - self.brush_size+1)
        x2, y2 = (event.x + self.brush_size+1), (event.y + self.brush_size+1)
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
            self.selected_characters.set(selection)
            flashcard_deck_path = f'../flashcard_decks/{selection}_deck.csv';
            self.flashcard_deck = FlashCardDeck(flashcard_deck_path)
            self.flashcard.config(text=self.flashcard_deck.get_current_flashcard_question())
            
    def clear_action(self):
        self.canvas.delete("all")

    def submit_action(self):
        image = self.get_image_from_canvas()
        ocr_result = self.image_processor.get_ocr_result(image)
        # for logging and debugging
        print(ocr_result)
        flashcard_evaluation = self.flashcard_deck.check_solution(ocr_result)
        if flashcard_evaluation:
            self.flashcard_deck.select_active_flashcard()
            self.flashcard.config(text=self.flashcard_deck.get_current_flashcard_question())
            self.clear_action()
        else:
            self.clear_action()
            
        
    def get_image_from_canvas(self):
        # postscript representation of the canvas
        ps = self.canvas.postscript(colormode='color')
        
        # create a PIL Image from the PostScript data
        image = Image.open(io.BytesIO(ps.encode('utf-8')))
        return image    

if __name__ == "__main__":
    # create main window
    root = tk.Tk()
    
    # instanciate application object
    app = AlphaBeta(root)
    
    # run application
    app.root.mainloop()
    