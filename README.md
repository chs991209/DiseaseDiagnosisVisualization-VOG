# 1. VOG Data Analysis Pipeline

This project implements a pipeline to parse, analyze, and visualize Vestibulo-Ocular Gaze (VOG) data of CSV files. The primary goal is to assess eye-tracking performance by comparing eye movement against a moving target.

<div align="center">
    <img src="https://github.com/user-attachments/assets/b1fe42e7-5aaf-4612-9c48-7c8d88dec418">
</div>

---

# 2. VOG Data to Spectrograms

### Let's introduce the core process of vog data(tabular time-series) visualization

## 2-1. Time-Series Data Handling 
### - From Target & Actual Eye Position Data to Actual Eye - Target Position Data 

<img width="2149" alt="스크린샷 2026-04-18 오후 1 54 59" src="https://github.com/user-attachments/assets/1979f2df-dd9a-4e0e-9e4d-e1de06015079" />

<br></br>
<p>First, we should get the difference of the patient's target's movement and the patient's eye's movement.
<br>At that, we subtract the position value of the target from the patient's actual eye's position.
<br>It can be thought like why do we subtract the target's one, not the patient's one,
<br>but it's like Prediction Value - Correct Value form of Machine Learning.
    <br></br>
<br>And we get squared value of them at the spectrograms so don't need to worry about that.</p>

## 2-2. Visualizing the Time-Series data
### - Time-Series Data to Spectrograms 
### -- Mean Spectrograms - to see overall distribution of participants' eye movement(Actual Eye- Target) data of tasks.
### The basic goal of this core process

<img width="2532" alt="스크린샷 2026-04-18 오후 2 16 50" src="https://github.com/user-attachments/assets/6ab4a7c6-ef0e-48e8-b7ac-c0ae5f01bc53" />

The goal is to 'see' the movement data with our eyes.
When we need to see what's going on on the time, and which frequency the data's appearing,
<br>we should visualize them, with time, frequency axes and the **movement value through 'Vision'**


<img width="2467" alt="스크린샷 2026-04-18 오후 2 28 12" src="https://github.com/user-attachments/assets/1af81549-7d52-4bd5-9c37-e3faaa37bf74" />

We have a lot of patients in the tasks' data.

%% Lets call the parts of the data as variables and numbers %%

<img width="851" align="center" alt="스크린샷 2026-04-18 오후 2 42 07" src="https://github.com/user-attachments/assets/89daa907-da75-4b57-bd2b-29339958a567" />


<br></br>
<p align="center"> i = patient(id), k = task(type of task-id), G = group(type of group-id)

In the data, there are numbers of tasks done by a lot of patients of each Group.
<br>Participants are departed to HC(health condition), and MCI(Mild Cognitive Impairment) group **(list of G)**.
<br>And each patient **(i)** had done tasks such as Saccade A, Saccade B, Anti Saccade B, Saccade R -- **(list of candidates for k)**.
<r>So the data have **i, k, G**!

<br>And the bellow statements will use x for time, y for frequency
<br><b>So (x, y) is about (time, frequency) space features</b>


#### 2-2-1. Fourier Transform

- We're gonna do Fourier Transformation(Short-term), Calculating Arithmetic Mean and Rendering to dB & Colorization

<img width="1651" align="center" alt="스크린샷 2026-04-18 오후 2 40 36" src="https://github.com/user-attachments/assets/48f9f1d6-74c2-4e22-88d1-cb22d181d159" />

<br></br>
<p align="center">We can get f_i^k value through fourier transform, which transforms the <b>wave(time-series-based) data</b> to <b>(time, frequency)</b>-based data.
<br>And the f_i^k value is for each participant <b>(i)</b></p>

#### 2-2-1-1. Scanning proces & Averaging process of Short-term Fourier Transform

<img width="2356" alt="스크린샷 2026-04-18 오후 3 16 26" src="https://github.com/user-attachments/assets/1143fa57-e225-43fc-92df-ee053b3dff27" />

<br><b>2-2-1-1-1. Scan the TS Data</b>
<br>
<br>The Short-term Fouerier Transform(STFT) does scanning of the data along time axis based direction.
<br>The <b>tau</b> is the variable for scanning the time-series eye movement data, and the scanning is done at each pixel of Spectrogram field,
<br>where you can see the spectrogram being shown on (time, frequency) field.
<br>
<br><b>2-2-1-1-1. Get value with correction factor</b>
<br>
<br>Then we divide the scanned data with <b>correction factor U</b> of window w

<img width="2136" alt="스크린샷 2026-04-18 오후 4 03 47" src="https://github.com/user-attachments/assets/67092d20-8ab9-4774-b44c-9c66cdb50c18" />
<br>
<img width="2425" alt="스크린샷 2026-04-18 오후 4 05 39" src="https://github.com/user-attachments/assets/a02c9514-6d93-4c9b-acb8-f40a8377a13c" />


<img width="2456" align="center" alt="스크린샷 2026-04-18 오후 2 50 41" src="https://github.com/user-attachments/assets/b5528a03-8c42-4dbe-ae2b-ce7f758d0d8d" />

<br></br>
<p align="center"> <b>The final value, which is Mean Spectrogram's data</b></p>

<p><br>We need to see the overall distribution of movement data of tasks by participants' groups,</br> 
<br>so we've done getting mean spectrograms of them first</br>
</p>

- We first do calculate Arithmetic Mean, and then we render it to dB(decibell) unit.

#### 2-2-2. Averaging Position(Actual Eye - Target) data 

<img width="2427" align="center" alt="스크린샷 2026-04-18 오후 3 02 46" src="https://github.com/user-attachments/assets/6facbe41-b879-4bcf-9aad-ccab0cbdaeef" />
<br></br>
<br>We get the calculated arithmetic mean value of the Time-series data,
<br>of each patient i of the group, doing task k</br>
Then we have to do visual transformation of all the data, so it's
<br>done for every task of every group of participant.</br>

Lets get to the next phase.

#### 2-2-3. Rendering Arithmetic Means of Time-Series into dB unit(Visualization target) data

<img width="1449" align="center" alt="스크린샷 2026-04-18 오후 3 08 14" src="https://github.com/user-attachments/assets/8b54c0b6-748f-49eb-8b6f-d27f458923cc" />

<br>The next phase is logarithmization of Arithmetic mean, to generate dB data.
<br>We're getting the mean spectrogram, so we gather all patients <b>(i)</b> participated in each task of group in Averaging process(2-2-2),
<br>and we're lgorithmizing it. Then we can get <b>each task of group's</b> dB data.

#### 2-2-4. Colorization of dB data to pixels' colors

<img width="2267" alt="스크린샷 2026-04-18 오후 3 34 02" src="https://github.com/user-attachments/assets/8696bfd6-2222-4481-bd46-04f0033b2107" />

<br> We need transformation from dB data to pixels' colors.
<br>We can use a bright color to show the strong(high dB) amplitude of the movement's position data,
<br>and use a dark color to show the tiny(low dB) amplitude of them.
<br> Then we use gradient color spectrum to show the difference of the amplitude of the data.

## Final Recap
#### Let's do a final recap for visualization to mean spectrograms process
<img width="2275" alt="스크린샷 2026-04-18 오후 3 42 32" src="https://github.com/user-attachments/assets/523c74a2-fb89-47d8-9c68-7b9cc6296cfa" />

# Getting Difference Maps

### After getting mean spectrograms of experiment data, we can get difference(of HC and MCI) map of experiment

<img width="2509" alt="스크린샷 2026-04-18 오후 3 55 56" src="https://github.com/user-attachments/assets/f28faaff-9d47-4574-b90c-17414cdf3ebb" />



<br>The fourier transformation to dB unit to colorizing is same.
<br> But we get the difference squared for each pixel of spectrogram.
<br> The output spectrograms mean the difference of the HC and MCI group's <b>Actual Eye - Target</b> for each tasks.

<img width="2523" alt="스크린샷 2026-04-18 오후 3 54 47" src="https://github.com/user-attachments/assets/51683954-418d-497c-90e7-cec990c825ea" />

# Getting Variance Maps

### We can get Variance Maps for each group
#### We can see how far the eye movements of each group are from the means of them.
<img width="2446" alt="스크린샷 2026-04-18 오후 3 56 57" src="https://github.com/user-attachments/assets/959f3dba-65d2-46b7-b645-88f87035db38" />

<br> We saw that the MCI patients' variance are vividly high

---
# Additional: Mel Filtering Applied Spectrograms

## Concept of Mel Filtering

<img width="1322" alt="스크린샷 2026-04-18 오후 4 21 02" src="https://github.com/user-attachments/assets/fc42845e-e9c1-4412-8da2-ce4bf4685ffb" />

<br> Mel filtering is to compress the time-series wave data with different density on different frequency.
<br> Human auditory organ is known to handle the audio signal in diverset density,
<br> -- When frequency is high, it compresses a lot.
<br> We cannot identify the difference of the frequency of the signals easily, between high frequencies
<br> -- When frequency is low, it compresses less.
<br> We can identify the difference of it between low frequencies.

<br>
<br> It is known to be caused by the distinguish-point of the meaning of language of voice highly focused on the low frequency signals,
<br> which vowels' frequency range is mostly based on low frequency area.

<br><b>The separation point of the frequency of the voice is mel break point</b>
<br>We can apply that in the Mean spectrograms of (Actual - Target) Movement data,
<br>by assigning appropriate break point of visualization(through mel filtering)
<br> ** Human voice's mel break point is known as 700~1000Hz

<img width="1065" alt="스크린샷 2026-04-18 오후 4 51 09" src="https://github.com/user-attachments/assets/c0a4bf24-f0fc-4b30-9349-29f23785aa16" />

Mel filter can be defined as Overlapping filter <b>on frequency axis's space.</b>

#### 1. Filters
<br> We're gonna filter with M frequencies points, frequency values equally divided in frequency area of Mel filter .

<img width="1506" alt="스크린샷 2026-04-18 오후 4 49 10" src="https://github.com/user-attachments/assets/bd71e52f-3c31-4bb4-8b18-ed5d5025ff1f" />


<br>We define $M$ filters. 
<br>Mel filtering process generates $M+2$ points linearly in the Mel domain between the minimum and maximum frequencies.
<br>This is to ensure uniform perceptual spacing.

#### 2. Inverse Mapping

<img width="679" alt="스크린샷 2026-04-18 오후 4 49 32" src="https://github.com/user-attachments/assets/0453d806-87d8-4249-8222-42bc7c04ebd5" />

<br>We do <b>inverse mapping</b> after that.

<br>The grid points are mapped back to the physical frequency domain (Hz). 
<br>The esults in non-linear spacing in Hz; the gaps between points increase logarithmically.
<br>It's an important point of Mel filtering

#### Mel filter's Trigometric Function
<br> Then it's the trigometric function of mel filter
<img width="1065" alt="스크린샷 2026-04-18 오후 4 51 09" src="https://github.com/user-attachments/assets/cc5b6b3d-e38e-47f6-a9f4-6a1068c65eb1" />

<br><b>When we project the Actual Eye- Target movement data with Mel filter, we can see mel filtered spectrograms.</b>
<img width="958" alt="스크린샷 2026-04-18 오후 4 54 07" src="https://github.com/user-attachments/assets/d234f3b0-2efd-48a7-905c-5ad6d8465b47" />

### We can get Mean Strograms with Mel Filters

<img width="1165" alt="스크린샷 2026-04-18 오후 4 55 57" src="https://github.com/user-attachments/assets/25e6fe85-140f-4f5d-a193-fcf327600b92" />

### Squared Difference Map with Mel Filters

<img width="1157" alt="스크린샷 2026-04-18 오후 4 56 14" src="https://github.com/user-attachments/assets/3b14c3ef-774c-44de-a602-7d479c6c851c" />

### Variance Map with Mel Filters

<img width="1455" alt="스크린샷 2026-04-18 오후 4 59 07" src="https://github.com/user-attachments/assets/e2a45696-6287-42ea-bbde-8aeaf8b39672" />


---

## 1-1. Navigating the Core Analysis Logic

To efficiently understand the data processing pipeline **before** diving into the main executor code (e.g., `src/app/main_app.py`), we recommend reviewing the key methods within the `src/` directory in the specified order. These three methods represent the foundational stages of the analysis.

---



## Data Tree

#### Data should be like this below

<details>
<summary>📂 Click to expand the Data Directory Tree</summary>

```text
data/
└── sample_csv
    ├── HC_csv_24_25
    │   ├── 20240329_084111_1324721_
    │   │   ├── PD VOG -_Horizontal Saccade A.csv
    │   │   ├── PD VOG -_Horizontal Saccade B (anti).csv
    │   │   ├── PD VOG -_Horizontal Saccade B.csv
    │   │   ├── PD VOG -_Horizontal Saccade R.csv
    │   │   ├── PD VOG -_Vertical Saccade A.csv
    │   │   ├── PD VOG -_Vertical Saccade B (anti).csv
    │   │   ├── PD VOG -_Vertical Saccade B.csv
    │   │   └── PD VOG -_Vertical Saccade R.csv
    │   ├── 20240329_094040_1073209_
    │   ...
    └── MCI_csv_25_26
        ├── 20250701_091148_644377_
        │   ├── PD VOG -_Horizontal Gaze Left30, 20sec.csv
        │   ├── PD VOG -_Horizontal Gaze Right30, 20sec.csv
        │   ├── PD VOG -_Horizontal Saccade A.csv
        │   ├── PD VOG -_Horizontal Saccade B (anti).csv
        │   ├── PD VOG -_Horizontal Saccade B.csv
        │   ├── PD VOG -_Horizontal Saccade R.csv
        │   ├── PD VOG -_Vertical Gaze  Down15, 20sec.csv
        │   ├── PD VOG -_Vertical Gaze  Up15, 20sec.csv
        │   ├── PD VOG -_Vertical Saccade A.csv
        │   ├── PD VOG -_Vertical Saccade B (anti).csv
        │   ├── PD VOG -_Vertical Saccade B.csv
        │   └── PD VOG -_Vertical Saccade R.csv
```
</details>

# (Linear) Mean Spectrograms

### Mean of Actual Eye 
#### - Target movement data, on (time, frequency) space, window size = 24

<img width="5180" alt="Mean_Spectrograms_Linear" src="https://github.com/user-attachments/assets/742b0d69-0bc9-4e6b-a535-bddc1a2341fe" />


# (Mel) Mean Spectrograms

### Mean of Actual Eye - Target movement data, on (time, frequency) space,
#### filtered with Mel filter, mel break = 20Hz, window size = 24


<img width="5180" alt="Mean_Spectrograms_Mel" src="https://github.com/user-attachments/assets/fb534e2c-b9b6-429e-a2d5-e70d0cba3310" />


# (Linear) Squared Difference Map Spectrograms

### Differnce between HC and MCI group for each task
#### window size = 24

<img width="5180" alt="Difference_Maps_Linear" src="https://github.com/user-attachments/assets/79e06fdf-f287-4912-95a7-9b25e236559b" />


# (Mel) Squared Difference Map Spectrograms

### Differnce between HC and MCI group for each task
#### mel break = 20Hz, window size = 24

<img width="5180" alt="Difference_Maps_Mel" src="https://github.com/user-attachments/assets/eac6fac9-502b-4afa-8fe5-ed546360d585" />


# (Linear) Variance Map Spectrograms

### Variance in each task in each group
#### window size = 24

<img width="5180" alt="Variance_Maps_Linear" src="https://github.com/user-attachments/assets/04a43b5b-2680-4cfd-b1af-2503aaae9459" />


# (Mel) Variance Map Spectrograms

### Variance in each task in each group
#### mel break = 20Hz, window size = 24

<img width="5180" alt="Variance_Maps_Mel" src="https://github.com/user-attachments/assets/7cd1925f-0321-4436-bee4-8f3940124fbb" />

