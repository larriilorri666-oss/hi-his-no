import streamlit as st

st.title("💯 Мега-челлендж: 100 чисел по порядку!")
st.write("Вставляй шарики строго по очереди: 1, 2, 3... до 100! Ошибка заблокирует фишку.")

# Код игры на 100 элементов со строгим порядком
game_code = """
<style>
    .game-container { display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }
    /* Поле с прокруткой, чтобы поместились все 100 фишек */
    #box { width: 100%; max-width: 340px; height: 600px; background: #222; border-radius: 15px; position: relative; border: 2px solid #444; overflow-y: auto; overflow-x: hidden; }
    
    /* Делаем лунки меньше (34px), чтобы они умещались в ряды */
    .hole { width: 34px; height: 34px; background: #3a3a3a; border: 2px dashed #555; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: absolute; color: #777; font-size: 11px; font-weight: bold; }
    
    /* Шарики тоже делаем компактными */
    .shape { width: 32px; height: 32px; border-radius: 50%; cursor: grab; touch-action: none; position: absolute; z-index: 10; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; box-shadow: 0 3px 5px rgba(0,0,0,0.3); }
    
    .win-message { display: none; color: #00c04b; font-size: 22px; font-weight: bold; margin-top: 15px; text-align: center; }
    .info-status { color: #f9a825; font-size: 14px; font-weight: bold; margin-bottom: 10px; }
</style>

<div class="game-container">
    <div class="info-status" id="status">Ждем шарик номер: 1</div>
    <div id="box">
        <!-- Сюда добавятся 100 лунок и 100 шариков -->
    </div>
    <div class="win-message" id="win">🏆 НЕВЕРОЯТНО! Вы прошли мега-челлендж и собрали все 100 чисел!</div>
</div>

<script>
    const box = document.getElementById('box');
    let nextRequiredNum = 1; // Переменная хранит номер шарика, который нужно вставить СЛЕДУЮЩИМ
    const totalItems = 100;

    const colors = ['#ff4b4b', '#1c83e1', '#00c04b', '#f9a825', '#9c27b0', '#00bcd4', '#e91e63', '#4caf50'];

    // 1. Генерируем 100 лунок (по 6 штук в ряду)
    for (let i = 1; i <= totalItems; i++) {
        const hole = document.createElement('div');
        hole.className = 'hole';
        hole.innerText = i;
        hole.dataset.num = i;
        
        const row = Math.floor((i - 1) / 6);
        const col = (i - 1) % 6;
        hole.style.left = (12 + col * 54) + 'px';
        hole.style.top = (15 + row * 50) + 'px';
        
        box.appendChild(hole);
    }

    // Находим нижнюю границу сетки лунок, чтобы свалить шарики еще ниже
    const ballsStartTop = Math.ceil(totalItems / 6) * 50 + 30;

    // 2. Генерируем 100 шариков в случайном порядке внизу прокручиваемого поля
    for (let i = 1; i <= totalItems; i++) {
        const ball = document.createElement('div');
        ball.className = 'shape';
        ball.innerText = i;
        ball.dataset.num = i;
        ball.style.background = colors[i % colors.length];
        
        // Случайный разброс в самом низу под сеткой
        const randomX = Math.floor(Math.random() * 280) + 10;
        const randomY = Math.floor(Math.random() * 250) + ballsStartTop; 
        ball.style.left = randomX + 'px';
        ball.style.top = randomY + 'px';
        
        // Запоминаем стартовые позиции на случай возврата фишки при ошибке порядка
        ball.dataset.startX = ball.style.left;
        ball.dataset.startY = ball.style.top;
        
        box.appendChild(ball);
        ball.addEventListener('pointerdown', onPointerDown);
    }

    function onPointerDown(e) {
        const ball = e.currentTarget;
        if (ball.dataset.placed) return;
        
        ball.style.cursor = 'grabbing';
        ball.style.zIndex = 100;
        ball.setPointerCapture(e.pointerId);
        
        const boxRect = box.getBoundingClientRect();
        
        // Учитываем скролл контейнера при захвате
        const startX = e.clientX - ball.getBoundingClientRect().left;
        const startY = e.clientY - ball.getBoundingClientRect().top;

        function onPointerMove(ev) {
            // Рассчитываем координаты внутри поля с учетом прокрутки box.scrollTop
            let x = ev.clientX - boxRect.left - startX + box.scrollLeft;
            let y = ev.clientY - boxRect.top - startY + box.scrollTop;
            
            ball.style.left = x + 'px';
            ball.style.top = y + 'px';
        }

        function onPointerUp(ev) {
            ball.removeEventListener('pointermove', onPointerMove);
            ball.removeEventListener('pointerup', onPointerUp);
            ball.style.cursor = 'grab';
            ball.style.zIndex = 10;
            
            const currentNum = parseInt(ball.dataset.num);
            const holes = document.querySelectorAll('.hole');
            let placedSuccessfully = false;
            
            holes.forEach(hole => {
                if (hole.dataset.num === ball.dataset.num) {
                    const hRect = hole.getBoundingClientRect();
                    const bRect = ball.getBoundingClientRect();
                    
                    const distance = Math.hypot(
                        (hRect.left + hRect.width/2) - (bRect.left + bRect.width/2),
                        (hRect.top + hRect.height/2) - (bRect.top + bRect.height/2)
                    );
                    
                    // Если пододвинули близко к своей лунке
                    if (distance < 25) {
                        // ГЛАВНАЯ ПРОВЕРКА ПОРЯДКА: совпадает ли номер с нужным по очереди?
                        if (currentNum === nextRequiredNum) {
                            ball.style.left = (hole.offsetLeft + 1) + 'px';
                            ball.style.top = (hole.offsetTop + 1) + 'px';
                            ball.dataset.placed = "true";
                            ball.style.cursor = 'default';
                            ball.style.boxShadow = 'none';
                            
                            nextRequiredNum++; // Запрашиваем следующее число
                            placedSuccessfully = true;
                            
                            if (nextRequiredNum <= totalItems) {
                                document.getElementById('status').innerText = "Ждем шарик номер: " + nextRequiredNum;
                            } else {
                                document.getElementById('status').style.display = 'none';
                                document.getElementById('win').style.display = 'block';
                            }
                        }
                    }
                }
            });
            
            // Если игрок бросил шарик мимо или нарушил порядок — возвращаем шарик на его исходное место
            if (!placedSuccessfully) {
                ball.style.left = ball.dataset.startX;
                ball.style.top = ball.dataset.startY;
            }
        }

        ball.addEventListener('pointermove', onPointerMove);
        ball.addEventListener('pointerup', onPointerUp);
    }
</script>
"""

# Отрисовываем увеличенное поле игры
st.components.v1.html(game_code, height=660)

st.write("---")
st.write("Проект усложнен по ТЗ заказчика 😎 Работает на телефоне!")
