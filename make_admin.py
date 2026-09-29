import os

admin = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel de Controle - Batalha TikTok Live</title>
  <script src="/socket.io/socket.io.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800;900&display=swap');
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0f111a;
      color: #f0f2f5;
      font-family: 'Montserrat', sans-serif;
      padding: 24px;
    }
    .container {
      max-width: 1100px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #1a1d2e;
      padding: 20px 24px;
      border-radius: 16px;
      border: 1px solid #2d314d;
    }
    h1 { font-size: 24px; font-weight: 900; }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 16px;
      border-radius: 20px;
      font-weight: 800;
      font-size: 14px;
    }
    .status-badge.connected { background: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; }
    .status-badge.connecting { background: rgba(241, 196, 15, 0.2); color: #f1c40f; border: 1px solid #f1c40f; }
    .status-badge.disconnected { background: rgba(231, 76, 60, 0.2); color: #e74c3c; border: 1px solid #e74c3c; }

    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }
    .card {
      background: #1a1d2e;
      border-radius: 16px;
      padding: 20px;
      border: 1px solid #2d314d;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .card-title {
      font-size: 18px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .form-row {
      display: flex;
      gap: 10px;
    }
    input[type="text"] {
      flex: 1;
      background: #0f111a;
      border: 1px solid #3d426b;
      color: #fff;
      padding: 12px 16px;
      border-radius: 10px;
      font-size: 15px;
      font-family: inherit;
    }
    input[type="text"]:focus {
      outline: none;
      border-color: #ff0055;
    }
    button {
      cursor: pointer;
      font-family: inherit;
      font-weight: 800;
      padding: 12px 20px;
      border-radius: 10px;
      border: none;
      transition: all 0.2s;
    }
    button:hover { opacity: 0.9; transform: translateY(-2px); }
    button:active { transform: translateY(0); }
    .btn-primary { background: #3b82f6; color: #fff; }
    .btn-danger { background: #ef4444; color: #fff; }
    .btn-success { background: #10b981; color: #fff; }
    .btn-warning { background: #f59e0b; color: #000; }
    .btn-copy { background: #8b5cf6; color: #fff; }

    /* Times */
    .teams-battle-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }
    .team-box {
      border-radius: 16px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      text-align: center;
    }
    .team-box.red-box {
      background: rgba(239, 68, 68, 0.1);
      border: 2px solid #ef4444;
    }
    .team-box.yellow-box {
      background: rgba(245, 158, 11, 0.1);
      border: 2px solid #f59e0b;
    }
    .team-box h2 { font-size: 22px; font-weight: 900; }
    .team-box .score-val {
      font-size: 52px;
      font-weight: 900;
      line-height: 1;
    }
    .btn-super-boost {
      padding: 18px 24px;
      font-size: 18px;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
      animation: pulse-btn 2s infinite;
    }
    @keyframes pulse-btn {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.02); }
    }
    .btn-super-boost.red {
      background: linear-gradient(90deg, #dc2626, #ef4444);
      color: #fff;
    }
    .btn-super-boost.yellow {
      background: linear-gradient(90deg, #d97706, #f59e0b);
      color: #000;
    }
    .quick-actions {
      display: flex;
      gap: 8px;
      justify-content: center;
    }
    .quick-actions button {
      padding: 8px 14px;
      font-size: 14px;
      background: #2d314d;
      color: #fff;
    }

    /* Logs */
    .logs-box {
      background: #0f111a;
      border-radius: 10px;
      padding: 12px;
      height: 200px;
      overflow-y: auto;
      font-family: monospace;
      font-size: 13px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .log-line {
      padding: 4px 8px;
      border-radius: 6px;
      background: #1a1d2e;
    }
    .log-line.red { color: #fca5a5; border-left: 3px solid #ef4444; }
    .log-line.yellow { color: #fde68a; border-left: 3px solid #f59e0b; }

    .url-display {
      background: #0f111a;
      border: 1px dashed #4b5280;
      border-radius: 10px;
      padding: 12px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div>
        <h1>⚔️ Painel de Controle - Batalha de Camisas</h1>
        <p style="color: #9ca3af; font-size: 14px; margin-top: 4px;">Gerenciamento em tempo real do TikTok Live Studio</p>
      </div>
      <div id="statusBadge" class="status-badge disconnected">
        <span id="statusDot">●</span>
        <span id="statusText">Desconectado</span>
      </div>
    </header>

    <!-- Conexao com o TikTok Live -->
    <div class="card">
      <div class="card-title">📡 Conexão com o TikTok Live</div>
      <div class="form-row">
        <input type="text" id="tiktokUser" placeholder="Seu @ de usuário no TikTok (ex: andradeindicai)" value="andradeindicai">
        <button id="btnConnect" class="btn-success">Conectar na Live</button>
        <button id="btnDisconnect" class="btn-danger">Desconectar</button>
      </div>
    </div>

    <!-- Link do Overlay para o TikTok Live Studio -->
    <div class="card">
      <div class="card-title">📺 Link para adicionar no TikTok LIVE Studio (Browser Source)</div>
      <div class="url-display">
        <code id="overlayUrl" style="color: #a78bfa; font-weight: 700; font-size: 15px;">http://localhost:3000/overlay.html</code>
        <button id="btnCopyUrl" class="btn-copy">📋 Copiar Link</button>
      </div>
      <p style="color: #9ca3af; font-size: 13px;">
        💡 <strong>Como usar no TikTok LIVE Studio:</strong> Clique em <em>Adicionar Fonte</em> ➔ Escolha <em>Link do Navegador</em> ➔ Cole o link acima ➔ Defina Resolução <strong>1080 x 1920</strong> (ou ajuste no canvas) ➔ Pronto! Fundo já é 100% transparente.
      </p>
    </div>

    <!-- Times e Super Boost (+50 Pontos) -->
    <div class="teams-battle-row">
      <!-- TIME VERMELHO -->
      <div class="team-box red-box">
        <h2 style="color: #ef4444;">🔴 TIME VERMELHO (Lula / PT 13)</h2>
        <div class="score-val" id="adminRedScore" style="color: #ef4444;">50</div>
        <p style="font-weight: 700; font-size: 14px;">Camisa Brasil Vermelho (Sacola #1)</p>
        <button id="btnBuyRed" class="btn-super-boost red">
          🛍️ COMPRA NA SACOLA (+50 PTS) 💥
        </button>
        <div class="quick-actions">
          <button onclick="addManual('red', 1, 'Comentário manual')">+1 Pt</button>
          <button onclick="addManual('red', 5, 'Presente manual Rosa')">+5 Pts</button>
          <button onclick="addManual('red', 10, 'Super presente')">+10 Pts</button>
          <button onclick="addManual('red', -5, 'Correção')">-5 Pts</button>
        </div>
      </div>

      <!-- TIME AMARELO -->
      <div class="team-box yellow-box">
        <h2 style="color: #f59e0b;">🟡 TIME AMARELO (Bolsonaro 22)</h2>
        <div class="score-val" id="adminYellowScore" style="color: #f59e0b;">50</div>
        <p style="font-weight: 700; font-size: 14px;">Camisa Acorda Brasil (Sacola #2)</p>
        <button id="btnBuyYellow" class="btn-super-boost yellow">
          🛍️ COMPRA NA SACOLA (+50 PTS) 💥
        </button>
        <div class="quick-actions">
          <button onclick="addManual('yellow', 1, 'Comentário manual')">+1 Pt</button>
          <button onclick="addManual('yellow', 5, 'Presente manual 1 Moeda')">+5 Pts</button>
          <button onclick="addManual('yellow', 10, 'Super presente')">+10 Pts</button>
          <button onclick="addManual('yellow', -5, 'Correção')">-5 Pts</button>
        </div>
      </div>
    </div>

    <!-- Ferramentas de Teste e Reset -->
    <div class="grid-2">
      <!-- Simulador de Teste Offline -->
      <div class="card">
        <div class="card-title">🧪 Testar Antes da Live (Simulador)</div>
        <p style="color: #9ca3af; font-size: 13px;">Clique para ver as animações, alertas e sons funcionando no overlay sem precisar estar ao vivo:</p>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          <button onclick="testAction('red', 'comment', 'Lula 13 meu voto!')" class="btn-primary" style="background: #dc2626;">💬 Testar Chat Vermelho (+1)</button>
          <button onclick="testAction('yellow', 'comment', 'Mito 22 acorda brasil!')" class="btn-primary" style="background: #d97706;">💬 Testar Chat Amarelo (+1)</button>
          <button onclick="testAction('red', 'gift', 'Rosa 🌹')" class="btn-primary" style="background: #be185d;">🌹 Testar Rosa (+5)</button>
          <button onclick="testAction('yellow', 'gift', 'TikTok 🎁')" class="btn-primary" style="background: #ca8a04;">🎁 Testar Presente Amarelo (+5)</button>
        </div>
      </div>

      <!-- Gerenciamento da Partida -->
      <div class="card">
        <div class="card-title">⚙️ Gerenciar Placar</div>
        <p style="color: #9ca3af; font-size: 13px;">Reiniciar placar para o início da live ou nova rodada:</p>
        <div>
          <button id="btnReset" class="btn-danger" style="width: 100%; padding: 14px;">🔄 REINICIAR PLACAR (50 VS 50)</button>
        </div>
      </div>
    </div>

    <!-- Log de Eventos -->
    <div class="card">
      <div class="card-title">📜 Registro de Atividades e Comentários Pontuados</div>
      <div class="logs-box" id="logsBox">
        <div class="log-line">Sistema iniciado. Aguardando conexão...</div>
      </div>
    </div>
  </div>

  <script>
    const socket = io();

    const statusBadge = document.getElementById('statusBadge');
    const statusText = document.getElementById('statusText');
    const adminRedScore = document.getElementById('adminRedScore');
    const adminYellowScore = document.getElementById('adminYellowScore');
    const logsBox = document.getElementById('logsBox');
    const tiktokUser = document.getElementById('tiktokUser');

    // Atualizar URL com porta atual
    document.getElementById('overlayUrl').innerText = window.location.origin + '/overlay.html';

    document.getElementById('btnCopyUrl').addEventListener('click', () => {
      navigator.clipboard.writeText(window.location.origin + '/overlay.html');
      alert('Link do Overlay copiado com sucesso! Cole no TikTok LIVE Studio.');
    });

    document.getElementById('btnConnect').addEventListener('click', () => {
      const u = tiktokUser.value.trim();
      if (u) {
        socket.emit('connect_tiktok', { username: u });
      }
    });

    document.getElementById('btnDisconnect').addEventListener('click', () => {
      socket.emit('disconnect_tiktok');
    });

    document.getElementById('btnBuyRed').addEventListener('click', () => {
      const name = prompt('Nome do comprador (opcional):', 'Apoiador Vermelho') || 'Apoiador Vermelho';
      socket.emit('trigger_purchase', { team: 'red', user: name });
    });

    document.getElementById('btnBuyYellow').addEventListener('click', () => {
      const name = prompt('Nome do comprador (opcional):', 'Apoiador Amarelo') || 'Apoiador Amarelo';
      socket.emit('trigger_purchase', { team: 'yellow', user: name });
    });

    document.getElementById('btnReset').addEventListener('click', () => {
      if (confirm('Tem certeza que deseja reiniciar o placar da batalha para 50 x 50?')) {
        socket.emit('reset_scores');
      }
    });

    function addManual(team, amount, reason) {
      socket.emit('manual_action', { team, amount, reason, user: 'Apresentador' });
    }

    function testAction(team, type, textOrGift) {
      if (type === 'comment') {
        socket.emit('test_event', { team, type: 'comment', text: textOrGift, user: 'Espectador_' + Math.floor(Math.random() * 900 + 100) });
      } else if (type === 'gift') {
        socket.emit('test_event', { team, type: 'gift', giftName: textOrGift, user: 'Presenteador_' + Math.floor(Math.random() * 900 + 100) });
      }
    }

    function log(msg, team = '') {
      const line = document.createElement('div');
      line.className = 'log-line ' + team;
      line.innerText = '[' + new Date().toLocaleTimeString() + '] ' + msg;
      logsBox.prepend(line);
      if (logsBox.children.length > 50) logsBox.removeChild(logsBox.lastChild);
    }

    socket.on('init_state', state => {
      if (state.scores) {
        adminRedScore.innerText = state.scores.red;
        adminYellowScore.innerText = state.scores.yellow;
      }
      if (state.tiktokUsername) {
        tiktokUser.value = state.tiktokUsername;
      }
      updateStatus(state.status, state.tiktokUsername);
    });

    socket.on('status_changed', data => {
      updateStatus(data.status, data.username);
      if (data.status === 'connected') {
        log('🟢 Conectado na live de @' + data.username + ' (Sala ID: ' + (data.roomId || 'OK') + ')');
      } else if (data.status === 'connecting') {
        log('🟡 Tentando conectar em @' + data.username + '...');
      } else {
        log('🔴 Desconectado da live (' + (data.error || data.reason || 'Normal') + ')');
      }
    });

    function updateStatus(status, username) {
      statusBadge.className = 'status-badge ' + status;
      if (status === 'connected') {
        statusText.innerText = 'AO VIVO (@' + username + ')';
      } else if (status === 'connecting') {
        statusText.innerText = 'Conectando...';
      } else {
        statusText.innerText = 'Desconectado';
      }
    }

    socket.on('score_updated', data => {
      adminRedScore.innerText = data.scores.red;
      adminYellowScore.innerText = data.scores.yellow;
      if (data.event && data.event.team !== 'both') {
        log(data.event.team.toUpperCase() + ' (+' + data.event.amount + '): @' + data.event.user + ' -> ' + data.event.reason, data.event.team);
      }
    });

    socket.on('super_purchase', data => {
      log('🚨 COMPRA SUPER BOOST! ' + data.team.toUpperCase() + ' (+' + data.points + '): ' + data.user + ' comprou ' + data.shirtName, data.team);
    });
  </script>
</body>
</html>
"""

with open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\admin.html", "w", encoding="utf-8") as f:
    f.write(admin)
print("Admin generated!")