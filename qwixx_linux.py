import tkinter as tk
import random
import subprocess
from datetime import datetime

board_type = 0
history = []
history_text = []
buttons = []
button_row = []
colors = ["red", "yellow", "green", "light blue"]
button_text = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

mode = input("1. Specific.\n2. Normal.\n3. Random Numbers.\n4. Random Colors.\n5. Random Number and Colors.\n")
if mode != "1":
    save = input("Press 1 if you would like to save the board.\n")
    if save == "1":
        with open(r"/home/Ryker/Desktop/Python_projects/Qwixx/qwixx.txt", "+a") as file:
            file.truncate(0)
elif mode == "1":
    board_type = input("1. Random Numbers.\n2. Random Colors.\n3.Random Numbers and Colors.\n")

root = tk.Tk()
root.title("Qwixx")

def button_click(row, col):
    if row == 4:
        history.append([row, col])
        history_text.append(buttons[row][col]["text"])
        buttons[row][col].config(state=tk.DISABLED, text="X")
    elif col == 11:
        lock_click_false(row)
    else:
        history.append([row, col])
        history_text.append(buttons[row][col]["text"])
        buttons[row][col].config(state=tk.DISABLED, text="X")
        for i in range(col):
            buttons[row][i].config(state=tk.DISABLED)
        if col == 10:
            lock_click_true(row)

def undo_click():
    row, col = history[-1]
    buttons[row][col].config(state=tk.NORMAL, text=history_text[-1])
    history.remove(history[-1])
    history_text.remove(history_text[-1])
    if col + 1 == 11:
        buttons[row][11].config(state=tk.NORMAL, text="Lock")
    elif col == 11:
        buttons[row][11].config(state=tk.NORMAL, text="Lock")
    for i in range(col+1):
        if buttons[row][col-i]["text"] == "X":
            break
        elif buttons[row][col-i]["text"] != "X":
            buttons[row][col-i].config(state=tk.NORMAL)

def lock_click_true(row):
    for i in range(11):
        buttons[row][i].config(state=tk.DISABLED)
    buttons[row][i+1].config(state=tk.DISABLED, text="X")

def lock_click_false(row):
    history.append([row, 11])
    history_text.append(buttons[row][11]["text"])
    for i in range(12):
        buttons[row][i].config(state=tk.DISABLED)

def get_score(xs):
    return xs * (xs + 1) // 2 if 0 <= xs <= 12 else 0

def end_game():
    score = 0
    final_score = 0
    for i in range(4):
        for j in range(12):
            if buttons[i][j]["text"] == "X":
                score += 1
        final_score += get_score(score)
        score = 0
    for i in range(4):
        if buttons[4][i]["text"] == "X":
            score += 1
    final_score -= (5 * score)
    final_score_label.config(text=f"Final score: {final_score}")
    final_score_label.update()
    subprocess.run(["gnome-screenshot", "-w", f"--file=/home/Ryker/Desktop/Python_projects/Qwixx/{datetime.now().strftime('%m-%d-%Y_%H:%M:%S')}.png"])

def create_board():
    global button_text, buttons
    if mode == "1":
        with open(r"/home/Ryker/Desktop/Python_projects/Qwixx/qwixx.txt", "r") as file:
            lines = file.readlines()
        if board_type == "1":
            for i in range(4):
                button_text = eval(lines[i])
                button_text.append("Lock")
                button_row = []
                for j in range(12):
                    the_text = button_text[j]
                    button = tk.Button(root, width=2, bg=colors[i], text=the_text, command=lambda row=i, col=j: button_click(row, col))
                    button.grid(row=i, column=j, padx=2, pady=2)
                    button_row.append(button)
                buttons.append(button_row)
        elif board_type == "2":
            buttons = [[], [], [], []]
            for i in range(12):
                color = eval(lines[i])
                for j in range(4):
                    button_text.append("Lock")
                    the_text = button_text[i]
                    button = tk.Button(root, width=2, bg=color[j], text=the_text, command=lambda row=j, col=i: button_click(row, col))
                    button.grid(row=j, column=i, padx=2, pady=2)
                    buttons[j].append(button)
        elif board_type == "3":
            for i in range(4):
                button_text = eval(lines[i])
                button_text.append("Lock")
                button_row = []
                for j in range(12):
                    the_text = button_text[j]
                    button = tk.Button(root, width=2, text=the_text, command=lambda row=i, col=j: button_click(row, col))
                    button.grid(row=i, column=j, padx=2, pady=2)
                    button_row.append(button)
                buttons.append(button_row)
            for i in range(12):
                color = eval(lines[i+4])
                for j in range(4):
                    buttons[j][i].config(bg=color[j])
                    
    elif mode == "4":
        buttons = [[], [], [], []]
        button_text.append("Lock")
        for i in range(12):
            random.shuffle(colors)
            if save == "1":
                with open(r"/home/Ryker/Desktop/Python_projects/Qwixx/qwixx.txt", "+a") as file:
                    file.write(str(colors) + "\n")
            for j in range(4):
                the_text = button_text[i]
                button = tk.Button(root, width=2, bg=colors[j], text=the_text, command=lambda row=j, col=i: button_click(row, col))
                button.grid(row=j, column=i, padx=2, pady=2)
                buttons[j].append(button)
    elif mode == "5":
        numbers = []
        for i in range(4):
            random.shuffle(button_text)
            if save == "1":
                with open(r"/home/Ryker/Desktop/Python_projects/Qwixx/qwixx.txt", "+a") as file:
                    file.write(str(button_text) + "\n")
            for j in button_text:
                numbers.append(j)
            numbers.append("Lock")
        color = [[], [], [], []]
        for i in range(12):
            random.shuffle(colors)
            if save == "1":
                with open(r"/home/Ryker/Desktop/Python_projects/Qwixx/qwixx.txt", "+a") as file:
                    file.write(str(colors) + "\n")
            for j in range(4):
                color[j].append(colors[j])
        color1 = []
        for i in range(4):
            for j in color[i]:
                color1.append(j)
        for i in range(4):
            button_row = []
            for j in range(12):
                the_text = numbers[i*12+j]
                button = tk.Button(root, width=2, bg=color1[i*12+j], text=the_text, command=lambda row=i, col=j: button_click(row, col))
                button.grid(row=i, column=j, padx=2, pady=2)
                button_row.append(button)
            buttons.append(button_row)
    else:
        for i in range(4):
            if mode == "3":
                random.shuffle(button_text)
                if save == "1":
                    with open(r"/home/Ryker/Desktop/Python_projects/Qwixx/qwixx.txt", "+a") as file:
                        file.write(str(button_text) + "\n")
            button_text.append("Lock")
            button_row = []
            for j in range(12):
                the_text = button_text[j]
                button = tk.Button(root, width=2, bg=colors[i], text=the_text, command=lambda row=i, col=j: button_click(row, col))
                button.grid(row=i, column=j, padx=2, pady=2)
                button_row.append(button)
            buttons.append(button_row)
            button_text.remove("Lock")
    if board_type == "0":
        for i in range(4):
            button = tk.Button(root, width=2, bg=colors[i], text="Lock", command=lambda row=i: lock_click_false(row))
            button.grid(row=i, column=11, padx=2, pady=2)
            buttons[i].append(button)

create_board()
undo_button = tk.Button(root, width=2, bg="gray", text="Undo", command=undo_click)
undo_button.grid(row=4, column=11, padx=2, pady=2)
end_button = tk.Button(root, width=2, bg="gray", text="End", command=end_game)
end_button.grid(row=4, column=10, padx=2, pady=2)
final_score_label = tk.Label(root, text="")
final_score_label.grid(row=6, columnspan=12, padx=2, pady=5)

for i in range(4):
    penalty = tk.Button(root, width=2, bg="gray", command=lambda col=i: button_click(4, col))
    penalty.grid(row=4, column=i, padx=2, pady=2)
    button_row.append(penalty)
buttons.append(button_row)

root.mainloop()
