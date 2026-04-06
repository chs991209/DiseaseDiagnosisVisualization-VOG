import pandas as pd
from pathlib import Path
from typing import List, Tuple, Optional


class VOGRobustParser:
    """
    [Parser] 데이터 로드 및 무결성 확보 책임
    Pandas의 블랙박스 파싱 에러를 우회하고, 인코딩을 자가 치유하며 파이프라인의 붕괴를 방어합니다.
    """

    def __init__(self):
        # 윈도우 의료 장비에서 출력되는 다양한 인코딩 풀 지원
        self.encodings = ['utf-16', 'utf-16le', 'utf-8-sig', 'cp949']

    def parse(self, file_path: Path) -> Optional[pd.DataFrame]:
        try:
            header_idx, header_columns, raw_lines = self._find_header(file_path)

            if header_idx == -1:
                # [Architectural Fix] Silent Failure 방지
                print(f"[Skip] {file_path.name}: VOG 헤더(LH, RH, Target)를 식별할 수 없어 건너뜁니다.")
                return None

            return self._assemble_dataframe(raw_lines, header_idx, header_columns)

        except Exception as e:
            # [Architectural Fix] 배치 파이프라인 보호 (Exception Isolation)
            print(f"[Error] {file_path.name} 파싱 중 치명적 오류 발생: {e}")
            return None

    def _find_header(self, file_path: Path) -> Tuple[int, List[str], List[str]]:
        for enc in self.encodings:
            try:
                with open(file_path, 'r', encoding=enc, errors='replace') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines):
                    line_clean = line.replace('\x00', '').lower()
                    # Domain Signature Matching
                    if 'lh' in line_clean and 'rh' in line_clean and 'target' in line_clean:
                        headers = [col.replace('\x00', '').strip() for col in line.split(',')]
                        return i, headers, lines
            except UnicodeError:
                continue
        return -1, [], []

    def _assemble_dataframe(self, raw_lines: List[str], header_idx: int, header_columns: List[str]) -> pd.DataFrame:
        parsed_data = []
        for line in raw_lines[header_idx + 1:]:
            line_clean = line.replace('\x00', '').strip()
            if not line_clean:
                continue

            row_values = [val.strip() for val in line_clean.split(',')]

            # 길이 보정 (Padding / Truncation)
            if len(row_values) < len(header_columns):
                row_values.extend([''] * (len(header_columns) - len(row_values)))
            elif len(row_values) > len(header_columns):
                row_values = row_values[:len(header_columns)]

            parsed_data.append(row_values)

        df = pd.DataFrame(parsed_data, columns=header_columns)
        df = df.apply(pd.to_numeric, errors='coerce')
        return df.dropna(how='all').reset_index(drop=True)