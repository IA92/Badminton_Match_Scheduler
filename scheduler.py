import numpy as np
import pandas as pd
import random

import tkinter as tk
import os, sys
from tkinter import filedialog

from utils import (
    concat_lists_to_a_dataframe,
    generate_excel_from_list_of_dataframe,
)


class Scheduler:
    def __init__(self, games, court_number):
        self.games = games
        self.players = set([item for sublist in self.games for item in sublist])
        self.court_number = court_number

    def __overlap_check(self, possible_combinations, accepted_list):
        number_of_games_left = len(possible_combinations)
        print(f"number of games left {number_of_games_left}")
        for i in range(number_of_games_left):
            check = all(item in accepted_list for item in possible_combinations[i])
            if check:
                return i

    def __remove_from_a_pool(self, pool, remove_list):
        try:
            for remove_idx in range(len(remove_list)):
                pool.remove(remove_list[remove_idx])
            return pool
        except:
            print(
                f"Remove ERROR: pool is {pool} and players to be removed is {remove_list}"
            )

    def get_scheduled_games(self):
        # Start scheduling
        total_games = len(self.games)
        initial_games = self.games.copy()
        for attempt_idx in range(100):
            random.shuffle(initial_games)
            self.games = initial_games.copy()
            self.scheduled_games = []
            # Create a placeholder for the new scheduled games
            for court_idx in range(self.court_number):
                self.scheduled_games.append([])
            # Create variables for the algorithm
            player_pool = self.players.copy()
            pool_idx = 0
            pool_idx_max = self.court_number
            remove_idx = 0
            remove_idx_max = self.court_number
            players_to_be_removed = []
            for games_idx in range(total_games):
                idx = self.__overlap_check(self.games, player_pool)
                if idx == None:
                    player_pool = self.players.copy()
                    self.__remove_from_a_pool(player_pool, players_to_be_removed)
                    idx = self.__overlap_check(self.games, player_pool)
                try:
                    self.scheduled_games[pool_idx].append(self.games[idx])
                except:
                    print(f"Couldn't find non-overlapping games, retrying...")
                    games_idx = total_games
                    break
                pool_idx += 1
                if pool_idx >= pool_idx_max:
                    pool_idx = 0
                players_to_be_removed.extend(self.games[idx])
                remove_idx += 1
                if remove_idx >= remove_idx_max:
                    remove_idx = 0
                    players_to_be_removed = []
                if self.court_number == 1:
                    players_to_be_removed.extend(self.games[idx])
                # Removing the players from previous game from the player pool
                self.__remove_from_a_pool(player_pool, self.games[idx])
                self.games.remove(self.games[idx])
            if len(self.games) == 0:
                print(
                    "Games scheduled successfully! Results is written to scheduled_games.csv/xlsx."
                )
                return self.scheduled_games
            else:
                print(
                    "Fail to schedule the game, please retry with lesser number of courts"
                )

    def get_formatted_matches_as_list_of_dataframe(self):
        # Get a list of formatted dataframe
        df = []
        for idx in range(len(self.scheduled_games)):
            each_df = pd.DataFrame(self.scheduled_games[idx])
            # Insert the scoring and vs columns in the middle
            middle_column_idx = int(
                len(each_df.columns) / 2
            )  # e.g., 1 for single matches and 2 for double matches
            each_df.insert(middle_column_idx, "score 1", "")
            each_df.insert(middle_column_idx + 1, "vs", "vs")
            each_df.insert(middle_column_idx + 2, "score 2", "")
            df.append(each_df)
        return df

    def __str__(self) -> str:
        return f"Scheduler of {len(self.games)} games and players: ({self.players})"


class Scheduler_gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x250")
        self.root.title("Scheduler.exe")
        # Create text to browse for the input .xlsx/.csv file
        self.frame_browse_directory = tk.Frame(self.root, borderwidth=25)
        self.frame_browse_directory.pack(fill=tk.X)
        self.label_browse_directory = tk.Label(
            self.frame_browse_directory,
            text="File:",
        )
        self.label_browse_directory.pack(side=tk.TOP, anchor=tk.NW)
        # Create a text window to show the chosen path
        self.text_browse_directory = tk.Text(
            self.frame_browse_directory,
            height=1,
            width=45,
            bg="light grey",
        )
        self.text_browse_directory.pack(side=tk.LEFT)
        self.text_browse_directory.insert(1.0, "Please choose a .xlsx or.csv file")
        self.text_browse_directory.config(state=tk.DISABLED)
        # Create button to open the browse dialog window
        self.button_browse_directory = tk.Button(
            self.frame_browse_directory,
            text="Browse",
            command=self.get_file_path_for_match_file,
        ).pack(side=tk.RIGHT)
        # # Create a text window to get the sheet name
        self.frame_sheet_name = tk.Frame(self.root, padx=25)
        self.frame_sheet_name.pack(fill=tk.X)
        self.label_sheet_name = tk.Label(
            self.frame_sheet_name,
            text="Sheet name:",
        )
        self.label_sheet_name.pack(side=tk.LEFT)
        self.text_sheet_name = tk.Text(self.frame_sheet_name, height=1, width=45)
        self.text_sheet_name.pack(side=tk.RIGHT)
        self.text_sheet_name.insert(1.0, "Sheet1")
        ## Create dropdown menu to select the number of courts
        self.frame_select_court_numer = tk.Frame(
            self.root,
            padx=25,
        )
        self.frame_select_court_numer.pack(fill=tk.X)
        # Create label to display text to select the number of courts
        self.label_select_court_number = tk.Label(
            self.frame_select_court_numer,
            text="Number of court:",
        )
        self.label_select_court_number.pack(side=tk.LEFT)
        # Dropdown menu options
        options = [
            "1",
            "2",
            "3",
            "4",
        ]

        # datatype of menu text
        self.selected_court_number = tk.StringVar()
        self.selected_court_number.set("1")  # initial menu text

        # Create Dropdown menu
        drop = tk.OptionMenu(
            self.frame_select_court_numer, self.selected_court_number, *options
        )
        drop.pack(side=tk.LEFT)

        ## Create frame for the run scheduler button
        self.frame_run_sheduler = tk.Frame(
            self.root,
            borderwidth=25,
        )
        self.frame_run_sheduler.pack(side=tk.BOTTOM, fill=tk.X)
        # Create run status text
        self.label_run_status = tk.Label(self.frame_run_sheduler, text="")
        self.label_run_status.pack(side=tk.TOP)
        # Create button to run the scheduler
        self.button_run_scheduler = tk.Button(
            self.frame_run_sheduler,
            text="Run scheduler",
            state=tk.DISABLED,
            command=self.get_scheduled_matches,
        )
        self.button_run_scheduler.pack(side=tk.BOTTOM)

        # Defining custom protocol for the 'x' button
        self.root.protocol("WM_DELETE_WINDOW", self.gui_exit_function)
        # Run the mainloop
        self.root.mainloop()

    def get_file_path_for_match_file(self):
        root = tk.Tk()
        root.withdraw()  # use to hide tkinter window
        type = [("Excel files", ".xlsx .xls"), ("CSV files", ".csv")]
        message = "Please select a csv file that contains the matches to be scheduled"
        self.file_path = filedialog.askopenfilename(
            parent=root,
            initialdir=os.getcwd(),
            title=message,
            filetypes=type,
        )
        if len(self.file_path) > 0:
            self.text_browse_directory.config(state=tk.NORMAL)
            self.text_browse_directory.delete(1.0, tk.END)
            self.text_browse_directory.insert(1.0, self.file_path)
            self.text_browse_directory.config(state=tk.DISABLED)
            # Enable run scheduler buttons
            self.button_run_scheduler.config(state=tk.NORMAL)
        else:
            self.text_browse_directory.delete(1.0, tk.END)
            self.text_browse_directory.insert(1.0, "No file chosen")
            self.file_path = ""

    def get_scheduled_matches(self):
        ## Process the data from the input file
        # Get data from the excel sheet, e.g., games and players
        self.selected_sheet_name = self.text_sheet_name.get(1.0, "end-1c")
        try:
            games = pd.read_excel(self.file_path, self.selected_sheet_name, header=None)
        except:
            # Update the run status text
            self.label_run_status.config(
                text="Run failed, please ensure correct data and sheet name in the excel file.",
                foreground="red",
            )
        games = games.replace("(?i)vs", np.nan, regex=True)
        games = games.dropna(axis=1)
        games = games.to_numpy().tolist()
        random.shuffle(games)

        # Get the scheduled games
        # Turn selected court number to integer
        selected_court_number = int(self.selected_court_number.get())
        sched = Scheduler(games, selected_court_number)
        try:
            scheduled_games = sched.get_scheduled_games()
        except:
            # Update the run status text
            self.label_run_status.config(
                text="Run failed, please ensure correct input.", foreground="red"
            )
        # Generate an excel file with scheduled matches in each court at different sheet
        generate_excel_from_list_of_dataframe(
            sched.get_formatted_matches_as_list_of_dataframe(),
            "scheduled_games",
            "Court",
        )
        # Print the scheduled games
        print(concat_lists_to_a_dataframe(sched.scheduled_games, 1))
        # Update the run status text
        self.label_run_status.config(
            text="Completed! Rerun for different results.", foreground="green"
        )

    def gui_exit_function(self):
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    scheduler_gui = Scheduler_gui()
