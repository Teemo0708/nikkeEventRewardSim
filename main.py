import csv
from reward_sim import (                   # reward_sim 패키지에서 함수/상수 불러오기
    simulate_rewards_array,                # 시뮬레이션 함수
    summarize_rewards,                     # 요약 통계 함수
    plot_and_save_hist,                    # 히스토그램 저장 함수
    TRIALS,                                # 총 전투 횟수 (28일 * 5회 = 140)
    BONUS_PER_BATTLE,                      # 전투 1회 성공 시 보상 개수 (50)
    N_SIM,                                 # 시뮬레이션 반복 횟수 (기본 10,000)
)

if __name__ == "__main__":                 # 프로그램 실행 시작점
    prob_list = [100, 90, 80, 70, 60, 50, 40, 30, 20, 0]  # 테스트할 확률 목록

    print("=== 추가 보상 시뮬레이션 (난수 기반 / 저장 전용) ===")
    saved_files = []                       # 저장된 파일 경로 모아둘 리스트
    stats_list = []                        # CSV 저장용 데이터 리스트

    for prob in prob_list:                 # 각 확률에 대해 시뮬레이션 실행
        rewards = simulate_rewards_array(prob, n_sim=N_SIM)  # 총 보상 배열 생성
        stats = summarize_rewards(prob, rewards)             # 통계 요약값 계산

        # 콘솔 출력 (평균, 표준편차, 최소, 최대)
        print(f"[{stats['확률(%)']}%] "
              f"평균={stats['평균 보상']:.1f}, "
              f"표준편차={stats['표준편차']:.1f}, "
              f"최소={stats['최소']}, "
              f"최대={stats['최대']}")

        expected = TRIALS * (prob / 100.0) * BONUS_PER_BATTLE  # 이론 기대값 계산
        path = plot_and_save_hist(prob, rewards, expected)     # 히스토그램 저장
        saved_files.append(path)                              # 저장된 파일 경로 기록

        stats_list.append({**stats, "이론 기대값": expected, "히스토그램 파일": path})

    # 저장된 파일 목록 출력
    print("\n[저장된 파일]")
    for p in saved_files:
        print(" -", p)

    # CSV 저장
    csv_filename = "reward_stats.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["확률(%)", "평균 보상", "표준편차", "최소", "최대", "이론 기대값", "히스토그램 파일"])
        writer.writeheader()
        writer.writerows(stats_list)

    print(f"\n[CSV 저장 완료] {csv_filename}")
