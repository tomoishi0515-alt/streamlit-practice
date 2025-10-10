import json
from pathlib import Path
import random
import streamlit as st
# ---- JSON読み込み　----
json_path = Path(__file__).parent.parent / "sample_data" / "highlow_round3.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)
st.title("High & Low Game!")
st.write("数字が1〜13の中で、次の数字がHighかLowかを当てるゲームです。")
initial_chips = 1000
# ---- セッション初期化 ----
if "chips" not in st.session_state:
    st.session_state.chips = initial_chips
if "round" not in st.session_state:
    st.session_state.round = 1
if "count" not in st.session_state:
    st.session_state.count = 0
if "max_count" not in st.session_state:
    st.session_state.max_count = 0
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 13)
if "already_predicted" not in st.session_state:
    st.session_state.already_predicted = False
# ---- 状態表示 ----
st.write(f"💰️ 現在のチップ: {st.session_state.chips}")
st.write(f"現在のラウンド: {st.session_state.round}")
st.write(f"現在の数字: {st.session_state.number}")
# ---- ゲームロジック ----
if not st.session_state.already_predicted:
    bet_amount = st.number_input(
        "賭け金を入力してください",
        min_value=1,
        max_value=st.session_state.chips,
        value=1,
        step=1,
        key="bet"
    )
    option = st.selectbox("次の数字はHighかLowか？", ("High", "Low"))
    if st.button("予想する"):
        next_number = random.randint(1, 13)
        st.session_state.next_number = next_number
        st.session_state.already_predicted = True
        # 勝敗処理
        if (option == "High" and next_number > st.session_state.number) or \
           (option == "Low" and next_number < st.session_state.number):
            st.session_state.count += 1
            st.session_state.chips += bet_amount
            st.session_state.result_message = "🎉 正解！チップを獲得しました！"
        elif next_number == st.session_state.number:
            st.session_state.result_message = "🤝 同じ数字！引き分けです。"
        else:
            st.session_state.count = 0
            st.session_state.chips -= bet_amount
            st.session_state.result_message = "❌ 不正解！チップを失いました。"
        if st.session_state.chips <= 0:
            st.session_state.result_message += "\n💀 チップがなくなりました。リセットします。"
            st.session_state.chips = initial_chips
            st.session_state.count = 0
            st.session_state.round = 1
        st.session_state.number = next_number
        # ✅ 即時UI反映
        st.rerun()
else:
    # ---- 結果表示 ----
    st.write(f"次の数字は **{st.session_state.next_number}** でした！")
    st.write(st.session_state.result_message)
    if st.button("次のラウンドへ進む"):
        st.session_state.round += 1
        st.session_state.already_predicted = False
        st.session_state.number = random.randint(1, 13)
        st.rerun()
# ---- 連勝記録 ----
st.write(f"🔥 現在の連勝数: {st.session_state.count}")
if st.session_state.count > st.session_state.max_count:
    st.session_state.max_count = st.session_state.count
st.write(f"🏆️ 最高連勝数: {st.session_state.max_count}")



















# import json
# from pathlib import Path

# # ----Pathを指定して JSONファイルを読み込み ----
# json_path = Path(__file__).parent.parent / "sample_data" / "highlow_round3.json"
# with open(json_path, "r", encoding="utf-8") as f:
#     data = json.load(f)

# import streamlit as st

# st.title("High & Low Game!")
# st.write("数字が1から13の中で、次に出る数字がHighかLowかを当てるゲームです。")
# import random
# initial_chips = 1000
# if "chips" not in st.session_state:
#     st.session_state.chips = initial_chips
# st.write(f"現在のチップは {st.session_state.chips} です")
# st.write("ゲームを始めるには、まず賭け金を入力してください。")
# bet_amount = st.number_input("賭け金を入力してください", min_value=1, max_value=st.session_state.chips, value=1, step=1)

# if "round" not in st.session_state:
#     st.session_state.round = 1
# round_num = st.session_state.round
# st.write(f"現在のラウンドは {round_num} です") 
# if "count" not in st.session_state:
#     st.session_state.count = 0
# if "max_count" not in st.session_state:
#     st.session_state.max_count = 0
# if "number" not in st.session_state:
#     st.session_state.number = random.randint(1, 13)
# st.write(f"現在の数字は {st.session_state.number} です")
# option = st.selectbox("次の数字はHighかLowかを選んでください", ("High", "Low"))
# if "guessed" not in st.session_state:
#     st.session_state.guessed = False
# if st.button("予想する", disabled=st.session_state.guessed):
#     st.session_state.guessed = True
#     next_number = random.randint(1, 13)
#     st.write(f"次の数字は {next_number} でした")
#     if (option == "High" and next_number > st.session_state.number) or (option == "Low" and next_number < st.session_state.number):
#         st.session_state.count += 1
#         st.session_state.chips += bet_amount
#         st.write(f"正解です！チップが {bet_amount} 増えました。")
#         st.balloons()
#     elif next_number == st.session_state.number:
#         st.write("同じ数字でした。引き分けです。")
#     else:
#         st.session_state.count = 0
#         st.session_state.chips -= bet_amount
#         st.write(f"不正解です。チップが {bet_amount} 減りました。")
#     st.session_state.number = next_number
#     if st.button("次のラウンドへ進む"):
#         if st.session_state.chips <= 0:
#             st.write("チップがなくなりました。ゲームオーバーです。")
#         else:
#             st.session_state.round += 1
#             round_num = st.session_state.round
#             st.write(f"ラウンドを進めました。現在のラウンドは {round_num} です")
#             st.session_state.guessed = False
# st.write(f"現在の連勝数は {st.session_state.count} です")
# if st.session_state.count > st.session_state.max_count:
#     st.session_state.max_count = st.session_state.count
# st.write(f"最高連勝数は {st.session_state.max_count} です") 
# if st.button("リセット"):
#     st.session_state.count = 0
#     st.session_state.number = random.randint(1, 13)
#     st.session_state.chips = initial_chips
#     st.write("ゲームをリセットしました。")
#     st.write(f"新しい現在の数字は {st.session_state.number} です")
#     st.session_state.round = 1
#     st.session_state.guessed = False
#     st.write(f"現在のラウンドは {st.session_state.round} です") 
#     st.write(f"現在のチップは {st.session_state.chips} です")
#     st.write("ゲームを始めるには、まず賭け金を入力してください。")
#     bet_amount = st.number_input("賭け金を入力してください", min_value=1, max_value=st.session_state.chips, value=1, step=1)
#     st.write(f"賭け金は {bet_amount} です") 
#     st.write(f"新しい現在の数字は {st.session_state.number} です")
#     st.write(f"現在の連勝数は {st.session_state.count} です")
#     st.write(f"最高連勝数は {st.session_state.max_count} です") 
#     st.write(f"現在のラウンドは {st.session_state.round} です") 
#     st.write(f"現在のチップは {st.session_state.chips} です")
#     bet_amount = st.number_input("賭け金を入力してください", min_value=1, max_value=st.session_state.chips, value=1, step=1)
#     st.write(f"賭け金は {bet_amount} です")     