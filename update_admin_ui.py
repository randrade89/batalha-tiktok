with open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\admin.html", "r", encoding="utf-8") as f:
    html = f.read()

old_status = """    socket.on('status_changed', data => {
      updateStatus(data.status, data.username);
      if (data.status === 'connected') {
        log('🟢 Conectado na live de @' + data.username + ' (Sala ID: ' + (data.roomId || 'OK') + ')');
      } else if (data.status === 'connecting') {
        log('🟡 Tentando conectar em @' + data.username + '...');
      } else {
        log('🔴 Desconectado da live (' + (data.error || data.reason || 'Normal') + ')');
      }
    });"""

new_status = """    socket.on('status_changed', data => {
      updateStatus(data.status, data.username, data.message);
      if (data.status === 'connected') {
        log('🟢 CONECTADO NA LIVE DE @' + data.username + ' (Sala ID: ' + (data.roomId || 'OK') + ')');
      } else if (data.status === 'connecting') {
        log('🟡 ' + (data.message || ('Tentando conectar em @' + data.username + '...')));
      } else {
        log('🔴 ' + (data.error || data.reason || 'Desconectado'));
      }
    });

    function updateStatus(status, username, customMsg) {
      statusBadge.className = 'status-badge ' + status;
      if (status === 'connected') {
        statusText.innerText = 'AO VIVO (@' + username + ')';
      } else if (status === 'connecting') {
        statusText.innerText = customMsg ? 'Aguardando Live...' : 'Conectando...';
      } else {
        statusText.innerText = 'Desconectado';
      }
    }"""

if old_status in html:
    html = html.replace(old_status, new_status)
    with open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\admin.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("admin.html updated successfully!")
else:
    print("old_status pattern not matched directly.")