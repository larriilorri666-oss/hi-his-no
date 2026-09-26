import streamlit as st

# Создаем меню в выдвижной панели слева
page = st.sidebar.selectbox("Выберите раздел:", [
    "🎮 Настраиваемая игра", 
    "🧪 Лаборатория циклов",
    "🐢 Геометрия на Python"
])

# --- СТРАНИЦА 1: НАСТРАИВАЕМАЯ ИГРА ---
if page == "🎮 Настраиваемая игра":
    st.title("🧩 Интерактивный конструктор пазла")
    st.write("Настройте сложность игры под себя!")

    total_balls = st.slider("Сколько шариков и лунок сделать в игре?", min_value=5, max_value=100, value=20, step=5)
    st.write(f"Текущая сложность: **{total_balls} шариков**. Попробуй расставить их строго по порядку!")

    game_code = f"""
    <style>
        .game-container {{ display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }}
        #box {{ width: 100%; max-width: 340px; height: 550px; background: #222; border-radius: 15px; position: relative; border: 2px solid #444; overflow-y: auto; overflow-x: hidden; }}
        .hole {{ width: 34px; height: 34px; background: #3a3a3a; border: 2px dashed #555; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: absolute; color: #777; font-size: 11px; font-weight: bold; }}
        .shape {{ width: 32px; height: 32px; border-radius: 50%; cursor: grab; touch-action: none; position: absolute; z-index: 10; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; box-shadow: 0 3px 5px rgba(0,0,0,0.3); }}
        .win-message {{ display: none; color: #00c04b; font-size: 22px; font-weight: bold; margin-top: 15px; text-align: center; }}
        .info-status {{ color: #f9a825; font-size: 14px; font-weight: bold; margin-bottom: 10px; }}
    </style>

    <div class="game-container">
        <div class="info-status" id="status">Ждем шарик номер: 1</div>
        <div id="box"></div>
        <div class="win-message" id="win">🏆 ПОБЕДА! Все {{total_balls}} чисел собраны строго по порядку!</div>
    </div>

    <script>
        const box = document.getElementById('box');
        let nextRequiredNum = 1;
        const totalItems = {total_balls};
        const colors = ['#ff4b4b', '#1c83e1', '#00c04b', '#f9a825', '#9c27b0', '#00bcd4', '#e91e63', '#4caf50'];

        for (let i = 1; i <= totalItems; i++) {{
            const hole = document.createElement('div');
            hole.className = 'hole';
            hole.innerText = i;
            hole.dataset.num = i;
            const row = Math.floor((i - 1) / 6);
            const col = (i - 1) % 6;
            hole.style.left = (12 + col * 54) + 'px';
            hole.style.top = (15 + row * 50) + 'px';
            box.appendChild(hole);
        }}

        const ballsStartTop = Math.ceil(totalItems / 6) * 50 + 30;

        for (let i = 1; i <= totalItems; i++) {{
            const ball = document.createElement('div');
            ball.className = 'shape';
            ball.innerText = i;
            ball.dataset.num = i;
            ball.style.background = colors[i % colors.length];
            const randomX = Math.floor(Math.random() * 280) + 10;
            const randomY = Math.floor(Math.random() * 200) + ballsStartTop; 
            ball.style.left = randomX + 'px';
            ball.style.top = randomY + 'px';
            ball.dataset.startX = ball.style.left;
            ball.dataset.startY = ball.style.top;
            box.appendChild(ball);
            ball.addEventListener('pointerdown', onPointerDown);
        }}

        function onPointerDown(e) {{
            const ball = e.currentTarget;
            if (ball.dataset.placed) return;
            ball.style.cursor = 'grabbing';
            ball.style.zIndex = 100;
            ball.setPointerCapture(e.pointerId);
            const boxRect = box.getBoundingClientRect();
            const startX = e.clientX - ball.getBoundingClientRect().left;
            const startY = e.clientY - ball.getBoundingClientRect().top;

            function onPointerMove(ev) {{
                let x = ev.clientX - boxRect.left - startX + box.scrollLeft;
                let y = ev.clientY - boxRect.top - startY + box.scrollTop;
                ball.style.left = x + 'px';
                ball.style.top = y + 'px';
            }}

            function onPointerUp(ev) {{
                ball.removeEventListener('pointermove', onPointerMove);
                ball.removeEventListener('pointerup', onPointerUp);
                ball.style.cursor = 'grab';
                ball.style.zIndex = 10;
                const currentNum = parseInt(ball.dataset.num);
                const holes = document.querySelectorAll('.hole');
                let placedSuccessfully = false;
                
                holes.forEach(hole => {{
                    if (hole.dataset.num === ball.dataset.num) {{
                        const hRect = hole.getBoundingClientRect();
                        const bRect = ball.getBoundingClientRect();
                        const distance = Math.hypot((hRect.left + hRect.width/2) - (bRect.left + bRect.width/2), (hRect.top + hRect.height/2) - (bRect.top + bRect.height/2));
                        if (distance < 25) {{
                            if (currentNum === nextRequiredNum) {{
                                ball.style.left = (hole.offsetLeft + 1) + 'px';
                                ball.style.top = (hole.offsetTop + 1) + 'px';
                                ball.dataset.placed = "true";
                                ball.style.cursor = 'default';
                                ball.style.boxShadow = 'none';
                                nextRequiredNum++;
                                placedSuccessfully = true;
                                if (nextRequiredNum <= totalItems) {{
                                    document.getElementById('status').innerText = "Ждем шарик номер: " + nextRequiredNum;
                                }} else {{
                                    document.getElementById('status').style.display = 'none';
                                    document.getElementById('win').style.display = 'block';
                                }}
                            }}
                        }}
                    }}
                }});
                if (!placedSuccessfully) {{
                    ball.style.left = ball.dataset.startX;
                    ball.style.top = ball.dataset.startY;
                }}
            }}
            ball.addEventListener('pointermove', onPointerMove);
            ball.addEventListener('pointerup', onPointerUp);
        }}
    </script>
    """
    st.components.v1.html(game_code, height=610)

# --- СТРАНИЦА 2: ЛАБОРАТОРИЯ ЦИКЛОВ ---
elif page == "🧪 Лаборатория циклов":
    st.title("🧪 Лаборатория циклов на Python")
    repeats = st.slider("Сколько раз повторить цикл?", min_value=1, max_value=20, value=5)
    st.write("### Результат работы цикла `for`:")
    for i in range(1, repeats + 1):
        st.write(f"🤖 Робот повторил это действие {i}-й раз")

# --- СТРАНИЦА 3: ГЕОМЕТРИЯ ---
elif page == "🐢 Геометрия на Python":
    st.title("🐢 Рисуем фигуры кодом на Python!")
    st.write("Давай посмотрим, как с помощью геометрии и циклов Python создаёт идеальные формы.")

    shape_choice = st.selectbox("Какую фигуру нарисовать?", ["Квадрат", "Треугольник", "Сложный узор"])

    if shape_choice == "Квадрат":
        st.write("### 🟥 Как Python рисует Квадрат через цикл:")
        st.code('''
# Робот делает 4 одинаковых шага и поворота на 90 градусов:
for i in range(4):
    forward(100)  # Ползи вперед
    right(90)     # Поверни направо на углы квадрата
''')
        st.markdown('<div style="width:100px; height:100px; background:#ff4b4b; border-radius:5px; margin: 20px auto;"></div>', unsafe_allow_html=True)

    elif shape_choice == "Треугольник":
        st.write("### 🔺 Как Python рисует Правильный Треугольник:")
        st.code('''
# У треугольника 3 стороны, а угол поворота равен 120 градусов:
for i in range(3):
    forward(100)
    right(120)
''')
        st.markdown('<div style="width: 0; height: 0; border-left: 50px solid transparent; border-right: 50px solid transparent; border-bottom: 100px solid #1c83e1; margin: 20px auto;"></div>', unsafe_allow_html=True)

    elif shape_choice == "Сложный узор":
        st.write("### 🌀 Магия циклов: Спираль из 20 квадратов!")
        st.write("Если запустить цикл 20 раз и каждый раз немного поворачивать квадрат, то получится шедевр:")
        st.code('''
for i in range(20):
    draw_square()  # Рисуем квадрат
    right(18)      # Немного сдвигаем угол поворота
''')
        
        html_pattern = '<div style="text-align:center;"><svg width="200" height="200" viewBox="0 0 200 200">'
        for r in range(0, 360, 2):
            html_pattern += f'<rect x="50" y="50" width="100" height="100" fill="none" stroke="#00c04b" stroke-width="1.5" transform="rotate({r} 100 100)"/>'
        html_pattern += '</svg></div>'
        st.markdown(html_pattern, unsafe_allow_html=True)
