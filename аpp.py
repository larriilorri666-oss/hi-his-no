import streamlit as st

st.title("🧩 Мега-пазл: Разложи 20 чисел!")
st.write("Перетащи все 20 шариков в лунки с соответствующими номерами!")

# Магия генерации 20 штук через HTML и JavaScript
game_code = """
<style>
    .game-container { display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }
    #box { width: 100%; max-width: 340px; height: 530px; background: #222; border-radius: 15px; position: relative; border: 2px solid #444; overflow: hidden; }
    
    /* Стили для 20 лунок */
    .hole { width: 45px; height: 45px; background: #3a3a3a; border: 2px dashed #666; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: absolute; color: #888; font-size: 14px; font-weight: bold; }
    
    /* Стили для 20 шариков */
    .shape { width: 42px; height: 42px; border-radius: 50%; cursor: grab; touch-action: none; position: absolute; z-index: 10; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    
    .win-message { display: none; color: #00c04b; font-size: 22px; font-weight: bold; margin-top: 15px; text-align: center; }
</style>

<div class="game-container">
    <div id="box">
        <!-- Сюда JavaScript сам добавит 20 лунок и 20 шариков -->
    </div>
    <div class="win-message" id="win">🎉 Потрясающе! Все 20 чисел на своих местах!</div>
</div>

<script>
    const box = document.getElementById('box');
    let successCount = 0;
    const totalItems = 20;

    // Цвета для шариков, чтобы они были весёлыми и разноцветными
    const colors = ['#ff4b4b', '#1c83e1', '#00c04b', '#f9a825', '#9c27b0', '#00bcd4', '#e91e63', '#4caf50'];

    // 1. Автоматически создаем 20 лунок (4 ряда по 5 штук вверху поля)
    for (let i = 1; i <= totalItems; i++) {
        const hole = document.createElement('div');
        hole.className = 'hole';
        hole.innerText = i;
        hole.dataset.num = i;
        
        // Считаем координаты сетки
        const row = Math.floor((i - 1) / 5);
        const col = (i - 1) % 5;
        hole.style.left = (15 + col * 64) + 'px';
        hole.style.top = (20 + row * 60) + 'px';
        
        box.appendChild(hole);
    }

    // 2. Автоматически создаем 20 шариков внизу поля в случайном порядке
    for (let i = 1; i <= totalItems; i++) {
        const ball = document.createElement('div');
        ball.className = 'shape';
        ball.innerText = i;
        ball.dataset.num = i;
        ball.style.background = colors[i % colors.length];
        
        // Случайный разброс в нижней части экрана, чтобы они не слиплись
        const randomX = Math.floor(Math.random() * 270) + 10;
        const randomY = Math.floor(Math.random() * 180) + 300; 
        ball.style.left = randomX + 'px';
        ball.style.top = randomY + 'px';
        
        box.appendChild(ball);
        
        // Подключаем физику движения пальца к каждому шарику
        ball.addEventListener('pointerdown', onPointerDown);
    }

    function onPointerDown(e) {
        const ball = e.currentTarget;
        if (ball.dataset.placed) return;
        
        ball.style.cursor = 'grabbing';
        ball.style.zIndex = 100; // Тащим поверх остальных
        ball.setPointerCapture(e.pointerId);
        
        const boxRect = box.getBoundingClientRect();
        const startX = e.clientX - ball.getBoundingClientRect().left;
        const startY = e.clientY - ball.getBoundingClientRect().top;

        function onPointerMove(ev) {
            let x = ev.clientX - boxRect.left - startX;
            let y = ev.clientY - boxRect.top - startY;
            
            // Ограничиваем движение внутри стенок коробки
            x = Math.max(0, Math.min(x, boxRect.width - 42));
            y = Math.max(0, Math.min(y, boxRect.height - 42));
            
            ball.style.left = x + 'px';
            ball.style.top = y + 'px';
        }

        function onPointerUp(ev) {
            ball.removeEventListener('pointermove', onPointerMove);
            ball.removeEventListener('pointerup', onPointerUp);
            ball.style.cursor = 'grab';
            ball.style.zIndex = 10;
            
            const holes = document.querySelectorAll('.hole');
            
            holes.forEach(hole => {
                if (hole.dataset.num === ball.dataset.num) {
                    const hRect = hole.getBoundingClientRect();
                    const bRect = ball.getBoundingClientRect();
                    
                    // Считаем расстояние между центром шарика и лункой
                    const distance = Math.hypot(
                        (hRect.left + hRect.width/2) - (bRect.left + bRect.width/2),
                        (hRect.top + hRect.height/2) - (bRect.top + bRect.height/2)
                    );
                    
                    // Если пододвинули близко к своей лунке
                    if (distance < 25) {
                        ball.style.left = (hole.offsetLeft + 1) + 'px';
                        ball.style.top = (hole.offsetTop + 1) + 'px';
                        ball.dataset.placed = "true";
                        ball.style.cursor = 'default';
                        ball.style.boxShadow = 'none';
                        successCount++;
                        
                        if (successCount === totalItems) {
                            document.getElementById('win').style.display = 'block';
                        }
                    }
                }
            });
        }

        ball.addEventListener('pointermove', onPointerMove);
        ball.addEventListener('pointerup', onPointerUp);
    }
</script>
"""

# Запуск игрового компонента
st.components.v1.html(game_code, height=570)

st.write("---")
st.write("Создано юным разработчиком на мобильном телефоне 📱")

