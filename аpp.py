import streamlit as st

st.title("🧩 Мини-игра: Расставь фигурки!")
st.write("Перетащи фигурки пальцем или мышкой в правильные отверстия!")

# Наш интерактивный игровой блок на HTML/JS
game_code = """
<style>
    .game-container { display: flex; flex-direction: column; align-items: center; gap: 30px; font-family: sans-serif; }
    .row { display: flex; justify-content: center; gap: 20px; width: 100%; }
    
    /* Стили для дырок в стене */
    .hole { width: 80px; height: 80px; background: #3a3a3a; border: 3px dashed #777; display: flex; align-items: center; justify-content: center; position: relative; }
    .hole-square { border-radius: 8px; }
    .hole-circle { border-radius: 50%; }
    .hole-triangle { width: 0; height: 0; background: transparent; border-left: 40px solid transparent; border-right: 40px solid transparent; border-bottom: 80px solid #3a3a3a; border-style: none none dashed none; }
    
    /* Стили для фигурок */
    .shape { width: 70px; height: 70px; cursor: grab; touch-action: none; position: absolute; z-index: 10; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; }
    .square { background: #ff4b4b; border-radius: 8px; left: 20px; top: 150px; }
    .circle { background: #1c83e1; border-radius: 50%; left: 120px; top: 150px; }
    .triangle { width: 0; height: 0; background: transparent; border-left: 35px solid transparent; border-right: 35px solid transparent; border-bottom: 70px solid #00c04b; left: 220px; top: 150px; cursor: grab; }
    
    .text-inside { position: absolute; top: 40px; left: -25px; width: 50px; text-align: center; color: white; font-size: 10px; font-family: sans-serif; }
    
    #box { width: 320px; height: 250px; background: #222; border-radius: 15px; position: relative; border: 2px solid #444; }
    .win-message { display: none; color: #00c04b; font-size: 20px; font-weight: bold; margin-top: 10px; }
</style>

<div class="game-container">
    <div id="box">
        <!-- Места-дырки -->
        <div class="hole hole-square" style="left: 30px; top: 30px;" data-shape="square"></div>
        <div class="hole hole-circle" style="left: 120px; top: 30px;" data-shape="circle"></div>
        <div class="hole" style="left: 210px; top: 30px; background:transparent; border:none;" data-shape="triangle">
            <div class="hole-triangle"></div>
        </div>

        <!-- Сами фигурки -->
        <div class="shape square" id="sq" data-shape="square">Куб</div>
        <div class="shape circle" id="ci" data-shape="circle">Круг</div>
        <div class="shape triangle" id="tr" data-shape="triangle"><span class="text-inside">Триуг</span></div>
    </div>
    <div class="win-message" id="win">🎉 Ты победил! Все фигуры на месте!</div>
</div>

<script>
    const shapes = document.querySelectorAll('.shape');
    const holes = document.querySelectorAll('.hole');
    let successCount = 0;

    shapes.forEach(shape => {
        shape.addEventListener('pointerdown', onPointerDown);
    });

    function onPointerDown(e) {
        const shape = e.currentTarget;
        if (shape.dataset.placed) return;
        
        shape.style.cursor = 'grabbing';
        shape.setPointerCapture(e.pointerId);
        
        const box = document.getElementById('box').getBoundingClientRect();
        const startX = e.clientX - shape.getBoundingClientRect().left;
        const startY = e.clientY - shape.getBoundingClientRect().top;

        function onPointerMove(ev) {
            let x = ev.clientX - box.left - startX;
            let y = ev.clientY - box.top - startY;
            
            // Если это треугольник, у него немного другая физика сдвига из-за границ
            if(shape.classList.contains('triangle')) {
                shape.style.left = x + 'px';
                shape.style.top = y + 'px';
            } else {
                shape.style.left = x + 'px';
                shape.style.top = y + 'px';
            }
        }

        function onPointerUp(ev) {
            shape.removeEventListener('pointermove', onPointerMove);
            shape.removeEventListener('pointerup', onPointerUp);
            shape.style.cursor = 'grab';
            
            // Проверка попадания в нужную дырку
            holes.forEach(hole => {
                if (hole.dataset.shape === shape.dataset.shape) {
                    const hRect = hole.getBoundingClientRect();
                    const sRect = shape.getBoundingClientRect();
                    
                    const distance = Math.hypot(
                        (hRect.left + hRect.width/2) - (sRect.left + sRect.width/2),
                        (hRect.top + hRect.height/2) - (sRect.top + sRect.height/2)
                    );
                    
                    // Если пододвинули близко к дырке (ближе 25 пикселей)
                    if (distance < 25) {
                        const boxRect = document.getElementById('box').getBoundingClientRect();
                        shape.style.left = (hRect.left - boxRect.left + (hRect.width - sRect.width)/2) + 'px';
                        shape.style.top = (hRect.top - boxRect.top + (hRect.height - sRect.height)/2) + 'px';
                        shape.dataset.placed = "true";
                        shape.style.cursor = 'default';
                        successCount++;
                        
                        if (successCount === 3) {
                            document.getElementById('win').style.display = 'block';
                        }
                    }
                }
            });
        }

        shape.addEventListener('pointermove', onPointerMove);
        shape.addEventListener('pointerup', onPointerUp);
    }
</script>
"""

# Запускаем код игры внутри нашего сайта
st.components.v1.html(game_code, height=350)

st.write("---")
st.write("Спасибо за внимание! Делаю всё на телефоне 📱")
