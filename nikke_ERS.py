import matplotlib
matplotlib.use("Agg")  # 창을 띄우지 않고 파일로만 저장

import os
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

# 한글 폰트 설정 (Windows: 맑은 고딕)
try:
    font_manager.fontManager.addfont(r"C:\Windows\Fonts\malgun.ttf")
    font_manager.fontManager.addfont(r"C:\Windows\Fonts\malgunbd.ttf")
    rcParams["font.family"] = "Malgun Gothic"
except Exception:
    # 경로 이슈 시, 시스템에 설치된 폰트 이름만으로도 시도
    rcParams["font.family"] = "Malgun Gothic"
rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지

# 고정 파라미터
BONUS_PER_BATTLE = 50
DAYS = 28
BATTLES_PER_DAY = 5
TRIALS = DAYS * BATTLES_PER_DAY  # 140회
N_SIM = 10000                   # 시뮬레이션 반복
OUTPUT_DIR = "reward_hists"     # 이미지 저장 폴더

# (선택) 재현성 확보
# np.random.seed(42)

# 시뮬레이션, 전투 1회 성공확률(%)에 대해 총 보상량 배열(n_sim개)을 반환
def simulate_rewards_array(prob_percent, n_sim=N_SIM):
    p = prob_percent / 100.0

    # 성공 횟수 ~ Binomial(n=TRIALS, p=p)
    successes = np.random.binomial(TRIALS, p, size=n_sim)
    rewards = successes * BONUS_PER_BATTLE
    return rewards

# 보상 배열로부터 요약 통계 산출 (평균, 표준편차, 최소, 최대)
def summarize_rewards(prob_percent, rewards):
    return {
        "확률(%)": prob_percent,
        "평균 보상": float(np.mean(rewards)),
        "표준편차": float(np.std(rewards, ddof=0)),  # 모표준편차
        "최소": int(np.min(rewards)),
        "최대": int(np.max(rewards)),
    }

def plot_and_save_hist(prob_percent, rewards, expected, out_dir=OUTPUT_DIR):
    """
    히스토그램 + 실험 평균(빨간 점선) + 이론 기대값(파란 실선)
    선 겹침 방지 스타일 적용 + 텍스트 레이블 표시
    """
    os.makedirs(out_dir, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    filename = f"reward_hist_{prob_percent}pct_{ts}.png"
    save_path = os.path.join(out_dir, filename)

    plt.figure()
    plt.hist(rewards, bins=30, color="lightgray", edgecolor=None)  # 막대는 회색 계열로

    # 실험 평균선
    mean_val = np.mean(rewards)
    plt.axvline(mean_val, color="red", linewidth=2.5, linestyle="--", label="실험 평균")
    plt.text(mean_val, plt.ylim()[1]*0.9, "", color="red",
             rotation=90, va="top", ha="right", fontsize=9)

    # 이론 기대값선
    plt.axvline(expected, color="blue", linewidth=1.5, linestyle="-", label="이론 기대값")
    plt.text(expected, plt.ylim()[1]*0.9, "", color="blue",
             rotation=90, va="top", ha="left", fontsize=9)

    # 제목/축/범례
    plt.title(f"보상 분포 히스토그램 - 성공확률 {prob_percent}%")
    plt.xlabel("총 보상량")
    plt.ylabel("빈도수")
    plt.legend()

    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    return save_path

# 실행부
if __name__ == "__main__":
    prob_list = [100, 90, 80, 70, 60, 50, 40, 30, 20, 0]

    print("=== 추가 보상 시뮬레이션 (난수 기반 / 저장 전용) ===")
    saved_files = []

    for prob in prob_list:
        # 시뮬레이션
        rewards = simulate_rewards_array(prob, n_sim=N_SIM)
        stats = summarize_rewards(prob, rewards)

        # 요약 출력
        print(f"[{stats['확률(%)']}%] "
              f"평균={stats['평균 보상']:.1f}, "
              f"표준편차={stats['표준편차']:.1f}, "
              f"최소={stats['최소']}, "
              f"최대={stats['최대']}")

        # 이론 기대값(평균)
        expected = TRIALS * (prob / 100.0) * BONUS_PER_BATTLE

        # 저장 전용 히스토그램
        path = plot_and_save_hist(prob, rewards, expected, out_dir=OUTPUT_DIR)
        saved_files.append(path)

    print("\n[저장된 파일]")
    for p in saved_files:
        print(" -", p)
