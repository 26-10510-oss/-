import streamlit as st
import pandas as pd
import numpy as np

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="스마트폰 배터리 심폐소생 플래너",
    page_icon="🔋",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title { font-size: 2.1rem; font-weight: 800; color: #1E3A8A; }
    .sub-title { font-size: 1.1rem; color: #4B5563; margin-bottom: 20px; }
    .action-card { background-color: #FEF3C7; border-left: 5px solid #F59E0B; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .success-card { background-color: #D1FAE5; border-left: 5px solid #10B981; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .solution-card { background-color: #EFF6FF; border-left: 5px solid #3B82F6; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    .graph-explain { background-color: #F3F4F6; padding: 15px; border-radius: 8px; margin-top: 10px; border: 1px solid #E5E7EB; }
    </style>
""", unsafe_allow_html=True)

# 2. 메인 타이틀 및 소개
st.markdown('<div class="main-title">🔋 스마트폰 배터리 심폐소생 플래너</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">내 습관대로 쓰면 언제 폰이 조기 사망할까? 실질적인 교체 타이밍 진단!</div>', unsafe_allow_html=True)

with st.expander("💡 화학공학으로 보는 배터리 이야기 (클릭해보세요!)"):
    st.markdown("""
    * **배터리도 열을 받으면 늙어요:** 스마트폰 배터리는 다양한 **화학 물질**로 채워져 있습니다. 온도가 높아지면 배터리 내부의 불필요한 화학 반응이 빨라져 수명이 급격히 줄어듭니다.
    * **100% 완충과 0% 방전은 배터리의 스트레스:** 배터리에 전기를 꽉 채우거나 완전히 비워 두면, **양극과 음극의 전극 소재**가 찌그러지거나 망가질 위험이 커집니다.
    * **급속 충전과 발열:** 너무 빠르게 전기를 넣으면 열이 발생하여 배터리 건강을 해칠 수 있습니다.
    """)

st.markdown("---")

# 3. 입력 폼 (학생 체크리스트)
st.subheader("📋 1. 나의 스마트폰 상태 & 습관 체크")

with st.form("student_battery_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### 📱 기기 기본 정보 & 충전")
        current_soh = st.slider("현재 내 폰의 배터리 성능 상태 (%)", min_value=50, max_value=100, value=95, help="아이폰: 설정 > 배터리 > 성능 상태 / 안드로이드: 설정 > 배터리 참고")
        
        charge_range = st.selectbox(
            "주로 몇 %에서 충전기를 꽂고 뽑나요?",
            [
                "20% ~ 80% 구간 유지 (가장 이상적)",
                "20%에서 100%까지 채우고 바로 뽑음",
                "매일 밤 100% 상태로 자는 동안 계속 꽂아둠",
                "0%가 되어 폰이 꺼질 때까지 썼다가 충전함"
            ]
        )
        
        charger_type = st.radio(
            "어떤 충전기를 자주 사용하나요?",
            ["일반 / 정품 기본 충전기", "초고속 / 초급속 충전기"]
        )

    with col2:
        st.markdown("##### 🔥 발열 및 사용 환경")
        temp_env = st.selectbox(
            "어떤 환경에서 스마트폰을 자주 쓰나요?",
            ["평범한 실내 (15℃~25℃)", "겨울철 추운 야외", "여름철 차 안, 핫팩 옆처럼 뜨거운 곳"]
        )
        
        charge_gaming = st.selectbox(
            "충전기 케이블을 꽂은 채 폰을 사용하나요?",
            ["전혀 안 함 (충전할 땐 폰을 둡니다)", "가끔 카톡이나 웹서핑 정도만 함", "자주 고사양 게임을 하거나 영상을 봄"]
        )
        
        case_type = st.radio(
            "충전할 때 두꺼운 케이스(두꺼운 범퍼 등)를 끼워두나요?",
            ["아니오 / 얇은 케이스", "네, 두꺼운 케이스를 낀 채 충전함"]
        )

    with col3:
        st.markdown("##### ⚙️ 기능 및 설정 상태")
        discharge_zero = st.selectbox(
            "배터리가 0%가 되어 폰이 꺼진 적이 얼마나 자주 있나요?",
            ["어쩌다 한 번 / 거의 없음", "한 달에 2~3번 정도", "일주일에 1번 이상 (자주 꺼짐)"]
        )
        
        screen_brightness = st.selectbox(
            "평소 화면 밝기 및 화면 유지 설정은?",
            ["자동 밝기 사용 (권장)", "항상 80% 이상 밝게 유지", "화면 켜짐 시간을 길게 설정함"]
        )
        
        battery_protection = st.radio(
            "스마트폰의 '배터리 보호(80~85% 제한)' 기능 설정",
            ["네, 켜두었습니다", "아니오 / 잘 모르겠습니다"]
        )

    submitted = st.form_submit_button("🧪 내 배터리 수명 진단하기")

# 4. 시뮬레이션 및 데이터 처리
if submitted:
    # 가중치 계산
    temp_factor = 2.0 if "뜨거운 곳" in temp_env else (1.2 if "추운" in temp_env else 1.0)
    gaming_factor = 1.9 if "자주" in charge_gaming else (1.1 if "가끔" in charge_gaming else 1.0)
    case_factor = 1.2 if "네, 두꺼운" in case_type else 1.0
    fast_charge_factor = 1.15 if "초고속" in charger_type else 1.0
    
    stress_factor = 1.0
    if "매일 밤 100%" in charge_range:
        stress_factor = 1.4
    elif "0%가 되어" in charge_range:
        stress_factor = 1.7
    elif "20% ~ 80%" in charge_range:
        stress_factor = 0.7

    zero_factor = 1.3 if "일주일에 1번 이상" in discharge_zero else (1.1 if "한 달에 2~3번" in discharge_zero else 1.0)
    brightness_factor = 1.2 if "80% 이상" in screen_brightness else 1.0
    protect_discount = 0.8 if "네" in battery_protection else 1.0

    # 월간 감소율 (%/월)
    base_decay = 0.5
    current_decay = base_decay * temp_factor * gaming_factor * case_factor * fast_charge_factor * stress_factor * zero_factor * brightness_factor * protect_discount
    ideal_decay = base_decay * 0.65  # 좋은 습관 시

    # 36개월 데이터 생성
    months = np.arange(0, 37, 1)
    current_list, ideal_list = [], []
    c_val, i_val = float(current_soh), float(current_soh)
    
    for m in months:
        current_list.append(max(30.0, round(c_val, 1)))
        ideal_list.append(max(30.0, round(i_val, 1)))
        c_val -= current_decay
        i_val -= ideal_decay

    # 교체 시점(80% 미만) 계산
    current_life = next((m for m, val in enumerate(current_list) if val < 80.0), 36)
    ideal_life = next((m for m, val in enumerate(ideal_list) if val < 80.0), 36)
    saved_months = ideal_life - current_life

    # 하루 체감 사용시간 계산 (새 폰 기준 하루 8시간 화면 켜짐 가정)
    current_use_hours_now = round(8 * (current_soh / 100), 1)
    current_use_hours_1yr = round(8 * (current_list[min(12, len(current_list)-1)] / 100), 1)
    ideal_use_hours_1yr = round(8 * (ideal_list[min(12, len(ideal_list)-1)] / 100), 1)

    # 5. 진단 결과 출력
    st.markdown("---")
    st.subheader("📢 2. 한눈에 보는 내 스마트폰 진단 결과")

    # 체감 메시지 박스
    if current_life <= 12:
        st.markdown(f"""
        <div class="action-card">
            🚨 <b>경고! 이대로 쓰면 약 {current_life}개월 뒤 배터리 교체 경고등(80% 미만)이 켜집니다!</b><br>
            1년도 안 돼서 보조배터리를 달고 살거나, 약 10만 원의 배터리 교체 비용이 발생할 수 있습니다.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-card">
            💡 <b>약 {current_life}개월 동안은 무난하게 사용 가능합니다!</b><br>
            하지만 아래 맞춤 솔루션을 적용하면 <b>+{saved_months}개월</b> 동안 폰을 훨씬 더 오랫동안 새것처럼 쓸 수 있습니다.
        </div>
        """, unsafe_allow_html=True)

    # 주요 지표 3가지
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("현재 내 폰의 하루 사용 가능 시간", f"약 {current_use_hours_now} 시간", "100% 충전 시 체감 시간")
    with m2:
        st.metric("1년 뒤 하루 사용 시간 (현재 습관)", f"약 {current_use_hours_1yr} 시간", f"현재보다 {round(current_use_hours_now - current_use_hours_1yr, 1)}시간 줄어듦", delta_color="inverse")
    with m3:
        st.metric("1년 뒤 하루 사용 시간 (습관 개선)", f"약 {ideal_use_hours_1yr} 시간", f"+{round(ideal_use_hours_1yr - current_use_hours_1yr, 1)}시간 더 오래 씀", delta_color="normal")

    # 그래프 출력
    st.markdown("---")
    st.subheader("📉 [배터리 수명 예측 그래프] 3년간 수명 변화 추이")

    df_chart = pd.DataFrame({
        "경과 개월 수": months,
        "현재 습관대로 사용시 (%)": current_list,
        "올바른 습관 적용시 (%)": ideal_list,
        "배터리 교체 권장선 (80%)": [80.0] * len(months)
    }).set_index("경과 개월 수")

    st.line_chart(df_chart, color=["#EF4444", "#10B981", "#9CA3AF"])

    # 💡 그래프 설명 박스 (요청하신 기능 1)
    st.markdown("""
    <div class="graph-explain">
        <b>🔍 이 그래프는 무엇을 의미하나요?</b><br>
        <ul>
            <li><b>가로축 (경과 개월 수):</b> 앞으로 시간이 흐르는 개월 수 (0개월 = 지금 ~ 36개월 = 3년 뒤)를 뜻합니다.</li>
            <li><b>세로축 (%):</b> 스마트폰 배터리의 최대 성능 용량입니다. (100%에 가까울수록 새 폰 상태)</li>
            <li><b>회색 점선 (80% 교체 권장선):</b> 스마트폰 제조사(삼성, 애플)에서 <b>"배터리를 새것으로 교체해야 한다"</b>고 권장하는 마지노선입니다. 빨간선(내 습관)이 이 회색선 밑으로 떨어지면 폰이 자주 꺼지거나 성능이 저하됩니다.</li>
            <li><b>빨간선 vs 초록선:</b> 빨간선은 <b>현재 내 습관대로 쓸 때의 수명 하락 속도</b>이며, 초록선은 <b>추천 솔루션을 지켰을 때 유지되는 이상적인 수명</b>입니다.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # 6. 선택한 항목에 따른 동적 맞춤형 솔루션 (요청하신 기능 2)
    st.markdown("---")
    st.subheader("🛠️ 3. 당신만을 위한 맞춤형 배터리 심폐소생 솔루션")
    st.write("입력하신 습관을 분석하여 **가장 시급하게 고쳐야 할 개선점과 해결법**만 정리해 드립니다.")

    solutions_found = False

    # 충전 중 게임/영상 사용 시
    if "자주" in charge_gaming or "가끔" in charge_gaming:
        solutions_found = True
        st.markdown("""
        <div class="solution-card">
            <b>🔥 [시급] 충전 중 게임 / 고화질 영상 시청 금지!</b><br>
            • <b>원인:</b> 충전 중 발생하는 열과 화면/프로세서 발열이 더해지면 배터리 온도가 40℃ 이상으로 치솟아 수명이 2배 이상 빠르고 늙습니다.<br>
            • <b>해결책:</b> 충전 케이블을 연결했을 때는 폰을 사용하지 않고 놔두는 습관을 들이세요. 급할 때는 고사양 게임 대신 가벼운 웹서핑 정도만 해주세요.
        </div>
        """, unsafe_allow_html=True)

    # 충전 범위 (완충 지속 또는 방전)
    if "매일 밤 100%" in charge_range or "0%가 되어" in charge_range:
        solutions_found = True
        st.markdown("""
        <div class="solution-card">
            <b>⚡ [시급] 과충전 및 완전 방전(0%) 스트레스 줄이기</b><br>
            • <b>원인:</b> 배터리를 0%까지 쓰거나 밤새 100% 전압을 유지하면 양극과 음극의 전극 소재에 큰 구조적 변형(스트레스)이 생깁니다.<br>
            • <b>해결책:</b> 배터리가 20% 이하로 떨어지기 전에 충전기를 꽂고, 80~90% 사이에서 뽑아주는 <b>20%-80% 충전 습관</b>을 길러보세요!
        </div>
        """, unsafe_allow_html=True)

    # 두꺼운 케이스
    if "네, 두꺼운" in case_type:
        solutions_found = True
        st.markdown("""
        <div class="solution-card">
            <b>📦 [주의] 충전할 때 두꺼운 케이스는 잠시 벗겨주세요</b><br>
            • <b>원인:</b> 범퍼 케이스나 두꺼운 가죽 케이스는 충전 시 발생하는 내부 열이 밖으로 방출되는 것을 방해합니다.<br>
            • <b>해결책:</b> 초고속 충전을 하거나 여름철에는 충전할 때만이라도 케이스를 살짝 벗겨두면 발열이 쉽게 빠져나갑니다.
        </div>
        """, unsafe_allow_html=True)

    # 자주 방전
    if "일주일에 1번 이상" in discharge_zero or "한 달에 2~3번" in discharge_zero:
        solutions_found = True
        st.markdown("""
        <div class="solution-card">
            <b>🪫 [주의] 폰이 꺼질 때까지 쓰는 습관(0% 방전)은 배터리 암살자!</b><br>
            • <b>원인:</b> 리튬 이온 배터리는 전압이 완전히 떨어지는 0% 상태가 되면 내부 화학 물질이 영구적으로 손상됩니다.<br>
            • <b>해결책:</b> 외출 시 보조배터리를 챙기거나 15~20% 알림이 뜨면 즉시 저전력 모드를 켜서 폰이 꺼지는 일만은 막아주세요.
        </div>
        """, unsafe_allow_html=True)

    # 배터리 보호 미설정
    if "아니오" in battery_protection:
        solutions_found = True
        st.markdown("""
        <div class="solution-card">
            <b>⚙️ [추천] 스마트폰의 '배터리 보호(80~85% 제한)' 기능을 켜보세요</b><br>
            • <b>해결책:</b><br>
              - <b>갤럭시:</b> 설정 > 배터리 > '배터리 보호' 활성화 (80% 또는 85% 제한)<br>
              - <b>아이폰:</b> 설정 > 배터리 > 배터리 성능 상태 > '최적화된 배터리 충전' 또는 '80% 제한' 활성화
        </div>
        """, unsafe_allow_html=True)

    # 화면 밝기
    if "80% 이상" in screen_brightness:
        solutions_found = True
        st.markdown("""
        <div class="solution-card">
            <b>☀️ [추천] 화면 밝기를 '자동 밝기'로 변경해 보세요</b><br>
            • <b>원인:</b> 최고 밝기 지속은 화면 디스플레이 전력 소비와 지속적인 발열을 일으켜 배터리 소모를 촉진합니다.<br>
            • <b>해결책:</b> '자동 밝기' 옵션을 켜서 실내에서는 적절한 밝기로 자동 조절되도록 해주세요.
        </div>
        """, unsafe_allow_html=True)

    # 나쁜 습관이 없는 경우
    if not solutions_found:
        st.markdown("""
        <div class="success-card">
            🎉 <b>완벽합니다! 특별히 교정할 나쁜 습관이 없습니다.</b><br>
            지금처럼 충전 중 사용을 줄이고 적절한 배터리 잔량을 유지해 주시면, 3년 이상 스마트폰을 새것처럼 깨끗하게 사용하실 수 있습니다!
        </div>
        """, unsafe_allow_html=True)