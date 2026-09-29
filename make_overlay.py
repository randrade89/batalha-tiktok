import os

overlay = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Overlay Batalha TikTok Live</title>
  <script src="/socket.io/socket.io.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,800;0,900;1,900&family=Oswald:wght@700&display=swap');
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body {
      background: transparent !important;
      font-family: 'Montserrat', sans-serif;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      position: relative;
      color: #fff;
    }
    .screen-container {
      width: 100%;
      height: 100%;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 24px 20px;
    }
    .battle-header {
      background: rgba(10, 10, 20, 0.88);
      border: 3px solid rgba(255, 255, 255, 0.2);
      border-radius: 24px;
      padding: 16px 20px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), 0 0 30px rgba(255, 215, 0, 0.3);
      backdrop-filter: blur(10px);
      z-index: 100;
    }
    .battle-title {
      text-align: center;
      font-size: 24px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      background: linear-gradient(90deg, #ff2222, #ffeb3b);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 0 0 20px rgba(255, 50, 50, 0.6);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
    }
    .scores-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      padding: 0 10px;
    }
    .team-badge { display: flex; align-items: center; gap: 12px; }
    .team-badge.red { color: #ff3b30; }
    .team-badge.yellow { color: #ffd60a; flex-direction: row-reverse; }
    .team-name { font-size: 22px; font-weight: 900; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.9); }
    .team-score { font-size: 46px; font-weight: 900; font-family: 'Oswald', sans-serif; text-shadow: 0 0 15px currentColor; }
    .vs-tag {
      font-size: 26px;
      font-style: italic;
      font-weight: 900;
      color: #ffffff;
      background: #ff0055;
      padding: 4px 14px;
      border-radius: 12px;
      box-shadow: 0 0 15px #ff0055;
      animation: pulse 1.5s infinite;
    }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
    .progress-track {
      width: 100%;
      height: 38px;
      background: #111;
      border-radius: 19px;
      overflow: hidden;
      position: relative;
      border: 3px solid #222;
      box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.9);
      display: flex;
    }
    .progress-red {
      height: 100%;
      background: linear-gradient(90deg, #b30000, #ff1a1a);
      transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      display: flex;
      align-items: center;
      justify-content: flex-start;
      padding-left: 15px;
      font-weight: 900;
      font-size: 18px;
      text-shadow: 0 2px 5px #000;
      box-shadow: 0 0 20px rgba(255, 30, 30, 0.8);
    }
    .progress-yellow {
      height: 100%;
      background: linear-gradient(90deg, #ffcc00, #ff9900);
      transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding-right: 15px;
      font-weight: 900;
      font-size: 18px;
      color: #000;
      text-shadow: 0 1px 2px rgba(255, 255, 255, 0.6);
      box-shadow: 0 0 20px rgba(255, 204, 0, 0.8);
    }
    .spark {
      position: absolute;
      top: -5px;
      bottom: -5px;
      width: 10px;
      background: #fff;
      box-shadow: 0 0 25px 8px #fff, 0 0 40px 15px #ffea00;
      z-index: 10;
      transform: translateX(-50%);
      border-radius: 5px;
      animation: flicker 0.2s infinite;
    }
    @keyframes flicker { 0%, 100% { opacity: 1; } 50% { opacity: 0.8; } }
    .shirts-layer {
      position: absolute;
      top: 240px;
      left: 20px;
      right: 20px;
      display: flex;
      justify-content: space-between;
      pointer-events: none;
      z-index: 80;
    }
    .shirt-card {
      width: 250px;
      background: rgba(15, 15, 25, 0.85);
      border-radius: 20px;
      padding: 14px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(8px);
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      border: 3px solid;
      position: relative;
    }
    .shirt-card.red-side { border-color: #ff3b30; box-shadow: 0 0 25px rgba(255, 59, 48, 0.4); }
    .shirt-card.yellow-side { border-color: #ffd60a; box-shadow: 0 0 25px rgba(255, 214, 10, 0.4); }
    .sacola-badge {
      position: absolute;
      top: -12px;
      background: #ff5722;
      color: #fff;
      font-size: 13px;
      font-weight: 900;
      padding: 4px 10px;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
      text-transform: uppercase;
    }
    .shirt-img {
      width: 140px;
      height: 140px;
      object-fit: contain;
      margin: 8px 0;
      filter: drop-shadow(0 8px 12px rgba(0, 0, 0, 0.6));
    }
    .shirt-title { font-size: 15px; font-weight: 900; text-transform: uppercase; margin-bottom: 8px; }
    .instructions-box {
      width: 100%;
      background: rgba(0, 0, 0, 0.5);
      border-radius: 12px;
      padding: 8px 6px;
      font-size: 12px;
      font-weight: 800;
      display: flex;
      flex-direction: column;
      gap: 5px;
      text-align: left;
    }
    .inst-row { display: flex; align-items: center; justify-content: space-between; padding: 2px 4px; }
    .inst-row.comment { color: #e0e0e0; }
    .inst-row.gift { color: #ff99ff; }
    .inst-row.purchase {
      background: linear-gradient(90deg, #ff5722, #ff9800);
      color: #fff;
      font-weight: 900;
      padding: 4px 6px;
      border-radius: 6px;
      box-shadow: 0 0 10px rgba(255, 87, 34, 0.6);
      animation: pulse 1.5s infinite;
    }
    .bottom-section { z-index: 100; display: flex; flex-direction: column; gap: 15px; }
    .recent-feed {
      height: 110px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      gap: 8px;
      overflow: hidden;
      pointer-events: none;
    }
    .feed-item {
      background: rgba(10, 10, 20, 0.88);
      border-radius: 30px;
      padding: 8px 18px;
      font-size: 15px;
      font-weight: 800;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      align-self: center;
      border: 2px solid;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.7);
      animation: slideUp 0.3s ease-out forwards;
    }
    .feed-item.red { border-color: #ff3b30; color: #ffb3b0; }
    .feed-item.yellow { border-color: #ffd60a; color: #fff4b0; }
    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .cta-banner {
      background: linear-gradient(90deg, #ff0055, #ff5500, #ffaa00);
      border-radius: 20px;
      padding: 16px 20px;
      text-align: center;
      box-shadow: 0 8px 30px rgba(255, 0, 85, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 15px;
      border: 3px solid #fff;
    }
    .cta-bag-icon { font-size: 38px; }
    .cta-text-box h3 { font-size: 22px; font-weight: 900; text-transform: uppercase; }
    .cta-text-box p { font-size: 15px; font-weight: 800; color: #fff; }
    .super-purchase-modal {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) scale(0);
      width: 90%;
      max-width: 500px;
      background: rgba(10, 10, 20, 0.96);
      border-radius: 30px;
      padding: 30px 20px;
      text-align: center;
      border: 5px solid #ffcc00;
      box-shadow: 0 0 60px rgba(255, 204, 0, 0.9), 0 0 100px rgba(255, 0, 0, 0.7);
      z-index: 1000;
      transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      pointer-events: none;
    }
    .super-purchase-modal.active { transform: translate(-50%, -50%) scale(1); }
    .modal-tag { font-size: 26px; font-weight: 900; text-transform: uppercase; color: #ffea00; margin-bottom: 15px; }
    .modal-buyer { font-size: 32px; font-weight: 900; color: #fff; margin-bottom: 8px; }
    .modal-shirt { font-size: 22px; font-weight: 800; color: #00ffcc; margin-bottom: 20px; }
    .modal-boost {
      font-size: 54px;
      font-weight: 900;
      font-family: 'Oswald', sans-serif;
      background: linear-gradient(90deg, #ff0055, #ffcc00);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: pulse 0.8s infinite;
    }
  </style>
</head>
<body>
  <div class="screen-container">
    <div class="battle-header">
      <div class="battle-title">
        <span>⚔️</span>
        <span>BATALHA ELEIÇÕES: QUEM VENCE?</span>
        <span>⚔️</span>
      </div>
      <div class="scores-row">
        <div class="team-badge red">
          <div>
            <div class="team-name">LULA (13)</div>
            <div class="team-score" id="redScore">50</div>
          </div>
        </div>
        <div class="vs-tag">VS</div>
        <div class="team-badge yellow">
          <div style="text-align: right;">
            <div class="team-name">BOLSONARO (22)</div>
            <div class="team-score" id="yellowScore">50</div>
          </div>
        </div>
      </div>
      <div class="progress-track">
        <div class="progress-red" id="redBar" style="width: 50%;">
          <span id="redPercent">50%</span>
        </div>
        <div class="spark" id="spark" style="left: 50%;"></div>
        <div class="progress-yellow" id="yellowBar" style="width: 50%;">
          <span id="yellowPercent">50%</span>
        </div>
      </div>
    </div>
    <div class="shirts-layer">
      <div class="shirt-card red-side">
        <div class="sacola-badge">SACOLA ITEM #1</div>
        <img src="/images/camisa_vermelha.png" alt="Camisa Vermelha" class="shirt-img">
        <div class="shirt-title" style="color: #ff4d4d;">CAMISA BRASIL 13</div>
        <div class="instructions-box">
          <div class="inst-row comment"><span>💬 Digite LULA / PT:</span><span style="color: #ff4d4d;">+1 Pt</span></div>
          <div class="inst-row gift"><span>🌹 Envie ROSA:</span><span style="color: #ff80df;">+5 Pts</span></div>
          <div class="inst-row purchase"><span>🛍️ COMPRE A CAMISA:</span><span>+50 PTS!</span></div>
        </div>
      </div>
      <div class="shirt-card yellow-side">
        <div class="sacola-badge" style="background: #ffb300; color: #000;">SACOLA ITEM #2</div>
        <img src="/images/camisa_amarela.png" alt="Camisa Amarela" class="shirt-img">
        <div class="shirt-title" style="color: #ffd60a;">ACORDA BRASIL 22</div>
        <div class="instructions-box">
          <div class="inst-row comment"><span>💬 Digite MITO / 22:</span><span style="color: #ffd60a;">+1 Pt</span></div>
          <div class="inst-row gift"><span>🎁 Envie 1 MOEDA:</span><span style="color: #ffd60a;">+5 Pts</span></div>
          <div class="inst-row purchase"><span>🛍️ COMPRE A CAMISA:</span><span>+50 PTS!</span></div>
        </div>
      </div>
    </div>
    <div class="bottom-section">
      <div class="recent-feed" id="feed"></div>
      <div class="cta-banner">
        <div class="cta-bag-icon">🛍️</div>
        <div class="cta-text-box">
          <h3>COMPRE NA SACOLA E ATIVE O SUPER BOOST!</h3>
          <p>Cada compra na sacola dá <strong>+50 PONTOS</strong> direto pro seu time!</p>
        </div>
      </div>
    </div>
  </div>
  <div class="super-purchase-modal" id="purchaseModal">
    <div class="modal-tag">🎉 SUPER COMPRA CONFIRMADA! 🎉</div>
    <div class="modal-buyer" id="modalBuyer">Nome do Comprador</div>
    <div class="modal-shirt" id="modalShirt">Comprou a Camisa Vermelha</div>
    <div class="modal-boost">+50 PONTOS! 💥</div>
  </div>
  <script>
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const audioCtx = AudioContext ? new AudioContext() : null;
    function playDing() {
      if (!audioCtx) return;
      try {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.25);
      } catch (e) {}
    }
    function playFanfare() {
      if (!audioCtx) return;
      try {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((freq, idx) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, audioCtx.currentTime + idx * 0.12);
          gain.gain.setValueAtTime(0.4, audioCtx.currentTime + idx * 0.12);
          gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + idx * 0.12 + 0.4);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(audioCtx.currentTime + idx * 0.12);
          osc.stop(audioCtx.currentTime + idx * 0.12 + 0.4);
        });
      } catch (e) {}
    }
    const socket = io();
    const redScoreEl = document.getElementById('redScore');
    const yellowScoreEl = document.getElementById('yellowScore');
    const redBarEl = document.getElementById('redBar');
    const yellowBarEl = document.getElementById('yellowBar');
    const redPercentEl = document.getElementById('redPercent');
    const yellowPercentEl = document.getElementById('yellowPercent');
    const sparkEl = document.getElementById('spark');
    const feedEl = document.getElementById('feed');
    const purchaseModalEl = document.getElementById('purchaseModal');
    const modalBuyerEl = document.getElementById('modalBuyer');
    const modalShirtEl = document.getElementById('modalShirt');
    function updateDisplay(scores) {
      const red = scores.red || 0;
      const yellow = scores.yellow || 0;
      const total = red + yellow;
      redScoreEl.innerText = red;
      yellowScoreEl.innerText = yellow;
      let pRed = 50;
      let pYellow = 50;
      if (total > 0) {
        pRed = Math.round((red / total) * 100);
        pYellow = 100 - pRed;
      }
      redBarEl.style.width = pRed + '%';
      yellowBarEl.style.width = pYellow + '%';
      sparkEl.style.left = pRed + '%';
      redPercentEl.innerText = pRed + '%';
      yellowPercentEl.innerText = pYellow + '%';
    }
    function addFeedItem(event) {
      if (!event || event.team === 'both') return;
      const item = document.createElement('div');
      item.className = 'feed-item ' + (event.team === 'red' ? 'red' : 'yellow');
      const icon = event.team === 'red' ? '🔴' : '🟡';
      item.innerHTML = '<span>' + icon + ' <strong>@' + event.user + '</strong>: ' + event.reason + '</span> <strong style="color:#fff;">(+' + event.amount + ')</strong>';
      feedEl.appendChild(item);
      if (feedEl.children.length > 3) {
        feedEl.removeChild(feedEl.children[0]);
      }
      setTimeout(() => {
        if (item.parentNode) item.parentNode.removeChild(item);
      }, 4000);
      playDing();
    }
    socket.on('init_state', state => {
      if (state && state.scores) updateDisplay(state.scores);
    });
    socket.on('score_updated', data => {
      updateDisplay(data.scores);
      addFeedItem(data.event);
    });
    socket.on('super_purchase', data => {
      modalBuyerEl.innerText = data.user;
      modalShirtEl.innerText = 'Comprou: ' + data.shirtName;
      purchaseModalEl.className = 'super-purchase-modal active';
      playFanfare();
      setTimeout(() => {
        purchaseModalEl.className = 'super-purchase-modal';
      }, 5500);
    });
  </script>
</body>
</html>
"""

with open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\overlay.html", "w", encoding="utf-8") as f:
    f.write(overlay)
print("Overlay generated!")