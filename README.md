# Step 2: Variance Map Architecture

VOG 스펙트로그램 탐색적 데이터 분석(EDA) 파이프라인의 핵심 확장 레이어인 <b>분산 맵(Variance Map)</b>의 아키텍처 설계, <br>임상적 해석 가이드, 그리고 시스템 엔지니어링 구현 상세 명세서

## 💡 1. Why Variance? (아키텍처 설계 배경)

단순한 평균(Mean, 1st Moment) 분석의 한계를 극복하고, 환자군 내부의 <b>구조적 불안정성(Structural Instability)</b>을 시각화하기 위해 데이터의 퍼짐 정도(Variance, 2nd Moment)를 도입했습니다.

- <b>평균(Mean)의 한계</b>: 환자군의 평균 에너지가 높다는 것은 '전반적인 에러'가 크다는 뜻이지만, 모든 환자가 골고루 못하는 것인지 일부가 극단적으로 못하는 것인지 설명하지 못합니다.

- <b>분산(Variance)의 해결책</b>: 특정 환자 집단(Group) 내 행동의 **불일치성(Inconsistency)과 이질성(Heterogeneity)**을 수학적으로 증명하는 핵심 지표로 작용합니다.

## 🏥 2. Clinical Significance (임상적 해석 가이드)

픽셀별 분산을 구하여 magma 컬러맵으로 렌더링한 스펙트로그램은 집단 간의 극명한 차이를 보여줍니다.

🟢 <b>건강한 대조군 (HC, Healthy Control)</b>

- 타겟 추적 패턴이 일관적이고 편차가 적음.

- <b>Visual</b>: 분산 맵 전체가 **차갑고 어두운 색(검은색/보라색)**으로 렌더링.

🔴 <b>경도인지장애 (MCI, Mild Cognitive Impairment)</b>

- 환자마다 인지/운동 제어 능력 붕괴 양상이 제각각임 (심한 머뭇거림 vs 강한 안구 떨림 등).

- <b>Visual</b>: 극심한 환자 간 편차로 인해 분산 에너지가 폭발하며, <b>뜨겁고 밝은 색(노란색/흰색)</b>으로 렌더링.

## 🛠️ 3. Code Implementation Details (구현 상세)

plot_and_save_variance_maps 메서드는 수학적 왜곡과 메모리 누수를 방지하기 위해 4가지 핵심 소프트웨어 공학 패턴을 따릅니다.

#### 🔹 3.1. 32-Panel 통합 뷰 (View Architecture)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;수평(H)/수직(V) 궤적 및 좌/우 안구를 하나의 그리드로 결합하여 <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;상하(HC vs MCI) 비교가 즉각적으로 이루어지도록 UX를 설계했습니다.

#### 🔹 3.2. 방어적 프로그래밍 (Defensive Programming)
```
if len(tensors) < 2:
    ax.axis('off')
    continue
```
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;분산은 최소 2개의 데이터가 필요합니다. 조건에 맞는 환자 데이터가 부족할 경우 런타임 크래시를 막는 필수적인</br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>가드 클로즈(Guard Clause)</b>가 적용되어 있습니다.

#### 🔹 3.3. 수학적 보정: Linear to Log Transformation
```
# 1. 선형 공간에서 픽셀별 분산 계산 (필수)
variance_tensor_linear = np.var(tensors, axis=0)

# 2. Log(dB) 매핑 및 런타임 에러 방어
variance_tensor_db = 10 * np.log10(np.clip(variance_tensor_linear, a_min=1e-10, a_max=None))
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⚠️ 데시벨(dB) 변환을 분산 연산 전에 수행하면 환자 간 에너지 격차가 왜곡됩니다.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;반드시 원본 선형 공간(Linear Power)에서 분산을 구한 뒤 dB 매핑을 수행합니다.

#### 🔹 3.4. 컬러맵 엔지니어링 (Color-Mapping)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;에러 불안정성의 '폭발'을 시각적으로 극대화하기 위해 viridis(평균 맵)와 구분되는 magma 컬러맵을 채택했습니다. 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;노이즈는 검게 숨기고 높은 분산값만 발광(Highlight)시킵니다.

## 📈 4. Quantitative Metrics Evolution (정량적 지표 변동 분석)

파이프라인이 고도화되면서 CSV로 추출되는 정량 수치(Overall_Mean_dB, Peak_Power_dB 등)에 변화가 발생했습니다. 
이는 STFT 윈도우 크기나 파라미터의 변동이 아닌, <b>평균을 산출하는 '수학적 공간'을 교정하면서 나타난 완벽하게 정상적이고 의도된 시프트(Shift)</b>입니다.

<img width="1327" height="385" alt="image" src="https://github.com/user-attachments/assets/e7f9738e-0e0b-432e-b5f3-866ea49b04d2" />


#### 📌 5. Conclusion:
모든 파라미터(noverlap=48 등)가 동일하게 통제된 상태에서 발생한 이 수치적 차이는, <br><b>"Log 스케일 평균이 MCI 환자의 에러(Outlier)를 상쇄시키고 있었다"</b>는 초기 가설을 입증하는 완벽한 수학적 증거입니다.
<br>
<br>실험의 Ground Truth로 Linear-space 기반의 현 branch 기반의 CSV 데이터를 활용해야 함.
