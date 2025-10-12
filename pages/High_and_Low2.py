# High & Low Game
# 1〜13の数字の中で、次の数字がHighかLowかを当てるゲーム
# 重複しない数字を引くようにする
# 連勝数、最高連勝数、結果表表示、ラウンド数指定機能追加
# チップがなくなったらゲームオーバー

import json
from pathlib import Path
import random
import pandas as pd
import streamlit as st
# ---- JSON読み込み ----
# json_path = Path(__file__).parent.parent / "sample_data" / "highlow_round3.json"
# if json_path.exists():
#     with open(json_path, "r", encoding="utf-8") as f:
#         data = json.load(f)
# ---- タイトル ----
st.title("♠️ High & Low Game!")
st.write("1〜13の数字の中で、次の数字がHighかLowかを当てるゲームです。")
# ---- 初期設定 ----
initial_chips = 1000
if "chips" not in st.session_state:
    st.session_state.chips = initial_chips
if "round" not in st.session_state:
    st.session_state.round = 1
if "count" not in st.session_state:
    st.session_state.count = 0
if "max_count" not in st.session_state:
    st.session_state.max_count = 0
if "used_numbers" not in st.session_state:
    st.session_state.used_numbers = set()
if "current_number" not in st.session_state:
    st.session_state.current_number = random.randint(1, 13)
    st.session_state.used_numbers.add(st.session_state.current_number)
if "previous_number" not in st.session_state:
    st.session_state.previous_number = None
if "next_number" not in st.session_state:
    st.session_state.next_number = None
if "already_predicted" not in st.session_state:
    st.session_state.already_predicted = False
if "history" not in st.session_state:
    st.session_state.history = []
if "max_rounds" not in st.session_state:
    st.session_state.max_rounds = 5  # ★ number_inputのデフォルト値をここで設定
# st.number_input("プレイするラウンド数を指定してください", 1, 10, 1)
if "game_end" not in st.session_state:
    st.session_state.game_end = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False
# ---- 重複しない数字を引く関数 ----
def draw_unique_number():
    # 1から13までの数字の中で、まだ使われていない数字のリストを作成
    available = [n for n in range(1, 14) if n not in st.session_state.used_numbers]
    if not available:
        st.session_state.used_numbers.clear()  # 山札リセット
        available = list(range(1, 14))
    new_num = random.choice(available)
    st.session_state.used_numbers.add(new_num)
    return new_num

# ---- ラウンド数設定 ----
# ゲームが進行中はラウンド数を変更できないようにする
is_game_in_progress = not st.session_state.game_end and st.session_state.round > 1
#if not is_game_in_progress: 
#if文だとなぜかデフォルト値(5)に戻されてしまう
st.number_input(
    "プレイするラウンド数を指定してください",
    min_value=1,
    max_value=10,
    key="max_rounds",  # keyを指定して値をsession_stateに直接保存
    disabled=is_game_in_progress
    #value=st.session_state.max_rounds
)
# ---- 状態表示 ----
st.markdown(f"**💰️ 現在のチップ:** {st.session_state.chips}")
st.markdown(f"**現在のラウンド:** {st.session_state.round} / {st.session_state.max_rounds}")
st.markdown(f"**現在の数字:** {st.session_state.current_number}")

# ---- ゲーム進行 ----
if st.session_state.game_end and not st.session_state.game_over:
    st.success("🎉 ゲーム終了！お疲れさまでした！")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.button("🔄 ゲームをリセット"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.stop()
    
elif not st.session_state.already_predicted:
    bet_amount = st.number_input(
        "賭け金を入力してください",
        min_value=1,
        max_value=st.session_state.chips,
        value=1,
        step=1,
        key="bet"
    )
    option = st.radio("次の数字はHighかLowか？", ("High", "Low"))
    #option = st.selectbox("次の数字はHighかLowか？", ("High", "Low"))
    if st.button("予想する"):
        next_number = draw_unique_number()
        st.session_state.next_number = next_number
        st.session_state.already_predicted = True
        # 判定処理
        if (option == "High" and next_number > st.session_state.current_number) or \
           (option == "Low" and next_number < st.session_state.current_number):
            st.session_state.count += 1
            st.session_state.chips += bet_amount
            result_text = "🎉 正解！チップを獲得しました！"
        elif next_number == st.session_state.current_number:
            result_text = "🤝 同じ数字！引き分けです。"
        else:
            st.session_state.count = 0
            st.session_state.chips -= bet_amount
            result_text = "❌ 不正解！チップを失いました。"
        # 記録を追加
        st.session_state.history.append({
            "ラウンド": st.session_state.round,
            "前の数字": st.session_state.current_number,
            "次の数字": next_number,
            "選択": option,
            "結果": result_text.replace("🎉 ", "").replace("❌ ", "").replace("🤝 ", ""),
            "チップ": st.session_state.chips
        })
        # ゲームオーバー処理
        if st.session_state.chips <= 0:
            result_text += "\n💀 チップがなくなりました。ゲームオーバーです。"
            st.session_state.game_over = True
            # st.session_state.chips = initial_chips
            # st.session_state.count = 0
            # st.session_state.round = 1
        # 表示更新
        st.session_state.previous_number = st.session_state.current_number
        st.session_state.current_number = next_number
        st.session_state.result_text = result_text
        st.rerun()
else:
    # ---- 結果表示 ----
    st.subheader("🎬 結果")
    st.write(f"前の数字：{st.session_state.previous_number}")
    st.write(f"次の数字：{st.session_state.next_number}")
    st.write(st.session_state.result_text)
    if st.session_state.game_over:
        if st.button("🔄 ゲームをリセット"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    elif st.session_state.round >= st.session_state.max_rounds:
        st.session_state.game_end = True
        st.rerun()
    else:
        if st.button("次のラウンドへ進む"):
            st.session_state.round += 1
            st.session_state.already_predicted = False
            st.session_state.previous_number = st.session_state.current_number    
            st.rerun()
# ---- 連勝記録 ----
st.markdown(f"🔥 現在の連勝数: {st.session_state.count}")
if st.session_state.count > st.session_state.max_count:
    st.session_state.max_count = st.session_state.count
st.markdown(f"🏆️ 最高連勝数: {st.session_state.max_count}")
# ---- 結果表表示 ----
if st.session_state.history:
    st.subheader("📈 結果履歴")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True)
# ---- リセット ----
if not st.session_state.game_over:
    if st.button("🔄 ゲームをリセット"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()