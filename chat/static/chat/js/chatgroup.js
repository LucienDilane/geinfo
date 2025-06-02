document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendMessageBtn = document.getElementById('sendMessageBtn');
    const chatMessages = document.querySelector('.chat-messages');

    // Récupérer l'ID du forum depuis l'attribut data
    const forumId = chatMessages.dataset.forumId;
    if (!forumId) {
        console.error("L'ID du forum n'a pas été trouvé. Assurez-vous que l'attribut data-forum-id est défini sur .chat-messages.");
        return; // Arrêter l'exécution si l'ID du forum est manquant
    }

    let lastMessageId = 0; // Pour le polling

    // Initialiser lastMessageId avec le dernier message déjà présent sur la page
    const initialMessages = chatMessages.querySelectorAll('.message');
    if (initialMessages.length > 0) {
        lastMessageId = parseInt(initialMessages[initialMessages.length - 1].dataset.messageId);
    }
    
    // Fonction pour ajouter un message au chat (rendue plus générique pour le polling)
    function addMessageToChat(messageData, prepend = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'mb-2');

        // Déterminer si le message est envoyé ou reçu par l'utilisateur actuel
        const isCurrentUser = messageData.is_current_user; // Viendra du backend
        if (isCurrentUser) {
            messageDiv.classList.add('sent', 'text-end');
        } else {
            messageDiv.classList.add('received');
        }
        
        messageDiv.dataset.messageId = messageData.id;

        const senderNameSpan = document.createElement('span');
        senderNameSpan.classList.add('sender-name');
        senderNameSpan.textContent = isCurrentUser ? 'Vous' : messageData.auteur;

        const messageContentP = document.createElement('p');
        messageContentP.classList.add('message-content');
        messageContentP.textContent = messageData.contenu;

        const messageTimeSmall = document.createElement('small');
        messageTimeSmall.classList.add('message-time');
        messageTimeSmall.textContent = messageData.date_envoi; // L'heure est déjà formatée par Django

        messageDiv.appendChild(senderNameSpan);
        messageDiv.appendChild(messageContentP);
        messageDiv.appendChild(messageTimeSmall);

        if (prepend) {
            chatMessages.prepend(messageDiv); // Pour insérer au début si on récupère l'historique
        } else {
            chatMessages.appendChild(messageDiv);
        }

        // Mettre à jour le dernier message ID
        lastMessageId = Math.max(lastMessageId, messageData.id);

        // Faire défiler vers le bas pour afficher le dernier message (uniquement si ce n'est pas une récupération d'historique)
        if (!prepend) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

  
    // Initialiser le polling
    // Défilement initial vers le bas pour les messages déjà chargés
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Lancer le polling toutes les X secondes (par exemple, toutes les 3 secondes)
    setInterval(fetchNewMessages, 3000); // Poll toutes les 3 secondes
});