import random
import pandas as pd
import streamlit as st
# ---- タイトル ----
st.title("🎯 Hit & Blow Game!")
st.write("4桁の数字を当てるゲームです。")
# ---- 初期設定 ----
if "target_number" not in st.session_state:
    st.session_state.target_number = "".join(random.sample("0123456789", 4))
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "game_end" not in st.session_state:
    st.session_state.game_end = False
# ---- ゲーム終了時の処理 ----
if st.session_state.game_end:
    st.balloons()
    st.success(f"🎉 正解！ {st.session_state.attempts} 回で当てました！")
    st.success(f"🎉 正解は {st.session_state.target_number} でした！お疲れさまでした！")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.button("🔄 ゲームをリセット"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.stop()
# ---- ユーザー入力 ----
user_input = st.text_input("4桁の数字を入力してください（例: 1234）", max_chars=4)
if user_input:
    # 入力の検証
    # 4桁の異なる数字であることを確認
    # 先頭にゼロが来ないことを確認
    # それ以外の文字が含まれていないことを確認
    if len(user_input) != 4 or not user_input.isdigit() or len(set(user_input)) != 4 or user_input[0] == "0":
        st.error("4桁の異なる数字を入力してください。")
    else:
        st.session_state.attempts += 1
        # HitとBlowの計算
        # 位置も考慮した一致をカウント
        # 位置を考慮しない一致をカウントし、Hitを引く
        hit = sum(1 for a, b in zip(user_input, st.session_state.target_number) if a == b)
        blow = sum(1 for char in user_input if char in st.session_state.target_number) - hit
        st.session_state.history.append({
            "試行回数": st.session_state.attempts,
            "入力": user_input,
            "Hit": hit,
            "Blow": blow
        })
        if hit == 4:
            st.session_state.game_end = True
            st.rerun()
        else:
            st.info(f"Hit: {hit}, Blow: {blow}")
            #st.rerun()
# ---- ゲーム中の表示 ----
# ---- 連勝記録 ----
#st.markdown(f"🔥 現在の試行回数: {st.session_state.attempts}")
# ---- 結果表表示 ----
if st.session_state.history:
    st.subheader("📈 結果履歴")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True)
