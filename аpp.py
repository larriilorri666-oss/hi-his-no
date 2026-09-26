import streamlit as st

# Создаем меню в выдвижной панели слева
page = st.sidebar.selectbox("Выберите раздел:", ["🎮 Игра: 100 шариков", "🧪 Лаборатория циклов"])

# --- СТРАНИЦА 1: НАША ИГРА ---
if page == "🎮 Игра: 100 шариков":
    st.title("💯 Мега-челлендж: 100 чисел по порядку!")
    st.write("Вставляй шарики строго по очереди: 1, 2, 3... до 100!")
    
    # Код игры (он остался прежним)
    game_code = """
    <style>
        .game-container { display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }
        #box { width: 100%; max-width: 340px; height: 500px; background: #222; border-radius: 15px; position: relative; border: 2px solid #444; overflow-y: auto; overflow-x: hidden; }
        .hole { width: 34px; height: 34px; background: #3a3a3a; border: 2px dashed #555; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: absolute; color: #777; font-size: 11px; font-weight: bold; }
        .shape { width: 32px; height: 32px; border-radius: 50%; cursor: grab; touch-action: none; position: absolute; z-index: 10; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; box-shadow: 0 3px 5px rgba(0,0,0,0.3); }
        .win-message { display: none; color: #00c04b; font-size: 22px; font-weight: bold; margin-top: 15px; text-align: center; }
        .info-status { color: #f9a825; font-size: 14px; font-weight: bold; margin-bottom: 10px; }
    </style>
    <div class="game-container">
        <div class="info-status" id="status">Ждем шарик номер: 1</div>
        <div id="box"></div>
        <div class="win-message" id="win">🏆 НЕВЕРОЯТНО! Все 100 чисел собраны!</div>
    </div>
    <script>
        const box = document.getElementById('box'); let nextRequiredNum = 1; const totalItems = 100;
        const colors = ['#ff4b4b', '#1c83e1', '#00c04b', '#f9a825', '#9c27b0', '#00bcd4', '#e91e63', '#4caf50'];
        for (let i = 1; i <= totalItems; i++) {
            const hole = document.createElement('div'); hole.className = 'hole'; hole.innerText = i; hole.dataset.num = i;
            const row = Math.floor((i - 1) / 6); const col = (i - 1) % 6;
            hole.style.left = (12 + col * 54) + 'px'; hole.style.top = (15 + row * 50) + 'px'; box.appendChild(hole);
        }
        const ballsStartTop = Math.ceil(totalItems / 6) * 50 + 30;
        for (let i = 1; i <= totalItems; i++) {
            const ball = document.createElement('div'); ball.className = 'shape'; ball.innerText = i; ball.dataset.num = i; ball.style.background = colors[i % colors.length];
            const randomX = Math.floor(Math.random() * 280) + 10; const randomY = Math.floor(Math.random() * 200) + ballsStartTop; 
            ball.style.left = randomX + 'px'; ball.style.top = randomY + 'px'; ball.dataset.startX = ball.style.left; ball.dataset.startY = ball.style.top;
            box.appendChild(ball); ball.addEventListener('pointerdown', onPointerDown);
        }
        function onPointerDown(e) {
            const ball = e.currentTarget; if (ball.dataset.placed) return;
            ball.style.cursor = 'grabbing'; ball.style.zIndex = 100; ball.setPointerCapture(e.pointerId);
            const boxRect = box.getBoundingClientRect(); const startX = e.clientX - ball.getBoundingClientRect().left; const startY = e.clientY - ball.getBoundingClientRect().top;
            function onPointerMove(ev) {
                let x = ev.clientX - boxRect.left - startX + box.scrollLeft; let y = ev.clientY - boxRect.top - startY + box.scrollTop;
                ball.style.left = x + 'px'; ball.style.top = y + 'px';
            }
            function onPointerUp(ev) {
                ball.removeEventListener('pointermove', onPointerMove); ball.removeEventListener('pointerup', onPointerUp); ball.style.cursor = 'grab'; ball.style.zIndex = 10;
                const currentNum = parseInt(ball.dataset.num); const holes = document.querySelectorAll('.hole'); let placedSuccessfully = false;
                holes.forEach(hole => {
                    if (hole.dataset.num === ball.dataset.num) {
                        const hRect = hole.getBoundingClientRect(); const bRect = ball.getBoundingClientRect();
                        const distance = Math.hypot((hRect.left + hRect.width/2) - (bRect.left + bRect.width/2), (hRect.top + hRect.height/2) - (bRect.top + bRect.height/2));
                        if (distance < 25) {
                            if (currentNum === nextRequiredNum) {
                                ball.style.left = (hole.offsetLeft + 1) + 'px'; ball.style.top = (hole.offsetTop + 1) + 'px'; ball.dataset.placed = "true"; ball.style.cursor = 'default'; ball.style.boxShadow = 'none';
                                nextRequiredNum++; placedSuccessfully = true;
                                if (nextRequiredNum <= totalItems) { document.getElementById('status').innerText = "Ждем шарик номер: " + nextRequiredNum; } else { document.getElementById('status').style.display = 'none'; document.getElementById('win').style.display = 'block'; }
                            }
                        }
                    }
                });
                if (!placedSuccessfully) { ball.style.left = ball.dataset.startX; ball.style.top = ball.dataset.startY; }
            }
            ball.addEventListener('pointermove', onPointerMove); ball.addEventListener('pointerup', onPointerUp);
        }
    </script>
    """
    st.components.v1.html(game_code, height=560)

# --- СТРАНИЦА 2: УЧИМ ЦИКЛЫ ---
elif page == "🧪 Лаборатория циклов":
    st.title("🧪 Лаборатория циклов на Python")
    st.write("Сейчас мы заставим компьютер работать за нас!")

    # Интерактивный ползунок: сколько раз повторить действие
    repeats = st.slider("Сколько раз повторить цикл?", min_value=1, max_value=20, value=5)

    st.write("### Результат работы цикла `for`:")

    # ВАШ ПЕРВЫЙ НАСТОЯЩИЙ ЦИКЛ НА САЙТЕ!
    for i in range(1, repeats + 1):
        st.write(f"🤖 Робот повторил это действие {i}-й раз")
