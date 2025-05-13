document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('listes-chat');
    const inputField = document.getElementById('listes-input');
    const btnCode = document.getElementById('btn-code');
    const btnText = document.getElementById('btn-text');
    
    // Détection automatique du type de saisie
    inputField.addEventListener('input', function() {
        const text = inputField.value.trim();
        if (text.startsWith('[') || text.includes('=') || text.includes('.')) {
            btnCode.classList.add('active');
            btnText.classList.remove('active');
        } else {
            btnText.classList.add('active');
            btnCode.classList.remove('active');
        }
    });
    
    function sendMessage() {
        const message = inputField.value.trim();
        if (!message) return;
        
        // Ajout du message utilisateur
        const userMsg = document.createElement('div');
        userMsg.className = 'message user-message';
        userMsg.innerHTML = `<p>${message}</p>`;
        chatContainer.appendChild(userMsg);
        
        // Envoi au serveur
        fetch('/themes/listes/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            const botMsg = document.createElement('div');
            botMsg.className = 'message bot-message';
            botMsg.innerHTML = `<p>${data.response}</p>`;
            chatContainer.appendChild(botMsg);
        });
        
        inputField.value = '';
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});