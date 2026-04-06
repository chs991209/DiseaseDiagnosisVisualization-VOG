import pandas as pd
from pathlib import Path
from typing import List, Tuple, Optional
from src.Dto.vog_data_entity import VOGData


class VOGDomainAnalyzer:
    """
    VOG 데이터의 도메인 로직을 처리하는 핵심 분석기(Analyzer).
    메타데이터 추출, 파생 변수(Error) 계산, Anti-saccade 반전 및 교차 축 노이즈 식별을 담당합니다.
    """

    def extract_metadata(self, file_path: Path) -> Tuple[str, str, str]:
        """데이터 디렉토리 구조(Path)를 역추적하여 메타데이터를 도출합니다."""
        group_name = (
            file_path.parent.parent.name
            if len(file_path.parents) >= 2
            else "Unknown_Group"
        )
        session_id = file_path.parent.name
        task_name = (
            file_path.stem.replace("PD VOG -_", "").replace("PD VOG -", "").strip()
        )
        return group_name, session_id, task_name

    def analyze(self, file_path: Path, df: pd.DataFrame) -> Optional[VOGData]:
        # 1. 파일 구조로부터 도메인 메타데이터 선행 추출
        group, session, task = self.extract_metadata(file_path)

        time_col = self._find_col(df, ["time", "t"]) or df.columns[0]

        target_v = self._find_col(df, ["targetv", "target_v"])
        target_h = self._find_col(df, ["targeth", "target_h"])

        target_col = (
            target_v if (target_v and df[target_v].abs().sum() > 0) else target_h
        )
        if not target_col:
            return None

        # Determine the primary axis of movement
        direction = "Vertical" if "v" in target_col.lower() else "Horizontal"

        eye_col_l = self._find_col(
            df, ["lv" if direction == "Vertical" else "lh"], exact=True
        )
        eye_col_r = self._find_col(
            df, ["rv" if direction == "Vertical" else "rh"], exact=True
        )

        if not eye_col_l or not eye_col_r:
            return None

        # =========================================================================
        # [ARCHITECTURAL UPDATE] Dynamic Target Inversion for Anti-Saccade Tasks
        # =========================================================================
        """
        If the name has 'anti'
        """
        is_anti = "anti" in task.lower()

        if is_anti:
            df["Expected_Target"] = -df[target_col]
        else:
            df["Expected_Target"] = df[target_col]

        # Feature Engineering: Calculate Tracking Error
        df["Error_L"] = df[eye_col_l] - df["Expected_Target"]
        df["Error_R"] = df[eye_col_r] - df["Expected_Target"]

        # =========================================================================
        # [DOMAIN LOGIC SEPARATION] Extracting Orthogonal Variance
        # =========================================================================
        noise_col_l, noise_col_r = self._extract_orthogonal_noise(df, direction)

        return VOGData(
            file_name=file_path.name,
            group=group,
            session_id=session,
            task_name=task,
            direction=direction,
            is_anti=is_anti,
            df=df,
            target_col=target_col,
            expected_target_col="Expected_Target",
            eye_col_l=eye_col_l,
            eye_col_r=eye_col_r,
            noise_col_l=noise_col_l,
            noise_col_r=noise_col_r,
            time_col=time_col,
        )

    def _extract_orthogonal_noise(
        self, df: pd.DataFrame, direction: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts the eye movement data on the axis orthogonal (perpendicular)
        to the primary target movement axis.

        [Methodological Note on Outlier Handling & EDA]
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
        return noise_col_l, noise_col_r

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