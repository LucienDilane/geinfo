// geinfo/static/geinfo/js/main.js

// URLs des APIs Django (doivent être passées globalement depuis le HTML)
// Ces variables sont définies dans un bloc <script> avant ce fichier main.js dans dashboard.html
// Elles sont donc disponibles ici globalement.
// const API_ETUDIANTS_LIST_URL;
// const API_CREATE_FORUM_URL;
// const DEFAULT_PROFILE_IMAGE_URL;
// const LOGOUT_URL;

let currentEtudiantsData = [];
let currentlySelectedEtudiantId = null;

// --- FONCTIONS GENERALES DE CHARGEMENT DE CONTENU ---

/**
 * Charge le contenu de la section spécifiée et met à jour la navigation.
 * @param {string} targetId L'ID de la section de contenu à afficher (ex: 'etudiants-content').
 */
function loadContent(targetId) {
    // 1. Gérer les classes 'active' dans la sidebar
    const allNavLinks = document.querySelectorAll('.sidebar .nav-link');
    allNavLinks.forEach(link => {
        link.classList.remove('active');
    });

    const activeLink = document.querySelector(`.sidebar .nav-link[data-target="${targetId}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }

    // 2. Afficher/Masquer les sections de contenu
    const allContentSections = document.querySelectorAll('.content-section');
    allContentSections.forEach(section => {
        section.classList.remove('active-content');
    });

    const targetSection = document.getElementById(targetId);
    if (targetSection) {
        targetSection.classList.add('active-content');
    }

    // 3. Mettre à jour le titre de la page dans la navbar
    const pageTitle = document.getElementById('page-title');
    const formattedTitle = targetId
                            .replace(/-content$/, '')
                            .replace(/-/g, ' ')
                            .toUpperCase();
    pageTitle.textContent = formattedTitle;

    // Logique spécifique à la section
    if (targetId === 'etudiants-content') {
        fetchEtudiantsAndDisplay(); // Charge les étudiants et initialise l'affichage
    } else if (targetId === 'forums-content') {
        console.log("Section Forums chargée. (Contenu à implémenter)");
    } else if (targetId === 'annonces-content') {
        console.log("Section Annonces chargée. (Contenu à implémenter)");
    } else if (targetId === 'logout-content') {
        console.log("Déconnexion demandée. Redirection...");
    }
}

// --- FONCTIONS SPÉCIFIQUES AUX ÉTUDIANTS ---

/**
 * Récupère la liste de tous les étudiants depuis l'API Django,
 * peuple la liste latérale et affiche le premier étudiant.
 */
async function fetchEtudiantsAndDisplay() {
    try {
        const response = await fetch(API_ETUDIANTS_LIST_URL);
        if (!response.ok) {
            throw new Error(`Erreur HTTP! statut: ${response.status}`);
        }
        const etudiants = await response.json();
        currentEtudiantsData = etudiants;

        populateEtudiantsList(etudiants);

        if (etudiants.length > 0) {
            // Afficher le profil du premier étudiant par défaut
            displayEtudiantProfile(etudiants[0].id);
        } else {
            // Gérer le cas où il n'y a pas d'étudiants
            document.getElementById('profile-name').textContent = "Aucun étudiant trouvé.";
            document.getElementById('profile-matricule').textContent = "";
            document.getElementById('profile-image').src = DEFAULT_PROFILE_IMAGE_URL;
            document.getElementById('profile-header-bg').style.backgroundImage = "url('https://via.placeholder.com/600x120/f0f0f0/cccccc?text=Fonds+par+défaut')";

            document.getElementById('stats-filiere-value').textContent = "";
            document.getElementById('stats-annee-value').textContent = "";
            document.getElementById('stats-niveau-value').textContent = "";
            document.getElementById('form-id').value = "";
            document.getElementById('display-matricule').value = "";
            document.getElementById('form-nom').value = "";
            document.getElementById('form-prenom').value = "";
            document.getElementById('form-annee').value = "";
            document.getElementById('form-niveau').value = "";
            document.getElementById('form-filiere').value = "";

            const studentForumsList = document.getElementById('student-forums-list');
            const noForumsMessage = document.getElementById('no-forums-message');
            studentForumsList.innerHTML = '';
            noForumsMessage.style.display = 'block';
            studentForumsList.appendChild(noForumsMessage);

            document.querySelector('#etudiants-content .d-grid.gap-2.mt-3').style.display = 'none';
            document.getElementById('delete-etudiant-btn').style.display = 'none';
        }

    } catch (error) {
        console.error("Erreur lors de la récupération des étudiants:", error);
        alert("Impossible de charger la liste des étudiants. Veuillez réessayer.");
    }
}

/**
 * Peuple la liste des étudiants dans la barre latérale gauche.
 * @param {Array<Object>} etudiants Le tableau d'objets étudiants à afficher.
 */
function populateEtudiantsList(etudiants) {
    const etudiantsListDiv = document.getElementById('etudiants-list');
    if (!etudiantsListDiv) return;

    etudiantsListDiv.innerHTML = '';

    if (etudiants.length === 0) {
        etudiantsListDiv.innerHTML = '<div class="p-3 text-center text-muted">Aucun étudiant à afficher.</div>';
        return;
    }

    etudiants.forEach(etudiant => {
        const etudiantItem = document.createElement('div');
        etudiantItem.className = 'team-member-item';
        etudiantItem.dataset.etudiantId = etudiant.id; // Stocke l'ID

        const profileImageUrl = etudiant.profil || DEFAULT_PROFILE_IMAGE_URL;

        etudiantItem.innerHTML = `
            <img src="${profileImageUrl}" alt="${etudiant.nom} ${etudiant.prenom}" class="me-3 rounded-circle" style="width: 50px; height: 50px;">
            <div class="team-member-info">
                <strong>${etudiant.nom} ${etudiant.prenom}</strong>
                <span>${etudiant.filiere} - Année ${etudiant.annee}</span>
            </div>
        `;

        etudiantsListDiv.appendChild(etudiantItem);

        etudiantItem.addEventListener('click', () => {
            displayEtudiantProfile(etudiant.id); // Passe l'ID au lieu du matricule
        });
    });
}

/**
 * Affiche les détails d'un étudiant spécifique dans la carte de profil
 * et le formulaire de modification.
 * @param {number} etudiantId L'ID de l'étudiant à afficher.
 */
async function displayEtudiantProfile(etudiantId) {
    try {
        currentlySelectedEtudiantId = etudiantId;

        // Construire l'URL directement en utilisant l'ID et l'URL de base
        // Nous allons faire une requête au serveur pour obtenir l'URL si nécessaire,
        // mais pour l'instant, on suppose une structure /api/etudiants/<int:pk>/
        // Il est préférable de passer l'URL directement depuis le template si possible.
        // Puisque nous n'avons plus de template d'URL dans le HTML, nous devrons la construire ici.
        // C'est là que la gestion des URLs peut être un peu délicate.
        // Solution la plus simple : Avoir un point de terminaison API pour obtenir l'URL.
        // Solution alternative (moins propre mais fonctionnelle): Construire la chaîne manuellement.
        // Pour cet exemple, nous allons construire la chaîne manuellement, en supposant que
        // API_ETUDIANTS_LIST_URL se termine par /api/etudiants/
        // et que l'URL détail est /api/etudiants/<id>/
        let baseUrl = API_ETUDIANTS_LIST_URL;
        if (baseUrl.endsWith('/')) {
            baseUrl = baseUrl.slice(0, -1); // Supprime le slash final si présent
        }
        const url = `${baseUrl}/${etudiantId}/`;


        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Erreur HTTP! statut: ${response.status}`);
        }
        const etudiantDetail = await response.json();

        // Mettre à jour l'objet dans currentEtudiantsData pour inclure les forums pour les futures sélections
        const index = currentEtudiantsData.findIndex(e => e.id === etudiantId);
        if (index > -1) {
            currentEtudiantsData[index] = etudiantDetail;
        } else {
            // Si l'étudiant n'est pas dans la liste initiale (ex: créé récemment), l'ajouter
            currentEtudiantsData.push(etudiantDetail);
        }

        updateProfileUI(etudiantDetail);

        const allEtudiantItems = document.querySelectorAll('#etudiants-list .team-member-item');
        allEtudiantItems.forEach(item => {
            item.classList.remove('active');
        });
        const activeEtudiantItem = document.querySelector(`#etudiants-list .team-member-item[data-etudiant-id="${etudiantId}"]`);
        if (activeEtudiantItem) {
            activeEtudiantItem.classList.add('active');
        }
        document.querySelector('#etudiants-content .d-grid.gap-2.mt-3').style.display = 'block';
        document.getElementById('delete-etudiant-btn').style.display = 'inline-block';
    } catch (error) {
        console.error("Erreur lors de l'affichage du profil étudiant:", error);
        alert("Impossible de charger les détails de l'étudiant. Veuillez réessayer.");
        currentlySelectedEtudiantId = null; // Réinitialiser
        fetchEtudiantsAndDisplay(); // Recharger pour gérer un éventuel étudiant supprimé
    }
}

/**
 * Met à jour les éléments de l'interface utilisateur (carte de profil, formulaire, et forums)
 * avec les données de l'étudiant.
 * @param {Object} etudiant L'objet étudiant contenant les informations à afficher.
 */
function updateProfileUI(etudiant) {
    document.getElementById('profile-header-bg').style.backgroundImage = `url('https://via.placeholder.com/600x120/5a5a5a/cccccc?text=Fonds+profil')`;
    document.getElementById('profile-image').src = etudiant.profil || DEFAULT_PROFILE_IMAGE_URL;
    document.getElementById('profile-image').alt = `${etudiant.nom} ${etudiant.prenom}`;
    document.getElementById('profile-name').textContent = `${etudiant.nom} ${etudiant.prenom}`;
    document.getElementById('profile-matricule').textContent = `Matricule: ${etudiant.matricule}`;
    document.getElementById('profile-quote').textContent = "Informations générales de l'étudiant.";

    document.getElementById('stats-filiere-value').textContent = etudiant.filiere;
    document.getElementById('stats-annee-value').textContent = etudiant.annee;
    document.getElementById('stats-niveau-value').textContent = etudiant.niveau;

    document.getElementById('form-id').value = etudiant.id;
    document.getElementById('display-matricule').value = etudiant.matricule;
    document.getElementById('form-nom').value = etudiant.nom;
    document.getElementById('form-prenom').value = etudiant.prenom;
    document.getElementById('form-annee').value = etudiant.annee;
    document.getElementById('form-niveau').value = etudiant.niveau;
    document.getElementById('form-filiere').value = etudiant.filiere;

    const studentForumsList = document.getElementById('student-forums-list');
    const noForumsMessage = document.getElementById('no-forums-message');
    studentForumsList.innerHTML = '';

    if (etudiant.forums && etudiant.forums.length > 0) {
        noForumsMessage.style.display = 'none';
        etudiant.forums.forEach(forum => {
            const forumItem = document.createElement('a');
            forumItem.href = "#";
            forumItem.className = "list-group-item list-group-item-action d-flex justify-content-between align-items-start";
            forumItem.innerHTML = `
                <div class="ms-2 me-auto">
                    <div class="fw-bold">${forum.nom}</div>
                    <small class="text-muted">${forum.description || "Pas de description"}</small>
                </div>
                <span class="badge bg-primary rounded-pill">Créateur: ${forum.createur_nom || 'N/A'}</span>
            `;
            studentForumsList.appendChild(forumItem);
        });
    } else {
        noForumsMessage.style.display = 'block';
        if (studentForumsList.contains(noForumsMessage)) {
            studentForumsList.innerHTML = '';
        }
        studentForumsList.appendChild(noForumsMessage);
    }

    document.getElementById('forum-creator-id').value = etudiant.id;
}

/**
 * Gère la soumission du formulaire de modification des informations de l'étudiant.
 */
async function submitEtudiantForm(event) {
    event.preventDefault();

    const etudiantIdToUpdate = document.getElementById('form-id').value;
    if (!etudiantIdToUpdate) {
        alert("Aucun étudiant sélectionné pour la mise à jour.");
        return;
    }

    // Construire l'URL pour la mise à jour
    let baseUrl = API_ETUDIANTS_LIST_URL;
    if (baseUrl.endsWith('/')) {
        baseUrl = baseUrl.slice(0, -1);
    }
    const url = `${baseUrl}/${etudiantIdToUpdate}/`;

    const formData = {
        matricule: document.getElementById('display-matricule').value,
        nom: document.getElementById('form-nom').value,
        prenom: document.getElementById('form-prenom').value,
        annee: document.getElementById('form-annee').value,
        niveau: document.getElementById('form-niveau').value,
        filiere: document.getElementById('form-filiere').value,
    };

    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || response.statusText}`);
        }

        const result = await response.json();
        alert(result.message);

        // Recharger les données des étudiants pour refléter les changements
        fetchEtudiantsAndDisplay();
        // Afficher à nouveau le profil de l'étudiant mis à jour
        displayEtudiantProfile(parseInt(etudiantIdToUpdate));

    } catch (error) {
        console.error("Erreur lors de la mise à jour de l'étudiant:", error);
        alert("Échec de la mise à jour: " + error.message + ". Veuillez vérifier la console.");
    }
}

/**
 * Gère la suppression d'un étudiant.
 */
async function deleteEtudiant() {
    if (!currentlySelectedEtudiantId) {
        alert("Aucun étudiant n'est sélectionné pour la suppression.");
        return;
    }

    const confirmDelete = confirm(`Êtes-vous sûr de vouloir supprimer l'étudiant sélectionné (ID: ${currentlySelectedEtudiantId}) ? Cette action est irréversible.`);
    if (!confirmDelete) {
        return;
    }

    // Construire l'URL pour la suppression
    let baseUrl = API_ETUDIANTS_LIST_URL;
    if (baseUrl.endsWith('/')) {
        baseUrl = baseUrl.slice(0, -1);
    }
    const url = `${baseUrl}/${currentlySelectedEtudiantId}/`;

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (!response.ok) {
            if (response.status === 404) {
                 throw new Error("L'étudiant n'a pas été trouvé. Il a peut-être déjà été supprimé.");
            }
            const errorData = await response.json();
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || response.statusText}`);
        }

        alert("Étudiant supprimé avec succès !");

        currentlySelectedEtudiantId = null;
        fetchEtudiantsAndDisplay(); // Recharger la liste et l'UI

    } catch (error) {
        console.error("Erreur lors de la suppression de l'étudiant:", error);
        alert("Échec de la suppression: " + error.message + ". Veuillez vérifier la console.");
    }
}

/**
 * Gère la soumission du formulaire de création de forum.
 */
async function submitCreateForumForm(event) {
    event.preventDefault();

    const forumName = document.getElementById('forum-name').value;
    const forumDescription = document.getElementById('forum-description').value;
    const creatorId = document.getElementById('forum-creator-id').value;

    if (!creatorId) {
        alert("Veuillez sélectionner un étudiant pour créer un forum.");
        return;
    }

    const formData = {
        nom: forumName,
        description: forumDescription,
        createur_id: parseInt(creatorId),
    };

    try {
        const response = await fetch(API_CREATE_FORUM_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`HTTP error! status: ${response.status} - ${errorData.error || response.statusText}`);
        }

        const result = await response.json();
        alert(result.message);

        const createForumModalElement = document.getElementById('createForumModal');
        const createForumModal = bootstrap.Modal.getInstance(createForumModalElement) || new bootstrap.Modal(createForumModalElement);
        createForumModal.hide();

        document.getElementById('create-forum-form').reset();

        if (currentlySelectedEtudiantId) {
            displayEtudiantProfile(currentlySelectedEtudiantId);
        }

    } catch (error) {
        console.error("Erreur lors de la création du forum:", error);
        alert("Échec de la création du forum: " + error.message + ". Veuillez vérifier la console.");
    }
}

/**
 * Fonction utilitaire pour récupérer le jeton CSRF des cookies.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// --- INITIALISATION AU CHARGEMENT DE LA PAGE ---
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.sidebar .nav-link[data-target]');
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const targetId = link.dataset.target;
            loadContent(targetId);
        });
    });

    const etudiantEditForm = document.getElementById('etudiant-edit-form');
    if (etudiantEditForm) {
        etudiantEditForm.addEventListener('submit', submitEtudiantForm);
    }

    const deleteEtudiantBtn = document.getElementById('delete-etudiant-btn');
    if (deleteEtudiantBtn) {
        deleteEtudiantBtn.addEventListener('click', deleteEtudiant);
    }

    const createForumForm = document.getElementById('create-forum-form');
    if (createForumForm) {
        createForumForm.addEventListener('submit', submitCreateForumForm);
    }

    loadContent('etudiants-content');
});