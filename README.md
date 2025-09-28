# 📘 **니케 이벤트 보상 시뮬레이터** (NIKKE Event Reward Simulator)

🔎 **개요**

본 프로그램은 [승리의 여신: 니케] 이벤트 추가 보상 시스템을 분석하기 위해 제작된 시뮬레이터입니다.

전투 승리 시 확률에 따라 지급되는 추가 보상(50개) 을 기준으로,

28일 × 하루 5회 = 총 140회 전투를 가정하여

사용자가 입력한 성공 확률(%)별 추가 보상 획득량을 시뮬레이션합니다.

시뮬레이션은 난수 기반으로 이루어지며, 평균·표준편차·최소·최대 보상량과 분포 히스토그램을 제공합니다.
</br></br></br>
⚙️ **고정 파라미터**

**변수명** /	값 /	설명

**BONUS_PER_BATTLE** / 	50 /	전투 1회 성공 시 보상량

**DAYS** /	28 /	이벤트 진행 일수

**BATTLES_PER_DAY** /	5 /	하루 전투 횟수

**TRIALS** /	140 /	전체 전투 횟수 (= 28 × 5)

**N_SIM** /	10000 /	시뮬레이션 반복 횟수
</br></br></br>
📂 **주요 파일**

      main.py
      
      여러 확률 구간(100%, 90%, …, 0%)을 한 번에 시뮬레이션.
      
      콘솔에 결과를 출력하고, 히스토그램 이미지를 reward_hists/ 폴더에 저장.
      
      gui.py
      
      Tkinter 기반 GUI 실행.
      
      사용자가 입력한 확률(%)에 대한 결과를 즉시 텍스트와 그래프로 표시.
      
      붉은 점선(실험 평균), 푸른 실선(이론 기대값, 30% 두껍게)을 함께 확인 가능.
      
      reward_sim/ (패키지 폴더)
      
      reward_sim.py : 시뮬레이션 및 통계 함수 정의
      
      __init__.py : 패키지 초기화
</br></br></br>
▶ 실행 방법
1. 가상환경 생성 및 실행

      python -m venv env
  
      source env/bin/activate     # macOS/Linux
  
      env\Scripts\activate        # Windows(cmd)

2. 의존성 설치

    pip install -r requirements.txt
  
  
      requirements.txt 
  
      numpy
      matplotlib

3. 콘솔 버전 실행

      python main.py


      여러 확률 구간(100~0%) 결과가 콘솔에 표시되고,
      
      reward_hists/ 폴더에 히스토그램 PNG 파일이 생성됩니다.
      
4. GUI 버전 실행

      python gui.py
      
      
      Tkinter GUI 창 실행
      
      확률(%) 입력 후 [시뮬레이션 실행] 버튼 클릭 → 결과 및 그래프 표시
</br></br></br>
      📊 예시 결과 (60% 확률)
      
      <img width="623" height="519" alt="image" src="https://github.com/user-attachments/assets/c7410c05-790b-496a-8863-b2e0007f43d0" />
</br></br></br>
🎯 기대 효과

데이터 기반 기획 검증 : 보상 확률 설계가 실제 유저 경험에 주는 영향을 직관적으로 확인

신규 유저 분석 : 기본 캐릭터만 사용했을 때 기대 보상량과 상점 구매 가능성을 수치적으로 분석

기획 현장 활용성 :

main.py → 보고서/분석 자료 생성

gui.py → 회의/토론 중 빠른 시뮬레이션 확인

