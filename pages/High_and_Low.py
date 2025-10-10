
import streamlit as st
st.title("High & Low Game!")
st.write("数字が1から13の中で、次に出る数字がHighかLowかを当てるゲームです。")
import random
qp = st.query_params
round_num = int(qp.get("round", "1"))
#st.write(f"現在のラウンドは {round_num} です")

if "count" not in st.session_state:
    st.session_state.count = 0
if "max_count" not in st.session_state:
    st.session_state.max_count = 0
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 13)
st.write(f"現在の数字は {st.session_state.number} です")
option = st.selectbox("次の数字はHighかLowかを選んでください", ("High", "Low"))
if st.button("予想する"):
    next_number = random.randint(1, 13)
    st.write(f"次の数字は {next_number} でした")
    if (option == "High" and next_number > st.session_state.number) or (option == "Low" and next_number < st.session_state.number):
        st.session_state.count += 1
        st.write("正解です！")
        st.balloons()
    elif next_number == st.session_state.number:
        st.write("同じ数字でした。引き分けです。")
    else:
        st.session_state.count = 0
        st.write("不正解です。")
    st.session_state.number = next_number
    if st.button("次のラウンドへ進む"):
        round_num += 1
        st.query_params["round"] = str(round_num)
        st.write(f"ラウンドを進めました。現在のラウンドは {round_num} です")
st.write(f"現在の連勝数は {st.session_state.count} です")
if st.session_state.count > st.session_state.max_count:
    st.session_state.max_count = st.session_state.count
st.write(f"最高連勝数は {st.session_state.max_count} です")

if st.button("リセット"):
    st.session_state.count = 0
    st.session_state.number = random.randint(1, 13)
    st.write("ゲームをリセットしました。")
    st.write(f"新しい現在の数字は {st.session_state.number} です")