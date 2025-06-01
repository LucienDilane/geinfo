// script.js

document.addEventListener('DOMContentLoaded', function() {
    const leftSidebar = document.querySelector('.left-sidebar');
    const rightSidebar = document.querySelector('.right-sidebar');
    const messagesContainer = document.getElementById('messages-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const body = document.body;
    let overlay = document.createElement('div');
    overlay.classList.add('sidebar-overlay');
    document.body.appendChild(overlay);

    // Scroll to bottom on page load
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Fonction pour ouvrir/fermer une sidebar
    function toggleSidebar(sidebar) {
        const isShowing = sidebar.classList.contains('show');
        if (isShowing) {
            sidebar.classList.remove('show');
            overlay.style.display = 'none';
            body.classList.remove('no-scroll');
        } else {
            if (sidebar === leftSidebar && rightSidebar.classList.contains('show')) {
                rightSidebar.classList.remove('show');
            } else if (sidebar === rightSidebar && leftSidebar.classList.contains('show')) {
                leftSidebar.classList.remove('show');
            }
            sidebar.classList.add('show');
            overlay.style.display = 'block';
            body.classList.add('no-scroll');
        }
    }

    // Gestion de l'overlay pour fermer les sidebars
    overlay.addEventListener('click', function() {
        if (leftSidebar.classList.contains('show')) {
            toggleSidebar(leftSidebar);
        }
        if (rightSidebar.classList.contains('show')) {
            toggleSidebar(rightSidebar);
        }
    });

    // Boutons toggle pour les sidebars (ajoutés au HTML)
    const toggleLeftBtn = document.querySelector('.toggle-sidebar-left');
    const toggleRightBtn = document.querySelector('.toggle-sidebar-right');

    if (toggleLeftBtn) {
        toggleLeftBtn.addEventListener('click', () => toggleSidebar(leftSidebar));
    }
    if (toggleRightBtn) {
        toggleRightBtn.addEventListener('click', () => toggleSidebar(rightSidebar));
    }

    // Auto-resize du textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Initial resize in case of pre-filled content
    if (messageInput) {
        messageInput.style.height = 'auto';
        messageInput.style.height = (messageInput.scrollHeight) + 'px';
    }

    // Pour simuler la sélection active des canaux/groupes dans la sidebar gauche
    document.querySelectorAll('.left-sidebar .nav-link-custom').forEach(link => {
        link.addEventListener('click', function(e) {
            // e.preventDefault(); // Désactiver si vous voulez des liens réels
            document.querySelectorAll('.left-sidebar .nav-link-custom.active').forEach(activeLink => {
                activeLink.classList.remove('active');
            });
            this.classList.add('active');
        });
    });


    // --- LOGIQUE POUR L'ENVOI DU MESSAGE (PUREMENT CLIENT) ---
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Empêche l'envoi traditionnel du formulaire

        const messageContent = messageInput.value.trim();

        if (messageContent.length === 0) {
            return; // Ne rien faire si le message est vide
        }

        // Récupérer les informations de l'utilisateur connecté
        // CES VALEURS SONT INJECTÉES PAR DJANGO DANS LE HTML.
        // Assurez-vous que le HTML contient des éléments avec ces IDs ou des attributs data-* si vous ne voulez pas les injecter directement.
        // Pour l'instant, je les laisse comme dans le HTML, en supposant qu'ils sont disponibles.
        const currentUserProfileUrl = document.getElementById('current-user-avatar')?.src || 'https://via.placeholder.com/40';
        const currentUserName = document.getElementById('current-user-name')?.textContent || 'Utilisateur Actuel';

        // Formater l'heure locale
        const now = new Date();
        const currentTime = now.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) + ', ' + now.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });

        const messageData = {
            auteur_nom: currentUserName,
            auteur_profil_url: currentUserProfileUrl,
            contenu: messageContent,
            date_envoi: currentTime,
            is_current_user: true // Toujours true pour les messages envoyés localement
        };

        // Crée l'élément de message HTML
        const newMessageElement = createMessageElement(messageData);
        messagesContainer.appendChild(newMessageElement);

        // Vide le textarea et réinitialise sa hauteur
        messageInput.value = '';
        messageInput.style.height = 'auto';

        // Scrolle en bas du conteneur de messages
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });

    // Fonction pour créer l'élément de message HTML
    function createMessageElement(messageData) {
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble');
        messageBubble.classList.add(messageData.is_current_user ? 'current-user' : 'other-user');

        const avatarContainer = document.createElement('div');
        avatarContainer.classList.add('avatar-container');
        const avatarImg = document.createElement('img');
        avatarImg.src = messageData.auteur_profil_url;
        avatarImg.alt = messageData.auteur_nom;
        avatarContainer.appendChild(avatarImg);

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');

        const senderInfo = document.createElement('div');
        senderInfo.classList.add('message-sender-info');
        senderInfo.textContent = messageData.auteur_nom;

        const messageText = document.createElement('div');
        messageText.classList.add('message-text');
        messageText.textContent = messageData.contenu;

        const messageTime = document.createElement('div');
        messageTime.classList.add('message-time');
        messageTime.textContent = messageData.date_envoi;

        messageContent.appendChild(senderInfo);
        messageContent.appendChild(messageText);
        messageContent.appendChild(messageTime);

        messageBubble.appendChild(avatarContainer);
        messageBubble.appendChild(messageContent);

        return messageBubble;
    }
    // --- FIN LOGIQUE POUR L'ENVOI DU MESSAGE ---

    // Initial scroll to bottom when page loads
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
});