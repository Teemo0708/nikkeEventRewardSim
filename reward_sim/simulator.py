import os
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from matplotlib.ticker import FuncFormatter

# 한글 폰트 설정 (Windows 기본: 맑은 고딕)
try:
    font_manager.fontManager.addfont(r"C:\Windows\Fonts\malgun.ttf")   # 일반체
    font_manager.fontManager.addfont(r"C:\Windows\Fonts\malgunbd.ttf") # 볼드체
    rcParams["font.family"] = "Malgun Gothic"                          # 전체 폰트 지정
except Exception:
    rcParams["font.family"] = "Malgun Gothic"                          # 실패 시 기본 설정
rcParams["axes.unicode_minus"] = False                                 # 마이너스 깨짐 방지

# 고정 파라미터
BONUS_PER_BATTLE = 50      # 전투 1회 성공 시 얻는 보너스 재화
DAYS = 28                  # 이벤트 진행일 수
BATTLES_PER_DAY = 5        # 하루 전투 횟수
TRIALS = DAYS * BATTLES_PER_DAY  # 전체 전투 횟수 = 28 * 5 = 140
N_SIM = 10000              # 시뮬레이션 반복 횟수
OUTPUT_DIR = "reward_hists" # 결과 그래프 저장 폴더명

def simulate_rewards_array(prob_percent, n_sim=N_SIM): 
    p = prob_percent / 100.0                                # %를 0~1 확률로 변환
    successes = np.random.binomial(TRIALS, p, size=n_sim)   # 이항분포: 140회 전투 중 성공 횟수 샘플링
    rewards = successes * BONUS_PER_BATTLE                  # 총 보상 = 성공 횟수 × 보너스 개수(50)
    return rewards                                          # 시뮬레이션 결과 배열 반환

def summarize_rewards(prob_percent, rewards): 
    return {
        "확률(%)": prob_percent,                             # 입력 확률
        "평균 보상": float(np.mean(rewards)),                # 실험 평균값
        "표준편차": float(np.std(rewards, ddof=0)),          # 분포의 퍼짐 정도
        "최소": int(np.min(rewards)),                        # 최소 보상값
        "최대": int(np.max(rewards)),                        # 최대 보상값
    }

def plot_and_save_hist(prob_percent, rewards, expected, out_dir=OUTPUT_DIR): 
    os.makedirs(out_dir, exist_ok=True)                      # 결과 저장 폴더 생성
    ts = time.strftime("%Y%m%d-%H%M%S")                      # 저장 파일에 타임스탬프 부여
    filename = f"reward_hist_{prob_percent}pct_{ts}.png"     # 파일명 구성
    save_path = os.path.join(out_dir, filename)

    fig, ax = plt.subplots()                                 # 그래프 객체 생성
    ax.hist(rewards, bins=30, color="lightgray", edgecolor="black")  # 보상 분포 히스토그램

    mean_val = np.mean(rewards)                              # 실험 평균
    ax.axvline(mean_val, color="red", linewidth=2.5, linestyle="--", label="실험 평균") # 빨간 점선

    ax.axvline(expected, color="blue", linewidth=1.5, linestyle="-", label="이론 기대값") # 파란 실선

    ax.ticklabel_format(style="plain", axis="x", useOffset=False)    # 오프셋 제거
    ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, pos: f"{x:,.0f}")) # 천단위 콤마

    if np.allclose(rewards, rewards[0]):                    # 모든 값이 동일할 경우 (예: 100% 확률)
        center = rewards[0]
        pad = max(50, center * 0.01)                        # 중심값 ±1% 여백
        ax.set_xlim(center - pad, center + pad)

    ax.set_title(f"보상 분포 히스토그램 - 성공확률 {prob_percent}%") # 그래프 제목
    ax.set_xlabel("총 보상량")                               # X축 라벨
    ax.set_ylabel("빈도수")                                  # Y축 라벨
    ax.legend()                                             # 범례 표시

    plt.savefig(save_path, bbox_inches="tight")              # 그래프 저장
    plt.close()                                              # 메모리 해제
    return save_path                                         # 저장 경로 반환
