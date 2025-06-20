async function startBot() {
    const mode = document.getElementById('mode').value;
    const config = document.getElementById('configPath').value;
    const res = await fetch('/api/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({mode, config})
    });
    if (!res.ok) {
        alert('Failed to start bot');
        return;
    }
    updateStatus();
}

async function stopBot() {
    const res = await fetch('/api/stop', {method: 'POST'});
    if (!res.ok) {
        alert('Failed to stop bot');
        return;
    }
    updateStatus();
}

function renderStatus(data) {
    const statusEl = document.getElementById('status');
    statusEl.textContent = `Running: ${data.running}  Balance: ${data.balance?.toFixed ? data.balance.toFixed(2) : 0}  Aggressiveness: ${data.aggressiveness ?? ''}`;
}

function renderTrades(trades) {
    const tbody = document.querySelector('#tradesTable tbody');
    tbody.innerHTML = '';
    (trades || []).forEach(t => {
        const tr = document.createElement('tr');
        if (!t.open) tr.classList.add('table-secondary');
        tr.innerHTML = `<td>${t.action}</td><td>${t.price.toFixed(2)}</td><td>${t.amount.toFixed(4)}</td><td>${t.reason}</td><td>${t.pnl.toFixed(2)}</td>`;
        tbody.appendChild(tr);
    });
}

async function updateStatus() {
    const res = await fetch('/api/status');
    const data = await res.json();
    renderStatus(data);
    renderTrades(data.trades);
}

document.getElementById('startBtn').addEventListener('click', startBot);
document.getElementById('stopBtn').addEventListener('click', stopBot);
updateStatus();
setInterval(updateStatus, 5000);
