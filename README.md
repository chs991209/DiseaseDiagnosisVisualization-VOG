# 👁️ VOG Spectrogram Analysis Pipeline

Video Oculography (VOG) 시계열 데이터를 스펙트로그램으로 변환하여 정상군(HC)과 경도인지장애(MCI) 환자군 간의 **임상적 바이오마커(Biomarker)**를 추출하는 신호 처리 및 데이터 분석 파이프라인입니다.

## 📌 1. Project Overview

이 파이프라인은 안구 운동의 미세한 지연(Hesitation)과 떨림(Tremor)을 주파수 도메인에서 포착합니다. 단순한 데이터 집계를 넘어, 수학적 오류를 방지하고 도메인 지식(Domain Knowledge)을 결합하여 딥러닝 모델의 어텐션 마스크(Attention Mask)를 찾아내는 탐색적 데이터 분석(EDA) 시스템입니다.

## ⚙️ 2. Core Architecture

데이터의 신뢰도를 극대화하기 위해 다음 3가지 핵심 아키텍처 패턴이 적용되었습니다.

### 2-1. Linear Space Averaging (기하 평균 함정 제거)

에러 신호를 dB(로그) 스케일로 선행 변환하여 평균을 낼 경우 극단값이 상쇄되는 문제를 해결합니다. 원본 선형 전력(Linear Power) 상태에서 산술 평균을 계산한 뒤 최종 렌더링에만 dB를 적용하여 병리적 에러 에너지를 온전히 보존합니다.

### 2-2. Difference Map Generation ($(MCI-HC)^2$)

두 집단의 평균 스펙트로그램 차이를 제곱 연산하여 노이즈를 억제하고 임상적 차이(Magnitude)만을 붉고 노랗게 폭발(Highlight)시킵니다.

### 2-3. Domain-Driven Routing (도메인 주도 설계)

Anti-saccade 태스크의 정답 좌표를 자동 반전(* -1)하여 순수 '인지 억제 실패율'을 도출하며, 수평/수직 태스크에 따라 분석 축(Axis)을 동적으로 전환하여 가비지 데이터를 차단합니다.

## 🎛️ Tunable Hyperparameters

<img width="1284" height="485" alt="스크린샷 2026-04-17 오후 1 00 09" src="https://github.com/user-attachments/assets/b28812da-a68c-40fa-bfe7-4d904889d031" />


## 📊 Outputs

파이프라인 실행 시 2D 이미지 대시보드와 함께, 의료진의 통계적 가설 검정(Hypothesis Testing)을 지원하기 위한 정량적 데이터(CSV)가 추출됩니다.

### 1. Quantitative Metrics (CSV)

경로: data/quantitative_results/spectrogram_quantitative_means.csv

설명: 2D 스펙트로그램 텐서에서 임상적으로 의미 있는 스칼라(Scalar) 지표들을 추출하여 다차원 피벗(Pivot) 테이블 형태로 제공합니다.

## 📂 CSV Data Dictionary (컬럼 정의서)

<img width="1285" height="670" alt="스크린샷 2026-04-17 오후 1 00 22" src="https://github.com/user-attachments/assets/51ae8a89-e30e-4767-a5c1-9d7a7455afc2" />


### 2. Comprehensive Visual Dashboards (PNG)

  -경로: img/visualization/difference_maps/ 등

  -설명: HC vs MCI 집단의 32-Panel 통합 뷰(수직/수평 결합) 및 어텐션 분석을 위한 Difference Map 대시보드를 생성합니다.

## 🚀 Quick Start
```
from mean_spectrogram_aggregator_cells import MeanSpectrogramAggregator
from pathlib import Path

# 1. 파이프라인 초기화 및 하이퍼파라미터 튜닝
aggregator = MeanSpectrogramAggregator(
    fs=120.0,
    target_fs=60.0,      # 다운샘플링 레이트
    nperseg=64,          # 윈도우 사이즈
    noverlap=24,         # 오버랩 (37.5% Sweet Spot)
    max_freq=30.0        # 관심 주파수 상한선
)

# 2. 데이터 적재 및 시간축 정규화
TARGET_DIR = Path("data/sample_csv")
aggregator.process_directory(TARGET_DIR)

# 3. 정량적 지표 추출 및 시각화 대시보드 저장
df_metrics = aggregator.export_quantitative_metrics(save_dir="data/quantitative_results")
aggregator.plot_and_save_comprehensive_dashboard()
aggregator.plot_and_save_difference_maps()
```
---
