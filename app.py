import streamlit as st
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

# ========== 設定(ここだけ編集すればOK) ==========
MEMBERS = [
    "阿部", "金澤", "金田", "黒崎", "小池", "中西", "西田",
    "野澤", "花田", "原", "原島", "久田", "藤川","吉田",
]  # この順番で毎週交代します
START_DATE = date(2026, 10, 26)  # 1人目の担当が始まる日(月曜日にしてください)
WEEKS_TO_SHOW = 14              # 一覧に表示する週数
# ================================================

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]


def monday_of(d: date) -> date:
    return d - timedelta(days=d.weekday())


def member_for_week(week_monday: date) -> str:
    weeks = (week_monday - monday_of(START_DATE)).days // 7
    return MEMBERS[weeks % len(MEMBERS)]


def fmt(d: date) -> str:
    return f"{d.month}/{d.day}({WEEKDAYS[d.weekday()]})"


st.set_page_config(page_title="鍵担当", page_icon="🔑", layout="centered")

today = datetime.now(ZoneInfo("Asia/Tokyo")).date()
this_monday = monday_of(today)
next_monday = this_monday + timedelta(days=7)

st.title("🔑 部屋の鍵担当")

# 今週・来週
st.caption(f"今週:{fmt(this_monday)} 〜 {fmt(this_monday + timedelta(days=6))}")
st.markdown(f"## 今週の担当:**{member_for_week(this_monday)}**")
st.info(f"来週({fmt(next_monday)}〜)の担当:**{member_for_week(next_monday)}**")

st.divider()

# 自分の担当週を調べる
st.subheader("自分の担当週を調べる")
me = st.selectbox("名前を選んでください", MEMBERS)
my_weeks = [
    this_monday + timedelta(days=7 * i)
    for i in range(len(MEMBERS))
    if member_for_week(this_monday + timedelta(days=7 * i)) == me
]
if my_weeks:
    next_turn = my_weeks[0]
    if next_turn == this_monday:
        st.success("今週はあなたの担当です!")
    else:
        st.write(f"次の担当週:**{fmt(next_turn)} 〜 {fmt(next_turn + timedelta(days=6))}**")

st.divider()

# スケジュール一覧
st.subheader(f"今後{WEEKS_TO_SHOW}週間のスケジュール")
rows = []
for i in range(WEEKS_TO_SHOW):
    wk = this_monday + timedelta(days=7 * i)
    rows.append(
        {
            "週": f"{fmt(wk)}〜",
            "担当": member_for_week(wk),
            "": "← 今週" if i == 0 else "",
        }
    )
st.dataframe(rows, hide_index=True, use_container_width=True)
