// ==================== FONCTIONS GÉNÉRALES ====================
function toggleTheme(theme) {
    document.querySelectorAll('.theme-content').forEach(content => {
        content.style.display = 'none';
    });
    document.getElementById(`${theme}-content`).style.display = 'block';
}

// ==================== CHATBOT ====================
async function sendChatMessage(pageType) {
    const input = document.getElementById(`${pageType}-input`);
    const chatbox = document.getElementById(`${pageType}-chat`);
    
    if (input.value.trim() === '') return;

    // Afficher le message de l'utilisateur
    chatbox.innerHTML += `<div class="user-message">${input.value}</div>`;
    
    // Simulation de réponse (remplacez par un appel API réel)
    chatbox.innerHTML += `<div class="bot-message">En traitement...</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: input.value,
                context: pageType 
            })
        });
        const data = await response.json();
        
        // Remplacer le message "En traitement" par la vraie réponse
        chatbox.lastElementChild.innerHTML = data.reply;
    } catch (error) {
        chatbox.lastElementChild.innerHTML = "Erreur de connexion à l'API";
    }

    input.value = '';
}

// ==================== EXAMEN BLANC ====================
function startExamTimer() {
    let timeLeft = 3600; // 1 heure en secondes
    const timer = setInterval(() => {
        const hours = Math.floor(timeLeft / 3600);
        const minutes = Math.floor((timeLeft % 3600) / 60);
        document.getElementById('countdown').textContent = 
            `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${(timeLeft % 60).toString().padStart(2, '0')}`;
        
        if (timeLeft-- <= 0) clearInterval(timer);
    }, 1000);
}

// ==================== CARTES MÉMOIRE ====================
let currentCard = 0;
const flashcards = [
    { front: "Qu'est-ce qu'une liste ?", back: "Collection mutable et ordonnée d'éléments" },
    { front: "Méthode pour ajouter un élément", back: ".append()" }
];

function updateFlashcard() {
    const card = document.querySelector('.flashcard');
    card.querySelector('.front p').textContent = flashcards[currentCard].front;
    card.querySelector('.back p').innerHTML = flashcards[currentCard].back;
}

function flipCard(element) {
    element.classList.toggle('flipped');
}

function nextCard() {
    currentCard = (currentCard + 1) % flashcards.length;
    document.querySelector('.flashcard').classList.remove('flipped');
    updateFlashcard();
    document.querySelector('.card-count').textContent = `${currentCard + 1}/${flashcards.length}`;
}

// ==================== ÉDITEUR DE CODE ====================
function runCode(editorId) {
    const code = document.getElementById(editorId).value;
    const output = document.getElementById(editorId.replace('code', 'output'));
    
    try {
        // Note: En production, utilisez une API pour exécution sécurisée
        output.textContent = "Résultat simulé : \n" + code.replace('□', 'i');
    } catch (error) {
        output.textContent = "Erreur : " + error.message;
    }
}

// ==================== INITIALISATION ====================
document.addEventListener('DOMContentLoaded', () => {
    // Démarrer le timer si on est sur la page d'examen
    if (document.getElementById('countdown')) {
        startExamTimer();
    }

    // Initialiser les cartes mémoire
    if (document.querySelector('.flashcard')) {
        updateFlashcard();
    }

    // Gestionnaires d'événements génériques
    document.querySelectorAll('.chat-input button').forEach(button => {
        button.addEventListener('click', (e) => {
            const pageType = e.target.closest('.chatbot-section').id.replace('-section', '');
            sendChatMessage(pageType);
        });
    });
});