## Badminton Match Scheduler
A scheduler that creates a badminton match schedule given the number of court the matches are going to be played at. 

The application can be used in two ways:
- As an excel add-in with [pyxll](https://www.pyxll.com/index.html)
    - Require the installation of python and its dependency
    - Require the installation of pyxll
- As a standalone executable that generates a csv file as the output

## Getting started to build the scheduler as an excel add-in
- Install python and pip from [here](https://www.python.org/)
- Open cmd prompt if you are on Windows
- Navigate to `scheduler_add_in` folder
- Run `pip install -r requirements.txt`
- Install pyxll (More information can be found [here](https://www.pyxll.com/docs/introduction.html#quickstart))
    - Download pyxll from [here](https://www.pyxll.com/download.html)
    - Open cmd prompt if you are on Windows
    - Run `pyxll install`
    - When prompt if pyxll has been downloaded, answer yes `y`
    - When prompt for the path to the downloaded pyxll, provide the path to the downloaded pyxll zip folder
    - The installation is complete!
    - Open excel and go to the new tab `PyXLL Example Tab`>`About PyXLL`>Click on the hyperlink to `pyxll.cfg` file
    - In the `pythonpath` section, add the path to the directory to the `.py` file where the python functions to be accessed are, e.g., `path_to_local_repository\scheduler_add_in`
    - In the `modules` section, add the filename of the `.py` where the python functions to be accessed are, e.g., `scheduler_add_in`
- In excel, go to the new tab `PyXLL Example Tab` and click the `Reload PyXLL` button
- Now the python functions from that module should be available in the excel
    Try typing `=function_name`, the auto complete should be available there
    
## Getting started to build the scheduler as an executable
- Install python and pip from [here](https://www.python.org/)
- Open cmd prompt if you are on Windows
- Navigate to `scheduler_exe` folder
- Run `pip install -r requirements.txt`
- Navigate to directory where the python file to be compiled is located, e.g., `path_to_local_repository`
    - Run `pyinstaller -F filename.py` or `pyinstaller --onefile filename.py`, e.g., `pyinstaller -F scheduler.py`
    - The executable will be created under a folder called `dist`!
    - Run the executable
        - Select the appropriate input file that contains a list of matches 
        - Input an integer as the number of courts where the organised matches will be allocated to
        - A `scheduled_games.csv ` file will be created in the same folder where the executable is located
            - This file will consist of the newly scheduled games (Note: The sequence of the scheduled games will be different each time the app is run)
            

