document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('listes-chat');
    const inputField = document.getElementById('listes-input');
    const sendBtn = document.getElementById('btn-send');
    const typeBadge = document.getElementById('input-type-badge');
    const quickBtns = document.querySelectorAll('.quick-btn');

    // Détection automatique du type de contenu
    inputField.addEventListener('input', function() {
        const text = inputField.value.trim();
        const isCode = text.includes('=') || text.includes('[') || 
                       text.includes(']') || text.includes('def ') || 
                       text.includes('import ') || text.includes('.') && 
                       !text.endsWith('.') || text.includes('(') || 
                       text.includes(')') || text.includes(':');
        
        if (isCode) {
            typeBadge.textContent = 'Code';
            typeBadge.className = 'type-badge code-badge';
        } else {
            typeBadge.textContent = 'Question';
            typeBadge.className = 'type-badge text-badge';
        }
    });

    // Actions rapides
    quickBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            inputField.value = this.dataset.prompt;
            inputField.dispatchEvent(new Event('input'));
            sendMessage();
        });
    });

    // Envoi de message
    function sendMessage() {
        const message = inputField.value.trim();
        if (!message) return;

        // Ajout du message utilisateur
        addMessage(message, 'user');
        
        // Envoi au serveur
        fetch('/themes/listes/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: message,
                is_code: typeBadge.textContent === 'Code'
            })
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, 'bot');
            Prism.highlightAll(); // Recolorer le nouveau code
        })
        .catch(error => {
            addMessage("Erreur de connexion au serveur", 'bot-error');
        });

        inputField.value = '';
    }

    // Gestion des touches
    inputField.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    // Fonction d'ajout de message
    function addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const now = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="sender">${type === 'user' ? 'Vous' : 'Assistant NSI'}</span>
                <span class="time">${now}</span>
            </div>
            <div class="message-content">
                ${formatContent(content, type)}
            </div>
        `;
        
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Formatage du contenu
    function formatContent(content, type) {
        if (type === 'bot' && content.includes('```python')) {
            return content.replace(/```python([\s\S]*?)```/g, 
                '<div class="code-example"><pre><code class="language-python">$1</code></pre></div>');
        }
        return `<p>${content.replace(/\n/g, '<br>')}</p>`;
    }
});