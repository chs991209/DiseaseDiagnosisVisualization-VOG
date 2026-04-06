import sys
from pathlib import Path

# 모듈 시스템 절대 경로 임포트 보장
current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from src.Parser.data_parser import VOGRobustParser
from src.Analyzer.vog_data_analyzer import VOGDomainAnalyzer
from src.Visualizer.visualizer import VOGMatplotlibVisualizer


class VOGPipelineFacade:
    def __init__(self, parser=None, analyzer=None, visualizer=None):
        self.parser = parser or VOGRobustParser()
        self.analyzer = analyzer or VOGDomainAnalyzer()
        self.visualizer = visualizer or VOGMatplotlibVisualizer()

    def process_file(self, file_path: Path) -> bool:
        if not file_path.exists():
            return False

        df = self.parser.parse(file_path)
        if df is None: return False

        vog_data = self.analyzer.analyze(file_path, df)
        if vog_data is None: return False

        self.visualizer.plot(vog_data)
        return True

    def process_directory(self, base_dir: Path) -> None:
        if not base_dir.exists():
            print(f"[Error] 데이터 디렉토리를 찾을 수 없습니다: {base_dir}")
            return

        csv_files = list(base_dir.rglob('*.csv'))

        print("=" * 60)
        print(f"🚀 VOG 데이터 배치 파이프라인 가동")
        print(f"- 대상: {base_dir.resolve()}")
        print(f"- 수량: 총 {len(csv_files)}개 파일")
        print("=" * 60)

        success_count = 0
        for i, path in enumerate(csv_files, 1):
            print(f"\n▶ [{i}/{len(csv_files)}] Processing: {path.name}")
            if self.process_file(path):
                success_count += 1

        print("\n" + "=" * 60)
        print(f"✅ 배치 완료! (성공: {success_count} / {len(csv_files)})")


def find_data_directory() -> Path:
    """프로젝트 루트의 `data/sample_csv`를 역추적하여 찾습니다."""
    current_path = Path(__file__).resolve()

    for parent in [current_path.parent] + list(current_path.parents):
        target = parent / "data" / "sample_csv"
        if target.exists():
            return target

    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        target = parent / "data" / "sample_csv"
        if target.exists():
            return target

    raise FileNotFoundError("프로젝트 폴더 내에서 'data/sample_csv' 디렉토리를 찾을 수 없습니다.")