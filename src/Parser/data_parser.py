import pandas as pd
from pathlib import Path
from typing import List, Tuple, Optional


class VOGRobustParser:
    def __init__(self):
        # 윈도우 의료 장비에서 출력되는 다양한 인코딩 풀 지원
        self.encodings = ['utf-16', 'utf-16le', 'utf-8-sig', 'cp949']

    def parse(self, file_path: Path) -> Optional[pd.DataFrame]:
        header_idx, header_columns, raw_lines = self._find_header(file_path)

        if header_idx == -1:
            return None

        return self._assemble_dataframe(raw_lines, header_idx, header_columns)

    def _find_header(self, file_path: Path) -> Tuple[int, List[str], List[str]]:
        for enc in self.encodings:
            try:
                with open(file_path, 'r', encoding=enc, errors='replace') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines):
                    line_clean = line.replace('\x00', '').lower()
                    # Domain Signature Matching: LH, RH, Target이 모두 포함된 줄을 진짜 헤더로 판단
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

            # 길이 보정 (안전망: Padding / Truncation)
            if len(row_values) < len(header_columns):
                row_values.extend([''] * (len(header_columns) - len(row_values)))
            elif len(row_values) > len(header_columns):
                row_values = row_values[:len(header_columns)]

            parsed_data.append(row_values)

        df = pd.DataFrame(parsed_data, columns=header_columns)
        df = df.apply(pd.to_numeric, errors='coerce')
        return df.dropna(how='all').reset_index(drop=True)