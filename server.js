const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const fs = require('fs');
const { TikTokLiveConnection, WebcastEvent } = require('tiktok-live-connector');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: '*' }
});

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const CONFIG_FILE = path.join(__dirname, 'session_config.json');

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    }
  } catch (e) {
    console.error('Erro ao ler session_config.json:', e);
  }
  return { username: 'andradeindicai', sessionId: '', ttTargetIdc: 'useast2a', autoConnect: true };
}

function saveConfig(cfg) {
  try {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2), 'utf8');
  } catch (e) {
    console.error('Erro ao salvar session_config.json:', e);
  }
}

let accountConfig = loadConfig();

// Estado da Batalha
let gameState = {
  tiktokUsername: accountConfig.username || 'andradeindicai',
  status: 'disconnected', // 'connected', 'waiting_live', 'connecting', 'disconnected'
  accountConfigured: !!(accountConfig.username),
  hasSessionCookie: !!(accountConfig.sessionId),
  statusMessage: 'Pronto para conectar',
  scores: {
    red: 50,
    yellow: 50
  },
  config: {
    redName: 'Lula / PT (camisa vermelha)',
    yellowName: 'Flávio Bolsonaro (camisa amarela)',
    redShirtName: 'Camisa Brasil Vermelho 13',
    yellowShirtName: 'Camisa Acorda Brasil 22',
    pointsComment: 1,
    pointsGift: 5,
    pointsPurchase: 50,
    soundEnabled: true
  },
  recentEvents: []
};

let tiktokLiveConnection = null;
let retryTimeout = null;
let isStandbyActive = false;
let retryCount = 0;
const MAX_RETRIES = 500;

function parseCookieInput(raw) {
  if (!raw) return { sessionId: '', ttTargetIdc: 'useast2a' };
  raw = raw.trim();
  if (!raw.includes('=') && !raw.includes(';')) {
    return { sessionId: raw, ttTargetIdc: 'useast2a' };
  }
  let sessionId = '';
  let ttTargetIdc = 'useast2a';
  const parts = raw.split(';');
  for (const part of parts) {
    const [k, ...vParts] = part.trim().split('=');
    const v = vParts.join('=');
    if (k && v) {
      const keyLower = k.trim().toLowerCase();
      if (keyLower === 'sessionid') sessionId = v.trim();
      if (keyLower === 'tt-target-idc' || keyLower === 'tt_target_idc') ttTargetIdc = v.trim();
    }
  }
  return { sessionId: sessionId || raw, ttTargetIdc };
}

function normalizeText(text) {
  if (!text) return '';
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

const redKeywords = /\b(lula|pt|13|vermelh|vermelho|vermelha|esquerda|faz o l|lulinha|companheiro|companheira|ptista|lulalivre|dilma|haddad|treze)\b/i;
const yellowKeywords = /\b(bolsonaro|mito|22|amarel|amarelo|amarela|direita|flavio|capitao|patriota|patriotas|brasil|acorda|acordabrasil|vinteedois|michele|pl)\b/i;

function addEvent(event) {
  gameState.recentEvents.unshift(event);
  if (gameState.recentEvents.length > 30) {
    gameState.recentEvents.pop();
  }
}

function updateScore(team, amount, reason, user = 'Anônimo') {
  if (team === 'red') {
    gameState.scores.red = Math.max(0, gameState.scores.red + amount);
  } else if (team === 'yellow') {
    gameState.scores.yellow = Math.max(0, gameState.scores.yellow + amount);
  }

  const eventData = {
    id: Date.now() + Math.random().toString(36).substr(2, 4),
    team,
    amount,
    reason,
    user,
    timestamp: new Date().toLocaleTimeString(),
    scores: { ...gameState.scores }
  };

  addEvent(eventData);

  io.emit('score_updated', {
    scores: gameState.scores,
    event: eventData
  });
}

function connectToTikTok(username, isRetry = false) {
  if (!username) return;
  username = username.replace(/^@/, '').trim();
  gameState.tiktokUsername = username;
  accountConfig.username = username;
  saveConfig(accountConfig);

  if (!isRetry) {
    retryCount = 0;
    isStandbyActive = true;
  }

  if (retryTimeout) {
    clearTimeout(retryTimeout);
    retryTimeout = null;
  }

  if (tiktokLiveConnection) {
    try {
      tiktokLiveConnection.disconnect();
    } catch (e) {}
    tiktokLiveConnection = null;
  }

  const waitMsg = retryCount === 0 
    ? `Conta salva e pronta! Verificando live de @${username}...` 
    : `Conta @${username} conectada! Aguardando você clicar em "Iniciar LIVE" no TikTok Studio... (${retryCount})`;

  gameState.status = retryCount === 0 ? 'connecting' : 'waiting_live';
  gameState.statusMessage = waitMsg;

  console.log(`[TikTok] ${waitMsg}`);
  io.emit('status_changed', { 
    status: gameState.status, 
    username, 
    message: waitMsg,
    hasSession: !!accountConfig.sessionId
  });

  try {
    const connOptions = {
      processInitialData: false,
      enableExtendedGiftInfo: true,
      requestPollingIntervalMs: 1000,
      clientParams: {
        app_language: 'pt-BR',
        device_platform: 'web'
      }
    };

    if (accountConfig.sessionId) {
      connOptions.session = {
        cookie: {
          value: {
            sessionId: accountConfig.sessionId,
            ttTargetIdc: accountConfig.ttTargetIdc || 'useast2a'
          }
        }
      };
    }

    tiktokLiveConnection = new TikTokLiveConnection(username, connOptions);

    tiktokLiveConnection.connect().then(state => {
      console.log(`[TikTok] CONECTADO COM SUCESSO! Sala ID: ${state.roomId} de @${username}`);
      gameState.status = 'connected';
      gameState.statusMessage = 'Conectado e recebendo dados da Live!';
      retryCount = 0;
      io.emit('status_changed', { 
        status: 'connected', 
        username, 
        roomId: state.roomId,
        message: '🔴 AO VIVO! Conectado na live com sucesso!'
      });
    }).catch(err => {
      const errMsg = err.message || '';
      console.warn(`[TikTok] Verificação de transmissão: ${errMsg}`);

      if (isStandbyActive && (errMsg.includes('online') || errMsg.includes('offline') || errMsg.includes('ended') || errMsg.includes('Room') || errMsg.includes('not found') || errMsg.includes('Failed'))) {
        retryCount++;
        gameState.status = 'waiting_live';
        const standbyMsg = `🟢 Conta Pré-Conectada! Aguardando início da transmissão no TikTok Studio...`;
        gameState.statusMessage = standbyMsg;
        io.emit('status_changed', { 
          status: 'waiting_live', 
          username, 
          message: standbyMsg,
          attempt: retryCount
        });

        retryTimeout = setTimeout(() => {
          if (isStandbyActive) {
            connectToTikTok(username, true);
          }
        }, 4000);
        return;
      }

      gameState.status = 'disconnected';
      gameState.statusMessage = errMsg || 'Erro ao conectar';
      io.emit('status_changed', { 
        status: 'disconnected', 
        username, 
        error: errMsg || 'Conta não está ao vivo no TikTok.' 
      });
    });

    // Chat
    tiktokLiveConnection.on(WebcastEvent.CHAT, data => {
      try {
        const rawComment = data.comment || '';
        const norm = normalizeText(rawComment);
        const user = (data.user && (data.user.nickname || data.user.uniqueId)) || data.nickname || data.uniqueId || 'Espectador';

        const isRed = redKeywords.test(norm);
        const isYellow = yellowKeywords.test(norm);
        const isPurchase = /\b(comprei|pedi|garanti|adquiri|comprado|comprada)\b/i.test(norm);

        if (isPurchase) {
          if (isRed && !isYellow) {
            const pts = gameState.config.pointsPurchase || 50;
            updateScore('red', pts, `COMPRA NA SACOLA: "${rawComment}" 🛍️`, user);
            io.emit('super_purchase', { team: 'red', points: pts, user, shirtName: gameState.config.redShirtName });
            return;
          } else if (isYellow && !isRed) {
            const pts = gameState.config.pointsPurchase || 50;
            updateScore('yellow', pts, `COMPRA NA SACOLA: "${rawComment}" 🛍️`, user);
            io.emit('super_purchase', { team: 'yellow', points: pts, user, shirtName: gameState.config.yellowShirtName });
            return;
          }
        }

        if (isRed && !isYellow) {
          updateScore('red', gameState.config.pointsComment, `Comentou: "${rawComment}"`, user);
        } else if (isYellow && !isRed) {
          updateScore('yellow', gameState.config.pointsComment, `Comentou: "${rawComment}"`, user);
        } else if (isRed && isYellow) {
          updateScore('red', 1, rawComment, user);
          updateScore('yellow', 1, rawComment, user);
        }
      } catch (e) {
        console.error('Erro ao processar chat:', e);
      }
    });

    // Gifts
    tiktokLiveConnection.on(WebcastEvent.GIFT, data => {
      try {
        const giftName = ((data.gift && data.gift.name) || data.giftName || data.describe || '').toLowerCase();
        const count = data.repeatCount || 1;
        const user = (data.user && (data.user.nickname || data.user.uniqueId)) || data.nickname || data.uniqueId || 'Fã';

        if (giftName.includes('rose') || giftName.includes('rosa')) {
          const pts = (gameState.config.pointsGift || 5) * count;
          updateScore('red', pts, `Mandou ${count}x Rosa(s) 🌹`, user);
        } else {
          const pts = (gameState.config.pointsGift || 5) * count;
          updateScore('yellow', pts, `Mandou ${count}x ${data.giftName || 'Presente'} 🎁`, user);
        }
      } catch (e) {
        console.error('Erro ao processar presente:', e);
      }
    });

    // Likes
    tiktokLiveConnection.on(WebcastEvent.LIKE, data => {
      try {
        const user = (data.user && (data.user.nickname || data.user.uniqueId)) || data.nickname || 'Fã';
        io.emit('like_effect', {
          user,
          count: data.likeCount || 1
        });
      } catch (e) {}
    });

    tiktokLiveConnection.on('streamEnd', () => {
      console.log('[TikTok] Live encerrada.');
      gameState.status = 'waiting_live';
      gameState.statusMessage = 'Live encerrada. Pronto para a próxima!';
      io.emit('status_changed', { 
        status: 'waiting_live', 
        username, 
        message: 'Live finalizada. Sistema aguardando nova transmissão...' 
      });
      if (isStandbyActive) {
        retryTimeout = setTimeout(() => connectToTikTok(username, true), 5000);
      }
    });

    tiktokLiveConnection.on('error', err => {
      console.error('[TikTok] Erro na conexão:', err.message || err);
    });

  } catch (err) {
    console.error('[TikTok] Erro fatal:', err);
    gameState.status = 'disconnected';
    io.emit('status_changed', { status: 'disconnected', username, error: err.message });
  }
}

function disconnectTikTok() {
  isStandbyActive = false;
  if (retryTimeout) {
    clearTimeout(retryTimeout);
    retryTimeout = null;
  }
  if (tiktokLiveConnection) {
    try {
      tiktokLiveConnection.disconnect();
    } catch (e) {}
    tiktokLiveConnection = null;
  }
  gameState.status = 'disconnected';
  gameState.statusMessage = 'Desconectado';
  io.emit('status_changed', { status: 'disconnected', username: gameState.tiktokUsername, message: 'Desconectado' });
}

// API Endpoints
app.get('/api/state', (req, res) => {
  res.json({
    ...gameState,
    accountConfig: {
      username: accountConfig.username,
      hasSessionId: !!accountConfig.sessionId,
      autoConnect: accountConfig.autoConnect
    }
  });
});

app.post('/api/save-account', (req, res) => {
  const { username, sessionCookie, autoConnect } = req.body;
  if (username) {
    accountConfig.username = username.replace(/^@/, '').trim();
    gameState.tiktokUsername = accountConfig.username;
  }
  if (sessionCookie !== undefined) {
    const parsed = parseCookieInput(sessionCookie);
    accountConfig.sessionId = parsed.sessionId;
    accountConfig.ttTargetIdc = parsed.ttTargetIdc;
  }
  if (autoConnect !== undefined) {
    accountConfig.autoConnect = !!autoConnect;
  }
  saveConfig(accountConfig);

  gameState.accountConfigured = true;
  gameState.hasSessionCookie = !!accountConfig.sessionId;

  // Iniciar standby imediato
  connectToTikTok(accountConfig.username);

  res.json({ 
    success: true, 
    username: accountConfig.username,
    hasSessionCookie: !!accountConfig.sessionId,
    message: 'Conta salva com sucesso! O sistema já está em prontidão para sua live.'
  });
});

app.post('/api/connect', (req, res) => {
  const { username } = req.body;
  if (username) {
    connectToTikTok(username);
    res.json({ success: true, message: `Conectando em @${username}` });
  } else {
    res.status(400).json({ error: 'Username obrigatório' });
  }
});

app.post('/api/disconnect', (req, res) => {
  disconnectTikTok();
  res.json({ success: true, message: 'Desconectado' });
});

app.post('/api/purchase', (req, res) => {
  const { team, user } = req.body;
  const targetTeam = team === 'yellow' ? 'yellow' : 'red';
  const buyer = user || (targetTeam === 'red' ? 'Comprador Vermelho' : 'Comprador Amarelo');
  const points = gameState.config.pointsPurchase || 50;

  updateScore(targetTeam, points, 'COMPRA NA SACOLA TIKTOK SHOP! 🛍️', buyer);

  io.emit('super_purchase', {
    team: targetTeam,
    points,
    user: buyer,
    shirtName: targetTeam === 'red' ? gameState.config.redShirtName : gameState.config.yellowShirtName
  });

  res.json({ success: true, team: targetTeam, points });
});

app.post('/api/reset', (req, res) => {
  gameState.scores = { red: 50, yellow: 50 };
  gameState.recentEvents = [];
  io.emit('score_updated', {
    scores: gameState.scores,
    event: { team: 'both', amount: 0, reason: 'Placar reiniciado 50/50', user: 'Admin' }
  });
  res.json({ success: true, scores: gameState.scores });
});

// Sockets
io.on('connection', socket => {
  socket.emit('init_state', {
    ...gameState,
    accountConfig: {
      username: accountConfig.username,
      hasSessionId: !!accountConfig.sessionId,
      autoConnect: accountConfig.autoConnect
    }
  });

  socket.on('manual_action', data => {
    if (data.team && data.amount) {
      updateScore(data.team, data.amount, data.reason || 'Ajuste manual', data.user || 'Apresentador');
    }
  });

  socket.on('trigger_purchase', data => {
    const targetTeam = data.team === 'yellow' ? 'yellow' : 'red';
    const buyer = data.user || (targetTeam === 'red' ? 'Comprador da Sacola' : 'Comprador da Sacola');
    const points = gameState.config.pointsPurchase || 50;

    updateScore(targetTeam, points, 'COMPRA NA SACOLA TIKTOK SHOP! 🛍️', buyer);

    io.emit('super_purchase', {
      team: targetTeam,
      points,
      user: buyer,
      shirtName: targetTeam === 'red' ? gameState.config.redShirtName : gameState.config.yellowShirtName
    });
  });

  socket.on('test_event', data => {
    if (data.type === 'comment') {
      updateScore(data.team, 1, `Comentou: "${data.text}"`, data.user);
    } else if (data.type === 'gift') {
      updateScore(data.team, 5, `Mandou ${data.giftName}`, data.user);
    }
  });

  socket.on('reset_scores', () => {
    gameState.scores = { red: 50, yellow: 50 };
    gameState.recentEvents = [];
    io.emit('score_updated', {
      scores: gameState.scores,
      event: { team: 'both', amount: 0, reason: 'Placar reiniciado 50/50', user: 'Admin' }
    });
  });

  socket.on('save_account_config', data => {
    if (data.username) {
      accountConfig.username = data.username.replace(/^@/, '').trim();
    }
    if (data.sessionCookie !== undefined) {
      const parsed = parseCookieInput(data.sessionCookie);
      accountConfig.sessionId = parsed.sessionId;
      accountConfig.ttTargetIdc = parsed.ttTargetIdc;
    }
    accountConfig.autoConnect = !!data.autoConnect;
    saveConfig(accountConfig);

    gameState.tiktokUsername = accountConfig.username;
    gameState.accountConfigured = true;
    gameState.hasSessionCookie = !!accountConfig.sessionId;

    connectToTikTok(accountConfig.username);
  });

  socket.on('connect_tiktok', data => {
    if (data && data.username) {
      connectToTikTok(data.username);
    } else if (accountConfig.username) {
      connectToTikTok(accountConfig.username);
    }
  });

  socket.on('disconnect_tiktok', () => {
    disconnectTikTok();
  });
});

process.on('uncaughtException', err => {
  console.error('[ERRO NÃO TRATADO]', err.message || err);
});

process.on('unhandledRejection', reason => {
  console.error('[PROMISE REJEITADA]', reason);
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, '0.0.0.0', () => {
  console.log('===================================================');
  console.log('🚀 Servidor da Live Batalha TikTok rodando!');
  console.log(`📺 Overlay (Link do Navegador): http://localhost:${PORT}/overlay.html`);
  console.log(`🎮 Painel do Apresentador:      http://localhost:${PORT}/admin.html`);
  if (accountConfig.username && accountConfig.autoConnect) {
    console.log(`✨ Modo Auto-Prontidão ativo para @${accountConfig.username}`);
    connectToTikTok(accountConfig.username);
  }
  console.log('===================================================');
});