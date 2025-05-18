import tkinter.messagebox
import customtkinter
import re
import tkinter
import os
import math
import sys
from PIL import Image
import requests

def srank(rank):
    rank = str(rank)
    ranks = {"Iron":"1", "Bronze":"2", "Silver":"3", "Gold":"4", "Platinum":"5", "Emerald":"6", "Diamond":"7"}
    return ranks.get(rank, "1")

folder_name = "leaguecalculator"
file_path = os.path.join(os.environ['APPDATA'], folder_name)
if not os.path.exists(file_path):
    os.makedirs(file_path)

def download_img(dir, name, pic_url):
    with open(os.path.join(dir, name), 'wb') as handle:
        response = requests.get(pic_url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    logo = Image.open(os.path.join(dir, name))
    new_name = "lol.ico"
    logo.save(os.path.join(dir, new_name), format="ICO")
    os.remove(os.path.join(dir, name))

def file_write(file, object):
    try:
        with open(file, "w") as f:
            f.write(object)
            return True
    except:
        return False

def look_for_files():
    package = "https://raw.githubusercontent.com/zgndia/league-lp-tracker/refs/heads/main/data/essentials.py"
    filename = "essentials.py"
    
    response = requests.get(package)

    defaultrank = "1\n4\n0\n20-25"
    items = ["lol.ico", "essentials.py", "rank.txt"]

    for item in items:
        print('Checking "' + item + '"...')
        if not os.path.exists(os.path.join(file_path, item)):
            if items[0] == item:
                download_img(file_path, "lol.png", "https://i.postimg.cc/8zdm3x9S/lol.png")
            if items[1] == item:
                if response.status_code == 200:
                    file_write(os.path.join(file_path, "essentials.py"), response.text)
                    print(f"Downloaded successfully as {filename}")
            if items[2] == item:
                file_write(os.path.join(file_path, "rank.txt"), defaultrank)

look_for_files()

sys.path.insert(0, file_path)
from essentials import *

class league():
    @staticmethod
    def round_up(n, p):
        m = 10 ** p
        return (math.ceil(n * m) / m)

    @staticmethod
    def substring_after(s, delim):
        return s.partition(delim)[2]

    @staticmethod
    def sortRank(currentrank):
        ranks = {1: "Iron", 2: "Bronze", 3: "Silver", 4: "Gold", 5: "Platinum", 6: "Emerald", 7: "Diamond"}
        rank = ranks.get(currentrank, "Iron")
        return rank

    def get_rank(self):
        txt = file.read(os.path.join(file_path, "rank.txt")).split()
        currentrank = txt[0]
        bracket = txt[1]
        lp = int(txt[2])
        gains = txt[3].replace("-", " ").split()
        p_gains, s_gains = gains[1], gains[0]
        return [self.sortRank(int(currentrank)), bracket, lp, p_gains, s_gains, currentrank]

    def get_text(self):
        data = self.get_rank(self)
        rank = data[0]
        bracket = int(data[1])
        lp = int(data[2])
        gains = int(self.round_up(int(data[3]) - (int(data[3]) / int(data[4])), 0))

        game = (100 - lp) / gains
        game = int(self.round_up(game, 0))
        if game < 1:
            game = 1
        addition = "s" if game > 1 else ""
        return f"You are {rank} {bracket}, {lp} lp. \n+{100 - lp} lp's to rankup.\nEstimated {game} (+{gains} lp per) game{addition} away from rankup."

    def get_newrank(interact, self):
        data = self.get_rank(self)
        bracket = int(data[1])
        lp = int(data[2])
        gains = data[3] + "-" + data[4]
        numrank = int(data[5])

        if interact is None:
            return
        if interact[0] == "-":
            num = self.substring_after(interact, "-")
            afterlp = int(lp) - int(num)
            if afterlp < 0:
                afterlp = 50
                if bracket == 4:
                    numrank -= 1
                    bracket = 1
                elif bracket < 4:
                    bracket += 1
                if numrank < 1:
                    numrank = 1
            data = f"{numrank}\n{bracket}\n{afterlp}\n{gains}"
            file.write(os.path.join(file_path, "rank.txt"), data)
            
        elif interact[0] == "+" or interact.isdigit():
            if not interact.isdigit():
                num = self.substring_after(interact, "+")
            else:
                num = int(interact)
            afterlp = int(lp) + int(num)
            while int(afterlp) > 99:
                afterlp = int(afterlp)
                afterlp = afterlp - 100
                afterlp = str(afterlp).replace("+","")
                if bracket == 1:
                    numrank += 1
                    bracket = 4
                elif bracket > 1:
                    bracket -= 1
                if numrank > 7:
                    numrank = 7
            
            data = f"{numrank}\n{bracket}\n{afterlp}\n{gains}"
            file.write(os.path.join(file_path, "rank.txt"), data)

def organizeText():
    x = league.get_text(league)
    t = [i.strip() for i in x.splitlines()]
    text = []
    for line in t:
        if not line == t[-1]:
            text.append("\t            " + line)
            continue
        text.append(line)
    return text

class LeagueGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")

        self.resizable(False, False)
        self.tabview = customtkinter.CTkTabview(self, width=320, height=0)
        self.tabview.add("View Stats")
        self.tabview.add("Set Rank")

        ranks = ["Iron","Bronze","Silver","Gold","Platinum","Emerald","Diamond"]
        brackets = ["1","2","3","4"]
        gains = ["15-20", "20-25", "25-30", "30-40"]

        second_tab = customtkinter.CTkOptionMenu(self.tabview.tab("Set Rank"), dynamic_resizing=False, values=(ranks), command=self.set_rank)
        second_tab_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Set Rank"), dynamic_resizing=False, values=(brackets), command=self.set_brackets)
        second_tab_3 = customtkinter.CTkOptionMenu(self.tabview.tab("Set Rank"), dynamic_resizing=False, values=(gains), command=self.set_gains)

        self.title("League WR Ratio")
        self.iconbitmap(os.path.join(file_path, "lol.ico"))

        self.app_width, self.app_height = 600, 400
        self.set_window_position()

        self.tabview.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.label = customtkinter.CTkLabel(text="Rank\t:", width=50, height=50, master=self.tabview.tab("Set Rank"))
        self.label_2 = customtkinter.CTkLabel(text="Bracket \t:", width=50, height=50, master=self.tabview.tab("Set Rank"))
        self.label_3 = customtkinter.CTkLabel(text="Gains \t:", width=50, height=50, master=self.tabview.tab("Set Rank"))
        self.textbox = customtkinter.CTkTextbox(width=300, height=150, master=self.tabview.tab("View Stats"))
        self.button = customtkinter.CTkButton(master=self.tabview.tab("View Stats"), text="Match Result", command=self.open_input_dialog_event)
        self.button_2 = customtkinter.CTkButton(master=self.tabview.tab("View Stats"), text="Reset LP", width=10, height=26,command=self.reset_lp)
        self.logo_label = customtkinter.CTkLabel(self, text="Made by Zgn", font=customtkinter.CTkFont(size=16, weight="bold"))

        self.textbox.grid(column=0, row=0,padx=(0,0), pady=(0,75))
        second_tab.grid(row=0, column=1, padx=(150, 0), pady=(0, 200))
        second_tab_2.grid(row=0, column=1, padx=(150, 0), pady=(0, 100))
        second_tab_3.grid(row=0, column=1, padx=(150, 0), pady=(0, 0))
        self.label.grid(row=0, column=1, padx=(0, 75), pady=(0, 200))
        self.label_2.grid(row=0, column=1, padx=(0, 75), pady=(0, 100))
        self.label_3.grid(row=0, column=1, padx=(0, 75), pady=(0, 0))
        self.button.grid(column=0, row=0,padx=(70,0), pady=(125,0))
        self.button_2.grid(column=0, row=0,padx=(0,140), pady=(125,0))
        self.logo_label.grid(row=0, column=0, padx=(5, 0), pady=(360, 0))

        self.update_textbox()

    def set_window_position(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (self.app_width / 2)
        y = (screen_height / 2) - (self.app_height / 2)
        self.geometry(f"{self.app_width}x{self.app_height}+{int(x)}+{int(y)}")

    def set_rank(self, rank):
        x = file.readlines(os.path.join(file_path, "rank.txt"))
        x[0] = srank(rank) + "\n"
        file.write(os.path.join(file_path, "rank.txt"), ''.join(x))
        self.update_textbox()

    def set_brackets(self, bracket):
        x = file.readlines(os.path.join(file_path, "rank.txt"))
        x[1] = bracket + "\n"
        file.write(os.path.join(file_path, "rank.txt"), ''.join(x))
        self.update_textbox()
    
    def reset_lp(self):
        q=tkinter.messagebox.askquestion(title=None, message="Are you sure that you are going to reset your LP?")
        if q!="yes":
            return
        
        x = file.readlines(os.path.join(file_path, "rank.txt"))
        x[2] = "0" + "\n"
        file.write(os.path.join(file_path, "rank.txt"), ''.join(x))
        self.update_textbox()

    def set_gains(self, gains):
        x = file.readlines(os.path.join(file_path, "rank.txt"))
        x[3] = gains
        file.write(os.path.join(file_path, "rank.txt"), ''.join(x))
        self.update_textbox()

    def update_textbox(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", customtkinter.END)
        text = organizeText()
        self.textbox.insert("0.0", "\t\tLP Tracker\n\n\n" + '\n'.join(text))
        self.textbox.configure(state="disabled")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Enter your LP\n(such as +25 or -8)", title="League WR Ratio")
        dialog_width, dialog_height = 300, 200
        x, y = self.get_window_position(dialog_width, dialog_height, self)
        dialog.geometry(f"{dialog_width}x{dialog_height}+{int(x)}+{int(y)}")
        lp = str(dialog.get_input())
        league.get_newrank(lp, league)
        self.update_textbox()

    @staticmethod
    def get_window_position(width, height, self):
        screen_width = LeagueGUI.winfo_screenwidth(self)
        screen_height = LeagueGUI.winfo_screenheight(self)
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        return x, y

if __name__ == "__main__":
    app = LeagueGUI()
    app.mainloop()
