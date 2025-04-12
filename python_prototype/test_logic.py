#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 22:48:23 2025

@author: nicolai
"""

import csv
import random

class FlashCardDeck:
    def __init__(self, flashcard_list_path):
        with open(flashcard_list_path, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader) # skip the header
            self._test_pairs = list(csv_reader)
        
        self._test_pairs = [pair[0].replace("\\n", "\n") for pair in self._test_pairs]
        self._test_pairs = [pair.split(";") for pair in self._test_pairs]
        self.select_active_flashcard()
        
    def select_active_flashcard(self):
        self.active_flashcard = random.choice(self._test_pairs)
    
    def check_solution(self, proposed_solution):
        if proposed_solution == self.active_flashcard[1]:
            return True
        else:
            return False
        
    def get_current_flashcard_question(self):
        return self.active_flashcard[0]

if __name__ == "__main__":        
    flashcard_deck = FlashCardDeck("../flashcard_decks/consonants_deck.csv")