import tkinter as tk
from reward_sim import simulate_rewards_array, summarize_rewards, TRIALS, BONUS_PER_BATTLE
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def run_simulation():
    try:
        prob = int(entry_prob.get())  # 입력 확률 (%)
        if not (0 <= prob <= 100):
            raise ValueError("확률은 0~100 사이여야 합니다.")

        rewards = simulate_rewards_array(prob, n_sim=10000)
        stats = summarize_rewards(prob, rewards)
        expected = TRIALS * (prob / 100.0) * BONUS_PER_BATTLE

        # 결과 텍스트 갱신
        msg = (
            f"[{stats['확률(%)']}%]\n"
            f"평균={stats['평균 보상']:.1f} | 표준편차={stats['표준편차']:.1f}\n"
            f"최소={stats['최소']} | 최대={stats['최대']}\n"
            f"이론 기대값={expected:.1f}"
        )
        result_text.set(msg)

        # 그래프 갱신
        for widget in frame_graph.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 3.6))
        ax.hist(rewards, bins=30, color="lightgray", edgecolor="black")

        mean_val = np.mean(rewards)
        # zorder로 항상 파랑 뒤 → 빨강 앞
        ax.axvline(expected, color="blue", linestyle="-", linewidth=2.6,
                   label="이론 기대값", zorder=1)
        ax.axvline(mean_val, color="red", linestyle="--", linewidth=2,
                   label="실험 평균", zorder=2)

        ax.set_title(f"보상 분포 히스토그램 ({prob}%)")
        ax.set_xlabel("총 보상량")
        ax.set_ylabel("빈도수")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        plt.close(fig)

    except Exception as e:
        result_text.set(f"에러: {e}")

def on_close():
    for widget in frame_graph.winfo_children():
        widget.destroy()
    root.destroy()

# UI 구성
root = tk.Tk()
root.title("보상 시뮬레이터 (즉시 결과/그래프)")
root.protocol("WM_DELETE_WINDOW", on_close)

frame_input = tk.Frame(root)
frame_input.pack(fill="x", padx=10, pady=8)

tk.Label(frame_input, text="성공 확률 (%)").pack(side="left")
entry_prob = tk.Entry(frame_input, width=8)
entry_prob.insert(0, "60")
entry_prob.pack(side="left", padx=6)

tk.Button(frame_input, text="시뮬레이션 실행", command=run_simulation).pack(side="left", padx=6)

result_text = tk.StringVar(value="확률을 입력하고 실행을 눌러주세요.")
label_result = tk.Label(root, textvariable=result_text, justify="left", anchor="w")
label_result.pack(fill="x", padx=10, pady=(0, 8))

frame_graph = tk.Frame(root, width=600, height=360, bd=1, relief="sunken")
frame_graph.pack(fill="both", expand=True, padx=10, pady=(0, 10))

root.mainloop()
