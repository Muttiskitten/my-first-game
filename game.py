import os
import tkinter as tk
from tkinter import PhotoImage
import random
import sys
from PIL import Image, ImageTk

root = tk.Tk()
root.title("High Low Card Game!")
root.geometry("400x300")

name_var = tk.StringVar()
player_score = tk.IntVar(value=0)
winning_score = 5

card_images = {}

card_values = {"A":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13}
cards = list(card_values.keys())
suit_values = {"\u2660":4, "\u2665":3, "\u2666":2, "\u2663":1}
suits = list(suit_values.keys())

def resource_path(relative_path):
     try:
          base_path = sys._MEIPASS
     except Exception:
          base_path = os.path.abspath(".")
     return os.path.join(base_path, relative_path)

suit_letters = {'♠': 'S', '♥': 'H', '♦': 'D', '♣': 'C'}
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

for suit_symbol, suit_letter in suit_letters.items():
     for rank in ranks:
         filename = f"{rank}{suit_letter}.png"
         path = resource_path(os.path.join ("cards", filename))
         image_key = f"{rank}{suit_symbol}"
         try:
             img = Image.open(path)
             img = img.resize((60, 90), Image.ANTIALIAS)
             card_images[image_key] = ImageTk.PhotoImage(img)
         except Exception as e:
              print(f"Failed to load {filename}: {e}")
              card_images[image_key] = None
         
first_card = None
first_suit = None
reset_button = None


welcome_label = tk.Label(root, text="🎴 Welcome to the High Low Game!", font=("Helvetica", 14))
name_label = tk.Label(root, text="Name?")
name_entry = tk.Entry(root, textvariable=name_var)

start_button = tk.Button(root, text="Start Game")

reset_button = tk.Button(root, text="Play Again", command=lambda: reset_game())
reset_button.pack_forget()

card_label = tk.Label(root)
card_label.pack(pady=10)

question_label = tk.Label(root, text="Will the Next card be Higher or Lower?")
question_label.pack()

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

higher_button = tk.Button(root, text="Higher", command=lambda: make_guess("higher"))
lower_button = tk.Button(root, text="Lower", command=lambda: make_guess("lower"))

score_label = tk.Label(root, text="", font=("Helvetica", 12))

def draw_card():
    card = random.choice(cards)
    suit = random.choice(suits)
    return card, suit

def start_game():
     if not name_var.get().strip():
          result_label.config(text="Please enter your cat's namr to play!")
          return
     welcome_label.pack_forget()
     name_label.pack_forget()
     name_entry.pack_forget()
     start_button.pack_forget()
     card_label.pack(pady=10)
     question_label.pack()
     higher_button.pack(side="left", padx=30)
     lower_button.pack(side="right", padx=30)
     score_label.pack(pady=20)

     global first_card, first_suit
     first_card, first_suit = draw_card()
    
     card_key = f"{first_card}{first_suit}"
     card_image = card_images.get(card_key)
     if card_image:
        card_label.config(image=card_image)
        card_label.image = card_image
     else:
        card_label.config(text=card_key)
        
     score_label.config(text=f"{name_var.get()}: {player_score.get()}")

def make_guess(choice):
    global first_card, first_suit

    second_card, second_suit = draw_card()
    card_key = f"{second_card}{second_suit}"
    card_image = card_images.get(card_key)

    if card_image:
        card_label.config(image=None, text="Drawing...")
        root.after(500, lambda: update_card_image(card_image))
    else:
        card_label.config(text=card_key)

    first_value = card_values[first_card]
    second_value = card_values[second_card]
    first_suit_value = suit_values[first_suit]
    second_suit_value = suit_values[second_suit]

    result = ""

    if (card_values[first_card] > card_values[second_card] and choice == "lower") or \
           (card_values[first_card] < card_values[second_card] and choice == "higher") or \
           (suit_values[first_suit] > suit_values[second_suit] and choice == "lower") or \
           (suit_values[first_suit] < suit_values[second_suit] and choice == "higher") or \
           (card_values[first_card] == card_values[second_card] and suit_values[first_suit] > suit_values[second_suit] and choice == "lower") or \
           (card_values[first_card] == card_values[second_card] and suit_values[first_suit] < suit_values[second_suit] and choice == "higher") or \
           (card_values[first_card] > card_values[second_card] and suit_values[first_suit] == suit_values[second_suit] and choice == "lower") or \
           (card_values[first_card] < card_values[second_card] and suit_values[first_suit] == suit_values[second_suit] and choice == "higher"):
           result = f"{name_var.get()} got a point."
           player_score.set(player_score.get() + 1)
                
    elif (card_values[first_card] == card_values[second_card] and suit_values[first_suit] == suit_values[second_suit] and choice == "higher") or \
           (card_values[first_card] == card_values[second_card] and suit_values[first_suit] == suit_values[second_suit] and choice == "lower"):
           result = "A tie mean no points."

    else:
         result = f"{name_var.get()} loses a point."
         player_score.set(player_score.get() - 1)

    result_label.config(text=result)
    score_label.config(
        text=f"{name_var.get()} Score: {player_score.get()}"
    )

    check_winner()

    first_card = second_card
    first_suit = second_suit

def check_winner():
    if player_score.get() >= winning_score:
        result_label.config(text=f"{name_var.get()} Wins! 🎉")
        disable_game_buttons()
    elif player_score.get() == -10:
        result_label.config(text=f"{name_var.get()} Loses! 🤖")
        disable_game_buttons()

def reset_game():
    global first_card, first_suit
    player_score.set(0)
    first_card, first_suit = draw_card()
    card_key = f"{first_card}{first_suit}"
    card_image = card_images[card_key]
    card_label.config(image=card_image)
    card_label.image = card_image
    score_label.config(text=f"{name_var.get()} score: 0")
    result_label.config(text="")
    higher_button.config(state=tk.NORMAL)
    lower_button.config(state=tk.NORMAL)
    reset_button.pack_forget()

def disable_game_buttons():
    higher_button.config(state=tk.DISABLED)
    lower_button.config(state=tk.DISABLED)
    reset_button.pack(pady=10)

start_button.config(command=start_game)

welcome_label.pack(pady=10)
name_label.pack()
name_entry.pack()
start_button.pack(pady=20)

root.mainloop()
