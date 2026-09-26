import streamlit as st

# 1. Обновляем наше меню в выдвижной панели (добавляем третий пункт)
page = st.sidebar.selectbox("Выберите раздел:", [
    "🎮 Настраиваемая игра", 
    "🧪 Лаборатория циклов",
    "🐢 Геометрия на Python"
])

# --- СТРАНИЦА 1: НАСТРАИВАЕМАЯ ИГРА ---
if page == "🎮 Настраиваемая игра":
    st.title("🧩 Интерактивный конструктор пазла")
    total_balls = st.slider("Сколько шариков и лунок сделать в игре?", min_value=5, max_value=100, value=20, step=5)
    
    # (Здесь остается весь тот огромный код игры, который ты уже запускал...)
    # ... для экономии места на экране телефона я его тут не расписываю, он у тебя уже есть

# --- СТРАНИЦА 2: ЛАБОРАТОРИЯ ЦИКЛОВ ---
elif page == "🧪 Лаборатория циклов":
    st.title("🧪 Лаборатория циклов на Python")
    repeats = st.slider("Сколько раз повторить цикл?", min_value=1, max_value=20, value=5)
    for i in range(1, repeats + 1):
        st.write(f"🤖 Робот повторил это действие {i}-й раз")

# --- НОВАЯ СТРАНИЦА 3: УЧИМСЯ РИСОВАТЬ ФИГУРЫ ---
elif page == "🐢 Геометрия на Python":
    st.title("🐢 Рисуем фигуры кодом на Python!")
    st.write("Давай посмотрим, как с помощью геометрии и циклов Python создаёт идеальные формы.")

    # Выбираем фигуру на сайте
    shape_choice = st.selectbox("Какую фигуру нарисовать?", ["Квадрат", "Треугольник", "Сложный узор"])

    # Так как стандартная Черепашка на сайтах требует отдельного окна, 
    # мы сгенерируем красивый векторный рисунок (SVG) прямо через Python!
    
    if shape_choice == "Квадрат":
        st.write("### 🟥 Как Python рисует Квадрат через цикл:")
        st.code('''
# Робот делает 4 одинаковых шага и поворота на 90 градусов:
for i in range(4):
    forward(100)  # Ползи вперед
    right(90)     # Поверни направо на углы квадрата
        ''')
        # Рисуем фигуру на экране
        st.markdown('<div style="width:100px; height:100px; background:#ff4b4b; border-radius:5px;"></div>', unsafe_allowed_html=True)

    elif shape_choice == "Треугольник":
        st.write("### 🔺 Как Python рисует Правильный Треугольник:")
        st.code('''
# У треугольника 3 стороны, а угол поворота равен 120 градусов:
for i in range(3):
    forward(100)
    right(120)
        ''')
        # Рисуем фигуру на экране
        st.markdown('<div style="width: 0; height: 0; border-left: 50px solid transparent; border-right: 50px solid transparent; border-bottom: 100px solid #1c83e1;"></div>', unsafe_allowed_html=True)

    elif shape_choice == "Сложный узор":
        st.write("### 🌀 Магия циклов: Спираль из 20 квадратов!")
        st.write("Если запустить цикл 20 раз и каждый раз немного поворачивать квадрат, то получится шедевр:")
        st.code('''
for i in range(20):
    draw_square()  # Рисуем квадрат
    right(18)      # Немного сдвигаем угол поворота
        ''')
        
        # Генерируем крутую спираль кодом!
        html_pattern = '<svg width="200" height="200" viewBox="0 0 200 200">'
        for r in range(0, 360, 18):
            html_pattern += f'<rect x="50" y="50" width="100" height="100" fill="none" stroke="#00c04b" stroke-width="1.5" transform="rotate({r} 100 100)"/>'
        html_pattern += '</svg>'
        st.markdown(html_pattern, unsafe_allowed_html=True)

