import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os, sys


def get_file_path(type, message):
    root = tk.Tk()
    root.withdraw()  # use to hide tkinter window
    file_path = filedialog.askopenfilename(
        parent=root,
        initialdir=os.getcwd(),
        title=message,
        filetypes=type,
    )
    if len(file_path) > 0:
        print(f"The file to be processed is {file_path}")
        return file_path
    else:
        print(f"No file chosen")
        sys.exit()


def get_input_integer(message):
    root = tk.Tk()
    root.withdraw()  # use to hide tkinter window
    return int(tk.simpledialog.askstring("Input", message))


# Convert a list of lists to a list of dataframes
def convert_lists_to_a_list_of_dataframe(lists):
    df = []
    for idx in range(len(lists)):
        each_df = pd.DataFrame(lists[idx])
        df.append(each_df)
    return df


# Concat a list of list to a dataframe in y axis (0) x axis (1)
def concat_lists_to_a_dataframe(lists, axis):
    df = []
    for idx in range(len(lists)):
        each_df = pd.DataFrame(lists[idx])
        df.append(each_df)
    return pd.concat(df, axis=axis)


# Concat dataframes in y axis (0) x axis (1)
def concat_dataframes_to_a_dataframe(dfs, axis):
    df = []
    for idx in range(len(dfs)):
        each_df = dfs[idx]
        df.append(each_df)
    return pd.concat(df, axis=axis)


def generate_csv_from_dataframe(dataframe, file_name):
    return dataframe.to_csv(f"{file_name}.csv")


def generate_excel_from_list_of_dataframe(dataframe_list, file_name, sheet_name):
    with pd.ExcelWriter(f"{file_name}.xlsx") as writer:
        for idx in range(len(dataframe_list)):
            dataframe_list[idx].to_excel(
                writer, sheet_name=f"{sheet_name} {idx+1}", header=False, index=False
            )
