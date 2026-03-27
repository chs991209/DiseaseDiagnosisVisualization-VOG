import sys
from pathlib import Path

# 파이썬 모듈 시스템의 절대 경로 임포트를 보장하기 위해 src 디렉토리를 PATH에 주입
current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from src.Parser.data_parser import VOGRobustParser
from src.Analyzer.vog_data_analyzer import VOGDomainAnalyzer
from src.Visualizer.visualizer import VOGMatplotlibVisualizer


class VOGPipelineFacade:
    def __init__(self, parser=None, analyzer=None, visualizer=None):
        # 의존성 주입(DI) 또는 기본 객체 생성
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

        # 재귀적 탐색 (HC_csv_24_25, MCI_csv_25_26 등 하위 구조를 모두 스캔)
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
    """
    현재 스크립트의 위치와 무관하게 프로젝트 루트의 `data/sample_csv`를 역추적하여 찾습니다.
    (src/app/ 에서 실행하든 VOGVisualization/ 에서 실행하든 안전하게 동작)
    """
    current_path = Path(__file__).resolve()

    # 상위 부모 폴더들을 순회하며 탐색
    for parent in [current_path.parent] + list(current_path.parents):
        target = parent / "data" / "sample_csv"
        if target.exists():
            return target

    # Jupyter Notebook 등 __file__ 속성이 없는 환경을 위한 Fallback
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        target = parent / "data" / "sample_csv"
        if target.exists():
            return target

    raise FileNotFoundError("프로젝트 폴더 내에서 'data/sample_csv' 디렉토리를 찾을 수 없습니다.")

