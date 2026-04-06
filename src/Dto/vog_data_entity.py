from dataclasses import dataclass
import pandas as pd


@dataclass
class VOGData:
    """
    VOG 데이터와 메타데이터를 담는 상태(State) 불변 객체
    (Data Transfer Object)
    """
    file_name: str
    group: str
    session_id: str
    task_name: str
    direction: str
    is_anti: bool              # Anti-saccade 여부 상태값
    df: pd.DataFrame
    target_col: str
    expected_target_col: str   # 보정된 타겟(Expected Target) 컬럼명
    eye_col_l: str
    eye_col_r: str
    noise_col_l: str
    noise_col_r: str
    time_col: str