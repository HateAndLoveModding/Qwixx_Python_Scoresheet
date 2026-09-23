# Standard Libraries
import random
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import font


class Player:
    def __init__(self, name, frame):
        self.name = name # Name of the player
        self.frame = frame # The frame that the player is in
        self.hist = [] # Stores a tuple with the first value containing the <row>_<col> key and the second value storing the original text of each button that was pressed
        self.buttons = {} # Each button has two key pointing at it. 1. <color>_<number> blue_5, 2. <row>_<column> 3_3
        self.score = 0 # The player's final score


class QwixxGame:
    def __init__(self):
        self.numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        self.colors = ['red', 'yellow', 'light green', 'light blue']
        self.highlighted = []
        self.root = root
        self.root.title("Qwixx")
        self.root.withdraw()
        self.the_font = font.Font(family="Arial", size=16)
        self.players = []
        self.current_player_index = 0
        self.roll_history = []
        self.end_button = tk.Button(self.root, width=2, font=self.the_font, bg="gray", text="End",
                                    command=self.end_game)
        self.end_button.grid(row=int(num_players / 2) + 2, columnspan=12, padx=2, pady=5)


    def create_players(self):
        for i in range((num_players + 1) // 2):
            for j in range(2):
                self.current_player_index = i * 2 + j
                if self.current_player_index >= num_players:
                    break
                name = input(f"Enter name for player {self.current_player_index + 1}: ")
                frame = tk.Frame(self.root, borderwidth=2, relief="sunken")
                frame.grid(row=i, column=j)
                player_label = tk.Label(frame, text=name, font=self.the_font)
                player_label.grid(row=0, columnspan=12)
                self.players.append(Player(name, frame))
        hi=0


    def create_dice(self):
        frame = tk.Frame(self.root, borderwidth=2, relief="sunken")
        frame.grid(row=int(num_players / 2) + 1, columnspan=12)
        roll_button = tk.Button(frame, text="Roll", font=self.the_font, command=lambda f=frame: self.roll_dice(f))
        roll_button.grid(row=0, column=0)
        undo_roll = tk.Button(frame, text="Undo Roll", font=self.the_font, command=lambda f=frame: self.undo_roll(f))
        undo_roll.grid(row=0, column=7)


    def roll_dice(self, frame):
        white_one = random.randint(1, 6)
        white_two = random.randint(1, 6)
        player_label = tk.Label(frame, text=str(white_one), bg="white", font=self.the_font)
        player_label.grid(row=0, column=5, padx=5, pady=2)
        player_label = tk.Label(frame, text=str(white_two), bg="white", font=self.the_font)
        player_label.grid(row=0, column=6, padx=5, pady=2)
        white_total = white_one + white_two
        roll = ""
        for player in self.players:
            for button in self.highlighted:
                button.config(highlightbackground=border_color, highlightthickness=2)
        self.highlighted.clear()
        for i in range(4):
            the_color = self.colors[i]
            colored_die_number = random.randint(1, 6)
            roll += str(colored_die_number) + "_"
            player_label = tk.Label(frame, text=str(colored_die_number), bg=the_color, font=self.the_font)
            player_label.grid(row=0, column=i+1, padx=5, pady=2)
            indices = [f"{the_color}_{white_total}", f"{the_color}_{white_one+colored_die_number}", f"{the_color}_{white_two+colored_die_number}"]
            for player in self.players:
                for index in indices:
                    for button in player.buttons.get(index, []):
                        if button["state"] != tk.DISABLED:
                            self.highlighted.append(button)
                            button.config(highlightbackground="black", highlightthickness=2)
        roll += f"{white_one}_{white_two}"
        self.roll_history.append(roll)
        self.switch_player()


    def penalty_button_click(self, player, col):
        index = f"4_{col}"
        player.hist.append((index, ""))
        player.buttons[index].config(state=tk.DISABLED, text="X")


    def lock_button_click(self, player, row):
        index = f"{row}_11"
        player.hist.append((index, ""))
        player.buttons[index].config(state=tk.DISABLED)
        for i in range(11):
            player.buttons[f"{row}_{i}"].config(state=tk.DISABLED)


    def button_click(self, player, row, col, color, text):
        index = f"{row}_{col}"
        player.hist.append((index, text))
        player.buttons[index].config(state=tk.DISABLED, text="X")
        for i in range(col):
            player.buttons[f"{row}_{i}"].config(state=tk.DISABLED)
        if col == 10:
            player.buttons[f"Lock_{row}"].config(state=tk.DISABLED, text="X")


    @staticmethod
    def undo_click(player):
        if player.hist:
            last_button = player.hist.pop()
            index = last_button[0]
            row, col = index.split("_")
            row, col = int(row), int(col)
            player.buttons[index].config(state=tk.NORMAL, text=last_button[1])
            if col + 1 == 11 or col == 11:
                player.buttons[f"{row}_11"].config(state=tk.NORMAL, text="Lock")
            for i in range(col + 1):
                if player.buttons[f"{row}_{col-i}"]["text"] == "X":
                    break
                else:
                    player.buttons[f"{row}_{col-i}"].config(state=tk.NORMAL)


    def undo_roll(self, frame):
        dice_colors = ['red', "yellow", "light green", "light blue", "white", "white"]
        if len(self.roll_history)>=2:
            roll = self.roll_history[-2].split("_")
            for i in range(6):
                player_label = tk.Label(frame, text=str(roll[i]), bg=dice_colors[i], font=self.the_font)
                player_label.grid(row=0, column=i + 1, padx=5, pady=2)
            self.roll_history.pop()
        else:
            print("Cannot undo any more rolls.")


    @staticmethod
    def get_score(xs):
        return xs * (xs + 1) // 2 if 0 <= xs <= 12 else 0


    def end_game(self):
        for player in self.players:
            score = 0
            final_score = 0
            for i in range(4):
                for j in range(12):
                    if player.buttons[f"{i}_{j}"]["text"] == "X":
                        score += 1
                final_score += self.get_score(score)
                score = 0
            for i in range(4):
                if player.buttons[f"penalty_{i}"]["text"] == "X":
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
        subprocess.run(["gnome-screenshot", "-w", f"--file=Past_Games/{datetime.now().strftime('%m-%d-%Y_%H:%M:%S')}.png"], check=False)  # noqa: DTZ005


    def create_boards(self):
        combined_colors = []
        combined_numbers = []

        if restore == "yes":
            with open(r"qwixx.txt", "r") as file:
                lines = file.readlines()
            combined_colors = eval(lines[0])
            combined_numbers = eval(lines[1])
        elif mode == "1":
            combined_numbers += self.numbers * 2
            self.numbers.reverse()
            combined_numbers += self.numbers * 2
            for i in range(4):
                combined_colors += [self.colors[i]] * 11
        elif mode == "2":
            for i in range(4):
                combined_colors += [self.colors[i]] * 11
                text = self.numbers.copy()
                random.shuffle(text)
                combined_numbers += text
        elif mode == "3":
            for i in range(4):
                combined_colors += [self.colors[i]] * 11
            for number in self.numbers:
                combined_numbers += [number]*4
            random.shuffle(combined_numbers)
        elif mode == "4":
            combined_numbers += self.numbers * 2
            self.numbers.reverse()
            combined_numbers += self.numbers * 2
            temporary = []
            for i in range(11):
                shuffled_colors = self.colors.copy()
                random.shuffle(shuffled_colors)
                temporary.append(shuffled_colors)
            for i in range(2):
                for j in range(11):
                    combined_colors.append(temporary[j][i])
            for i in range(2):
                for j in range(11):
                    combined_colors.append(temporary[10-j][i+2])
        elif mode == "5":
            combined_numbers += self.numbers * 2
            self.numbers.reverse()
            combined_numbers += self.numbers * 2
            temporary = []
            for i in range(11):
                shuffled_colors = self.colors.copy()
                random.shuffle(shuffled_colors)
                temporary.append(shuffled_colors)
            for i in range(4):
                for j in range(11):
                    combined_colors.append(temporary[j][i])
        elif mode == "6":
            combined_numbers += self.numbers * 2
            self.numbers.reverse()
            combined_numbers += self.numbers * 2
            temporary = [[], [], [], []]
            shuffled_colors = self.colors.copy()
            random.shuffle(shuffled_colors)
            first = [shuffled_colors[0], shuffled_colors[1]]
            last = [shuffled_colors[2], shuffled_colors[3]]
            for i in range(11):
                random.shuffle(first)
                temporary[0].append(first[0])
                temporary[1].append(first[1])
            for i in range(11):
                random.shuffle(last)
                temporary[2].append(last[0])
                temporary[3].append(last[1])
            for i in range(4):
                combined_colors += temporary[i]
        elif mode == "7":
            combined_numbers += self.numbers * 2
            self.numbers.reverse()
            combined_numbers += self.numbers * 2
            combined_colors = []
            for color in self.colors:
                combined_colors += [color]*11
            random.shuffle(combined_colors)
        elif mode == "8":
            pairs_by_number = {n: [(n, c) for c in self.colors] for n in self.numbers}
            for i in range(4):
                random.shuffle(self.numbers)
                for num in self.numbers:
                    value = random.choices(pairs_by_number[num], k=1)
                    combined_numbers.append(value[0][0])
                    combined_colors.append(value[0][1])
                    pairs_by_number[num].remove(value[0])
        elif mode == "9":
            for i in range(4):
                combined_colors += [self.colors[i]] * 11
            for number in self.numbers:
                combined_numbers += [number]*4
            random.shuffle(combined_numbers)
            combined_colors = []
            for color in self.colors:
                combined_colors += [color]*11
            random.shuffle(combined_colors)

        with open(r"qwixx.txt", "w") as file:
            file.writelines(str(combined_colors) + "\n")
            file.writelines(str(combined_numbers))

        for player in self.players:
            for i in range(4):
                for j in range(11):
                    the_color = combined_colors[i*11+j]
                    the_number = combined_numbers[i*11+j]
                    button = tk.Button(player.frame, width=2, bg=the_color, font=self.the_font, text=the_number,
                                       highlightbackground=border_color, highlightthickness=2,
                                       command=lambda p=player, row=i, col=j, the_color=the_color, the_text=the_number: self.button_click(p, row, col, the_color, the_text))
                    button.grid(row=i + 1, column=j, padx=2, pady=2)
                    player.buttons[f"{i}_{j}"] = button
                    index = f"{the_color}_{the_number}"
                    if index not in player.buttons:
                        player.buttons[index] = []
                    player.buttons[index].append(button)
            for i in range(4):
                button = tk.Button(player.frame, width=2, bg=self.colors[i], font=self.the_font, text="Lock",
                                command=lambda p=player, row=i: self.lock_button_click(p, row))
                button.grid(row=i + 1, column=11, padx=2, pady=2)
                player.buttons[f"Lock_{i}"] = button
                player.buttons[f"{i}_11"] = button
                penalty = tk.Button(player.frame, width=2, bg="gray", font=self.the_font,
                                    command=lambda p=player, col=i: self.penalty_button_click(p, col))
                penalty.grid(row=5, column=i, padx=2, pady=2)
                player.buttons[f"penalty_{i}"] = penalty
                player.buttons[f"4_{i}"] = penalty
            undo_button = tk.Button(player.frame, width=2, font=self.the_font, bg="gray", text="Undo",
                                    command=lambda p=player: self.undo_click(p))
            undo_button.grid(row=5, column=11, padx=2, pady=2)


    def switch_player(self):
        self.players[self.current_player_index%num_players].frame.config(highlightbackground=border_color, highlightthickness=10)
        self.current_player_index += 1
        self.players[self.current_player_index%num_players].frame.config(highlightbackground="black", highlightthickness=10)

if __name__ == "__main__":
    num_players = int(input("Enter number of players: "))
    restore = input("Would you like to load the last saved board? Type 'yes' if you do. ")
    if restore!="yes":
        mode = input("1. Normal.\n2. Hodgepodge of Numbers.\n3. Pandemonium of Numbers.\n4. Hodgepodge of Colors V1.\n5. Hodgepodge of Colors V2.\n6. Hodgepodge of Colors V3.\n7. Pandemonium of Colors.\n8. Hodgepodge of Numbers and Colors.\n9. Pandemonium of Numbers and Colors.\n")
    root = tk.Tk()
    border_color = root.cget("highlightbackground")
    game = QwixxGame()
    game.create_players()
    game.create_boards()
    game.create_dice()
    root.deiconify()
    root.mainloop()
