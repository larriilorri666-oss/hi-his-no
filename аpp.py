import streamlit as st

st.title("🛡️ Проверка доступа на сайт")

name = st.text_input("Как тебя зовут?")
age = st.slider("Сколько тебе лет?", min_value=0, max_value=100, value=18)

if st.button("Проверить доступ"):
    if age == 18:
        st.balloons()
        st.success(f"Ого, {name}, тебе как раз 18! Добро пожаловать во взрослую жизнь! 🥳")
    elif age > 18:
        st.success(f"Привет, {name}! Доступ разрешен. 👍")
    else:
        st.error(f"Извини, {name}, но тебе ещё рано сюда. 🛑")
