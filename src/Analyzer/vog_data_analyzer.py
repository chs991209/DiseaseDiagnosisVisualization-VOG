import pandas as pd
from pathlib import Path
from typing import List, Tuple, Optional
from src.Dto.vog_data_entity import VOGData


class VOGDomainAnalyzer:
    def extract_metadata(self, file_path: Path) -> Tuple[str, str, str]:
        """
        데이터 디렉토리 구조(Path)를 역추적하여 메타데이터를 도출합니다.
        예: data/sample_csv/HC_csv_24_25/20240329.../PD VOG -_...csv
        """
        # 상위 2단계 폴더명 (HC_csv_24_25 또는 MCI_csv_25_26)
        group_name = (
            file_path.parent.parent.name
            if len(file_path.parents) >= 2
            else "Unknown_Group"
        )
        # 상위 1단계 폴더명 (20240329_084111_1324721_)
        session_id = file_path.parent.name
        # 파일명에서 불필요한 접두어 정리
        task_name = (
            file_path.stem.replace("PD VOG -_", "").replace("PD VOG -", "").strip()
        )
        return group_name, session_id, task_name

    def analyze(self, file_path: Path, df: pd.DataFrame) -> Optional[VOGData]:
        time_col = self._find_col(df, ["time", "t"]) or df.columns[0]

        target_v = self._find_col(df, ["targetv", "target_v"])
        target_h = self._find_col(df, ["targeth", "target_h"])

        target_col = (
            target_v if (target_v and df[target_v].abs().sum() > 0) else target_h
        )
        if not target_col:
            return None

        # Determine the primary axis of movement (Vertical or Horizontal)
        direction = "Vertical" if "v" in target_col.lower() else "Horizontal"

        eye_col_l = self._find_col(
            df, ["lv" if direction == "Vertical" else "lh"], exact=True
        )
        eye_col_r = self._find_col(
            df, ["rv" if direction == "Vertical" else "rh"], exact=True
        )

        if not eye_col_l or not eye_col_r:
            return None

        # Feature Engineering: 추적 오차(Error) 계산
        df["Error_L"] = df[eye_col_l] - df[target_col]
        df["Error_R"] = df[eye_col_r] - df[target_col]

        # --- Detecting Outlier Noise Process ---
        # The logic here is to capture the eye movements on the axis orthogonal (perpendicular)
        # to the primary target movement axis.
        # For instance, if the target is moving vertically (direction == "Vertical"),
        # then any significant horizontal movement (lh, rh) is considered statistical noise or an outlier.
        # This cross-axis noise helps in evaluating the quality of the subject's focus
        # and identifying artifacts like blinks, head movements, or lack of attention.
        """
        This logic deliberately eschews algorithmic data clipping in favor of qualitative visual diagnostics. 
        By extracting the raw, orthogonal positional data relative to the primary stimulus vector 
        (e.g., horizontal variance during a vertical task), 
        it visualizes the departure from the theoretical trajectory. 
        This unadulterated plotting allows statisticians and clinicians to visually identify 
        the nature of the variance—distinguishing between random stochastic noise and systematic artifacts 
        (e.g., unintended saccades or spatial drifts)—rather than masking them through automated outlier removal.
        """
        noise_col_l = self._find_col(
            df, ["lh" if direction == "Vertical" else "lv"], exact=True
        )
        noise_col_r = self._find_col(
            df, ["rh" if direction == "Vertical" else "rv"], exact=True
        )

        group, session, task = self.extract_metadata(file_path)

        return VOGData(
            file_name=file_path.name,
            group=group,
            session_id=session,
            task_name=task,
            direction=direction,
            df=df,
            target_col=target_col,
            eye_col_l=eye_col_l,
            eye_col_r=eye_col_r,
            noise_col_l=noise_col_l,
            noise_col_r=noise_col_r,
            time_col=time_col,
        )

    def _find_col(
        self, df: pd.DataFrame, keywords: List[str], exact: bool = False
    ) -> Optional[str]:
        for col in df.columns:
            col_lower = str(col).lower()
            for kw in keywords:
                if exact and col_lower == kw:
                    return col
                if not exact and kw in col_lower:
                    return col
        return None
