from dataclasses import dataclass
import pandas as pd


@dataclass
class VOGData:
    """ VOG 데이터와 메타데이터를 담는 상태(State) 불변 객체 """
    file_name: str
    group: str
    session_id: str
    task_name: str
    direction: str
    df: pd.DataFrame
    target_col: str
    eye_col_l: str
    eye_col_r: str
    noise_col_l: str
    noise_col_r: str
    time_col: str