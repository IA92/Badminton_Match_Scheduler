import numpy as np
import pandas as pd
import random

from utils import (
    get_file_path,
    get_input_integer,
    concat_dataframes_to_a_dataframe,
    concat_lists_to_a_dataframe,
    generate_csv_from_dataframe,
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


if __name__ == "__main__":
    # Get the file path
    path_to_games_excel_file = get_file_path(
        [("Excel files", ".xlsx .xls"), ("CSV files", ".csv")],
        "Please select a csv file that contains the matches to be scheduled",
    )

    # Get data from the excel sheet, e.g., games and players
    games = pd.read_excel(path_to_games_excel_file, "Sheet1", header=None)
    games = games.replace("(?i)vs", np.nan, regex=True)
    games = games.dropna(axis=1)
    games = games.to_numpy().tolist()
    random.shuffle(games)
    # Get the court number
    court_number = get_input_integer(
        "Input the court number for the scheduled games (int)"
    )
    # Get the scheduled games
    sched = Scheduler(games, court_number)
    scheduled_games = sched.get_scheduled_games()
    # Generate an excel file with scheduled matches in each court at different sheet
    generate_excel_from_list_of_dataframe(
        sched.get_formatted_matches_as_list_of_dataframe(),
        "scheduled_games",
        "Court",
    )
    # Print the scheduled games
    print(concat_lists_to_a_dataframe(sched.scheduled_games, 1))
    input("Press any key to close this window...")
