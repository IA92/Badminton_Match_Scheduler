from pyxll import xl_func
from scheduler import Scheduler
from utils import concat_lists_to_a_dataframe


@xl_func
def get_scheduled_matches_for_1_courts(data):
    sched = Scheduler(data, 1)
    sched.get_scheduled_games()
    return concat_lists_to_a_dataframe(sched.scheduled_games, 1)


@xl_func
def get_scheduled_matches_for_2_courts(data):
    sched = Scheduler(data, 2)
    sched.get_scheduled_games()
    return concat_lists_to_a_dataframe(sched.scheduled_games, 1)
