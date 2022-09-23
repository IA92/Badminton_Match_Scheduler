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


# Concat the dataframes in y axis (0) x axis (1)
def concat_lists_to_a_dataframe(lists, axis):
    df = []
    for idx in range(len(lists)):
        df.append(pd.DataFrame(lists[idx]))
    return pd.concat(df, axis=axis)


def generate_csv_from_dataframe(dataframe, file_name):
    return dataframe.to_csv(f"{file_name}.csv")
