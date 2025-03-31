#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 14:46:52 2025

@author: nicolai
"""

from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image




if __name__ == "__main__":
    # load processor and model from huggingface
    processor = TrOCRProcessor.from_pretrained('openthaigpt/thai-trocr',)
    model = VisionEncoderDecoderModel.from_pretrained('openthaigpt/thai-trocr')
    
    # get test image
    path = './test_consonant.png'
    solution = 'ก'
    image = Image.open(path).convert("RGB")
    
    # process and generate text
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_text)
    
    # compare to solution
    if (generated_text == solution):
        print('Sucess!')
    else: 
        print("Try Again")
