from pyxll import xl_func
from scheduler import Scheduler
from utils import concat_lists_to_a_dataframe, concat_dataframes_to_a_dataframe


# Please make sure that the data provided is either a list of 2 players or 4 players with clean formatting
@xl_func
def get_scheduled_matches_for_1_courts(data):
    sched = Scheduler(data, 1)
    sched.get_scheduled_games()
    return concat_lists_to_a_dataframe(sched.scheduled_games, 1).to_numpy().tolist()


@xl_func
def get_scheduled_matches_for_2_courts(data):
    sched = Scheduler(data, 2)
    sched.get_scheduled_games()
    return concat_lists_to_a_dataframe(sched.scheduled_games, 1).to_numpy().tolist()


@xl_func
def get_scheduled_matches_for_1_courts_with_formatting(data):
    sched = Scheduler(data, 1)
    sched.get_scheduled_games()
    return (
        concat_dataframes_to_a_dataframe(
            sched.get_formatted_matches_as_list_of_dataframe(), 1
        )
        .to_numpy()
        .tolist()
    )


@xl_func
def get_scheduled_matches_for_2_courts_with_formatting(data):
    sched = Scheduler(data, 2)
    sched.get_scheduled_games()
    return (
        concat_dataframes_to_a_dataframe(
            sched.get_formatted_matches_as_list_of_dataframe(), 1
        )
        .to_numpy()
        .tolist()
    )
