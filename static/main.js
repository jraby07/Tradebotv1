async function startBot() {
    const res = await fetch('/api/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({mode: 'simulate'})
    });
<<<<<<< HEAD
=======
    if (!res.ok) {
        alert('Failed to start bot');
        return;
    }
>>>>>>> pr8
    updateStatus();
}

async function stopBot() {
<<<<<<< HEAD
    await fetch('/api/stop', {method: 'POST'});
=======
    const res = await fetch('/api/stop', {method: 'POST'});
    if (!res.ok) {
        alert('Failed to stop bot');
        return;
    }
>>>>>>> pr8
    updateStatus();
}

async function updateStatus() {
    const res = await fetch('/api/status');
    const data = await res.json();
    document.getElementById('status').textContent = JSON.stringify(data, null, 2);
}

document.getElementById('startBtn').addEventListener('click', startBot);
document.getElementById('stopBtn').addEventListener('click', stopBot);
updateStatus();
