import tkinter as tk
import subprocess
from datetime import datetime
from tkinter import font
import random

"""
Add switch player method
Add highlighting
more green contrast
Roll history
"""

num_players = int(input("Enter number of players: "))
mode = input("2. Normal.\n3. Random Numbers.\n4. Random Colors.\n5. Random Number and Colors.\n")
button_text = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
colors = ['red', 'yellow', 'green', 'light blue']
with open(r"qwixx.txt", "+a") as file:
    file.truncate(0)

class Player:
    def __init__(self, name, frame):
        self.name = name
        self.frame = frame
        self.history = []
        self.history_text = []
        self.buttons = []
        self.score = 0


class QwixxGame:
    def __init__(self):
        self.root = root
        self.root.title("Qwixx")
        self.root.withdraw()
        self.the_font = font.Font(family="Arial", size=16)
        self.players = []
        self.current_player_index = 0
        self.create_players()
        self.create_file()
        self.create_boards()
        self.create_dice()
        self.roll_history = []
        self.root.deiconify()
        self.end_button = tk.Button(self.root, width=2, font=self.the_font, bg="gray", text="End", 
                                    command=self.end_game)
        self.end_button.grid(row=int(num_players / 2) + 2, columnspan=12, padx=2, pady=5)

    def create_players(self):
        for i in range((num_players + 1) // 2):
            for j in range(2):
                current_player_index = i * 2 + j
                if current_player_index >= num_players:
                    break
                name = input(f"Enter name for player {current_player_index + 1}: ")
                frame = tk.Frame(self.root, borderwidth=2, relief="sunken")
                frame.grid(row=i, column=j)
                player_label = tk.Label(frame, text=name, font=self.the_font)
                player_label.grid(row=0, columnspan=12)
                self.players.append(Player(name, frame))

    def create_dice(self):
        frame = tk.Frame(self.root, borderwidth=2, relief="sunken")
        frame.grid(row=int(num_players / 2) + 1, columnspan=12)
        roll_button = tk.Button(frame, text="Roll", font=self.the_font, command=lambda f=frame: self.roll_dice(f))
        roll_button.grid(row=0, column=0)
        undo_roll = tk.Button(frame, text="Undo Roll", font=self.the_font, command=lambda f=frame: self.undo_roll(f))
        undo_roll.grid(row=0, column=7)

    def roll_dice(self, frame):
        dice_result = []
        dice_results_added = []
        dice_colors = ['red', "light blue", "green", "yellow", "white", "white"]
        the_dice_colors = ['red', 'red', 'light blue', 'light blue', 'green', 'green', 'yellow', 'yellow']
        for i in range(6):
            number = random.randint(1, 6)
            player_label = tk.Label(frame, text=str(number), bg=dice_colors[i], font=self.the_font)
            player_label.grid(row=0, column=i + 1, padx=5, pady=2)
            dice_result.append(number)
        self.roll_history.append(dice_result)
        dice_results_added.append(dice_result[5] + dice_result[4])
        dice_results_added.append(dice_result[0] + dice_result[4])
        dice_results_added.append(dice_result[0] + dice_result[5])
        dice_results_added.append(dice_result[1] + dice_result[4])
        dice_results_added.append(dice_result[1] + dice_result[5])
        dice_results_added.append(dice_result[2] + dice_result[4])
        dice_results_added.append(dice_result[2] + dice_result[5])
        dice_results_added.append(dice_result[3] + dice_result[4])
        dice_results_added.append(dice_result[3] + dice_result[5])
        for player in self.players:
            for y in range(4):
                for x in range(11):
                    player.buttons[y][x].config(highlightbackground=border_color, highlightthickness=2)
        for player in self.players:
            for y in range(4):
                for x in range(11):
                    for i in range(8):
                        if (player.buttons[y][x]["text"] == str(dice_results_added[i + 1])
                                and player.buttons[y][x]["bg"] == the_dice_colors[i]):
                            player.buttons[y][x].config(highlightbackground="black", highlightthickness=2)
                        elif player.buttons[y][x]["text"] == str(dice_results_added[0]):
                            player.buttons[y][x].config(highlightbackground="black", highlightthickness=2)

    def button_click(self, player, row, col):
        if row == 4:
            player.history.append([row, col])
            player.history_text.append(player.buttons[row][col]["text"])
            player.buttons[row][col].config(state=tk.DISABLED, text="X")
        elif col == 11:
            self.lock_click_false(player, row)
        else:
            player.history.append([row, col])
            player.history_text.append(player.buttons[row][col]["text"])
            player.buttons[row][col].config(state=tk.DISABLED, text="X")
            for i in range(col):
                player.buttons[row][i].config(state=tk.DISABLED)
            if col == 10:
                self.lock_click_true(player, row)
        # Optionally switch player here if needed
        # self.switch_player()

    @staticmethod
    def undo_click(player):
        if player.history:
            row, col = player.history[-1]
            player.buttons[row][col].config(state=tk.NORMAL, text=player.history_text[-1])
            player.history.pop()
            player.history_text.pop()
            if col + 1 == 11:
                player.buttons[row][11].config(state=tk.NORMAL, text="Lock")
            elif col == 11:
                player.buttons[row][11].config(state=tk.NORMAL, text="Lock")
            for i in range(col + 1):
                if player.buttons[row][col - i]["text"] == "X":
                    break
                elif player.buttons[row][col - i]["text"] != "X":
                    player.buttons[row][col - i].config(state=tk.NORMAL)

    def undo_roll(self, frame):
        dice_colors = ['red', "light blue", "green", "yellow", "white", "white"]
        for i in range(6):
            player_label = tk.Label(frame, text=str(self.roll_history[-2][i]), bg=dice_colors[i], font=self.the_font)
            player_label.grid(row=0, column=i + 1, padx=5, pady=2)
        self.roll_history.pop()

    @staticmethod
    def lock_click_true(player, row):
        for i in range(11):
            player.buttons[row][i].config(state=tk.DISABLED)
        player.buttons[row][11].config(state=tk.DISABLED, text="X")

    @staticmethod
    def lock_click_false(player, row):
        player.history.append([row, 11])
        player.history_text.append(player.buttons[row][11]["text"])
        for i in range(12):
            player.buttons[row][i].config(state=tk.DISABLED)

    @staticmethod
    def get_score(xs):
        return xs * (xs + 1) // 2 if 0 <= xs <= 12 else 0

    def end_game(self):
        for player in self.players:
            score = 0
            final_score = 0
            for i in range(4):
                for j in range(12):
                    if player.buttons[i][j]["text"] == "X":
                        score += 1
                final_score += self.get_score(score)
                score = 0
            for i in range(4):
                if player.buttons[4][i]["text"] == "X":
                    score += 1
            final_score -= (5 * score)
            player.score = final_score
        self.display_scores()

    def display_scores(self):
        scores = [f"{player.name}: {player.score}" for player in self.players]
        self.end_button.grid_forget()
        final_score_label = tk.Label(self.root, font=self.the_font, text="\t".join(scores))
        final_score_label.grid(row=int(num_players / 2) + 2, columnspan=12, padx=2, pady=5)
        final_score_label.update()
        subprocess.run(["gnome-screenshot", "-w", f"--file={datetime.now().strftime('%m-%d-%Y_%H:%M:%S')}.png"])

    def create_boards(self):
        global button_text, colors
        the_font = font.Font(family="Arial", size=16)
        with open(r"qwixx.txt", "r") as file1:
            lines = file1.readlines()

        if mode == "3":
            for player in self.players:
                player.buttons = []
                for i in range(4):
                    button_text = eval(lines[i])
                    button_text.append("Lock")
                    button_row = []
                    for j in range(12):
                        the_text = button_text[j]
                        button = tk.Button(player.frame, width=2, bg=colors[i], font=the_font, text=the_text,
                                           highlightbackground=border_color, highlightthickness=2,
                                           command=lambda p=player, row=i, col=j: self.button_click(p, row, col))
                        button.grid(row=i + 1, column=j, padx=2, pady=2)
                        button_row.append(button)
                    player.buttons.append(button_row)
                button_row = []
                for i in range(4):
                    penalty = tk.Button(player.frame, width=2, bg="gray", font=self.the_font,
                                        command=lambda p=player, col=i: self.button_click(p, 4, col))
                    penalty.grid(row=5, column=i, padx=2, pady=2)
                    button_row.append(penalty)
                player.buttons.append(button_row)
                undo_button = tk.Button(player.frame, width=2, font=self.the_font, bg="gray", text="Undo",
                                        command=lambda p=player: self.undo_click(p))
                undo_button.grid(row=5, column=11, padx=2, pady=2)

        elif mode == "4":
            for player in self.players:
                player.buttons = [[], [], [], []]
                for i in range(11):
                    color = eval(lines[i])
                    for j in range(4):
                        the_text = button_text[i]
                        if j == 0 or j == 1:
                            button = tk.Button(player.frame, width=2, bg=color[j], font=the_font, text=the_text,
                                               highlightbackground=border_color, highlightthickness=2,
                                               command=lambda p=player, row=j, col=i: self.button_click(p, row, col))
                            button.grid(row=j + 1, column=i, padx=2, pady=2)
                            player.buttons[j].append(button)
                        elif j == 2 or j == 3:
                            button = tk.Button(player.frame, width=2, bg=color[j], font=the_font, text=the_text,
                                               highlightbackground=border_color, highlightthickness=2,
                                               command=lambda p=player, row=j, col=10 - i: self.button_click(p, row,
                                                                                                             col))
                            button.grid(row=j + 1, column=10 - i, padx=2, pady=2)
                            player.buttons[j].append(button)
                player.buttons = [player.buttons[0], player.buttons[1], player.buttons[2][::-1],
                                  player.buttons[3][::-1]]
                for i in range(4):
                    button = tk.Button(player.frame, width=2, bg="gray", font=the_font, text="Lock",
                                       command=lambda p=player, row=i, col=11: self.button_click(p, row, col))
                    button.grid(row=i + 1, column=11, padx=2, pady=2)
                    player.buttons[i].append(button)
                button_row = []
                for i in range(4):
                    penalty = tk.Button(player.frame, width=2, bg="gray", font=self.the_font,
                                        command=lambda p=player, col=i: self.button_click(p, 4, col))
                    penalty.grid(row=5, column=i, padx=2, pady=2)
                    button_row.append(penalty)
                player.buttons.append(button_row)
                undo_button = tk.Button(player.frame, width=2, font=self.the_font, bg="gray", text="Undo",
                                        command=lambda p=player: self.undo_click(p))
                undo_button.grid(row=5, column=11, padx=2, pady=2)

        elif mode == "5":
            for player in self.players:
                player.buttons = []
                generated_list = eval(lines[0])
                for i in range(4):
                    button_row = []
                    for j in range(11):
                        button = tk.Button(player.frame, width=2, bg=generated_list[i * 11 + j][1], font=the_font,
                                           highlightbackground=border_color, highlightthickness=2,
                                           text=generated_list[i * 11 + j][0],
                                           command=lambda p=player, row=i, col=j: self.button_click(p, row, col))
                        button.grid(row=i + 1, column=j, padx=2, pady=2)
                        button_row.append(button)
                    player.buttons.append(button_row)
                for i in range(4):
                    button = tk.Button(player.frame, width=2, bg="gray", text="Lock", font=the_font,
                                       command=lambda p=player, row=i, col=11: self.button_click(p, row, col))
                    button.grid(row=i + 1, column=11, padx=2, pady=2)
                    player.buttons[i].append(button)
                button_row = []
                for i in range(4):
                    penalty = tk.Button(player.frame, width=2, bg="gray", font=self.the_font,
                                        command=lambda p=player, col=i: self.button_click(p, 4, col))
                    penalty.grid(row=5, column=i, padx=2, pady=2)
                    button_row.append(penalty)
                player.buttons.append(button_row)
                undo_button = tk.Button(player.frame, width=2, font=self.the_font, bg="gray", text="Undo",
                                        command=lambda p=player: self.undo_click(p))
                undo_button.grid(row=5, column=11, padx=2, pady=2)
        else:
            for player in self.players:
                player.buttons = []
                for i in range(4):
                    button_row = []
                    for j in range(11):
                        the_text = button_text[j]
                        button = tk.Button(player.frame, width=2, bg=colors[i], font=the_font, text=the_text,
                                           highlightbackground=border_color, highlightthickness=2,
                                           command=lambda p=player, row=i, col=j: self.button_click(p, row, col))
                        button.grid(row=i + 1, column=j, padx=2, pady=2)
                        button_row.append(button)
                    player.buttons.append(button_row)
                for i in range(4):
                    button = tk.Button(player.frame, width=2, bg=colors[i], font=the_font, text="Lock",
                                       command=lambda p=player, row=i: self.lock_click_false(p, row))
                    button.grid(row=i + 1, column=11, padx=2, pady=2)
                    player.buttons[i].append(button)
                button_row = []
                for i in range(4):
                    penalty = tk.Button(player.frame, width=2, bg="gray", font=self.the_font,
                                        command=lambda p=player, col=i: self.button_click(p, 4, col))
                    penalty.grid(row=5, column=i, padx=2, pady=2)
                    button_row.append(penalty)
                player.buttons.append(button_row)
                undo_button = tk.Button(player.frame, width=2, font=self.the_font, bg="gray", text="Undo",
                                        command=lambda p=player: self.undo_click(p))
                undo_button.grid(row=5, column=11, padx=2, pady=2)

    @staticmethod
    def create_file():
        if mode == "4":
            for i in range(11):
                random.shuffle(colors)
                with open(r"qwixx.txt", "+a") as file2:
                    file2.write(str(colors) + "\n")
        elif mode == "5":
            generated_list = []
            for i in button_text:
                for j in colors:
                    generated_list.append([i, j])
            generated_list = sorted(generated_list, key=lambda x: random.random())
            with open(r"qwixx.txt", "+a") as file3:
                file3.write(str(generated_list) + "\n")
        elif mode == "3":
            for i in range(4):
                random.shuffle(button_text)
                with open(r"qwixx.txt", "+a") as file4:
                    file4.write(str(button_text) + "\n")

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        print(f"It's now {self.players[self.current_player_index].name}'s turn.")


if __name__ == "__main__":
    root = tk.Tk()
    border_color = root.cget("highlightbackground")
    game = QwixxGame()
    root.mainloop()
