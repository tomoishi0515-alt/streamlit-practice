import streamlit as st

st.title("Hello, Streamlit!")
st.write("これは最小構成のStreamlit四則演算アプリです。")
# input_number1 = st.number_input("数字を入力してください")
# input_number2 = st.number_input("数字を入力してください")
input_number1 = st.number_input("1つ目の数字を入力してください", key="input1")
input_number2 = st.number_input("2つ目の数字を入力してください", key="input2")
input_operation = st.selectbox("演算子を選んでください", ("+", "-", "*", "/"), key="operation")
if st.button("計算する"):
    if input_operation == "+":
        st.write(f"計算結果は {input_number1 + input_number2} です")
    elif input_operation == "-":
        st.write(f"計算結果は {input_number1 - input_number2} です")
    elif input_operation == "*":
        st.write(f"計算結果は {input_number1 * input_number2} です")
    elif input_operation == "/":
        if input_number2 != 0:
            st.write(f"計算結果は {input_number1 / input_number2} です")
        else:
            st.write("0で割ることはできません")
#if st.button("風船を飛ばす"):
    st.balloons()
#if st.button("雪を降らす"):
    #st.snow()