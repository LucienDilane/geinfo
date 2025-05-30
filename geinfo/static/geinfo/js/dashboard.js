// geinfo/static/geinfo/js/main.js

// --- CONSTANTES GLOBALES (assumées définies dans dashboard.html) ---
// Ces variables sont supposées être définies dans votre template dashboard.html
// Exemple: <script> const API_ETUDIANTS_LIST_URL = "{% url 'etudiants_list_api' %}"; </script>
// const API_ETUDIANTS_LIST_URL;
// const API_FORUMS_LIST_URL;
// const API_CREATE_FORUM_URL; // Pour le modal de création lié à l'étudiant
// const API_CREATE_FORUM_GLOBAL_URL; // Pour le modal de création global
// const DEFAULT_PROFILE_IMAGE_URL;
// const LOGOUT_URL;
// const API_FORUM_MEMBERS_URL_BASE; // Pour la base de l'URL des membres d'un forum
// const API_FORUM_REMOVE_MEMBER_URL_BASE; // Pour la base de l'URL de suppression d'un membre

// --- VARIABLES D'ÉTAT GLOBALES ---
let currentEtudiantsData = [];      // Stocke la liste complète des étudiants
let currentlySelectedEtudiantId = null; // ID de l'étudiant actuellement affiché

let currentForumsData = [];         // Stocke la liste complète des forums
let currentlySelectedForumId = null;    // ID du forum actuellement affiché


// --- FONCTIONS UTILITAIRES ---

// Fonction pour obtenir le token CSRF
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

// Fonction pour construire l'URL de détail/édition/suppression d'un étudiant
function getEtudiantDetailApiUrl(etudiantId) {
    if (!etudiantId) return null;
    // Remplacez l'ID '0' de l'URL de base par l'ID réel de l'étudiant
    return API_ETUDIANTS_LIST_URL.replace('/api/etudiants/', `/api/etudiants/${etudiantId}/`);
}

// Fonction pour construire l'URL de détail/édition/suppression d'un forum
function getForumDetailApiUrl(forumId) {
    if (!forumId) return null;
    // Remplacez l'ID '0' de l'URL de base par l'ID réel du forum
    return API_FORUMS_LIST_URL.replace('/api/forums/', `/api/forums/${forumId}/`);
}


// --- GESTION DES SECTIONS DE CONTENU (NAVIGATION) ---

// Fonction pour basculer entre les sections de contenu (Étudiants, Forums, etc.)
function loadContent(targetId) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none'; // Cache toutes les sections
    });
    document.getElementById(targetId).style.display = 'block'; // Affiche la section cible

    // Met à jour la classe active dans la barre latérale
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`.sidebar .nav-link[data-target="${targetId}"]`).classList.add('active');

    // Charge les données spécifiques à la section
    if (targetId === 'etudiants-content') {
        fetchEtudiantsAndDisplay();
    } else if (targetId === 'forums-content') {
        fetchForumsAndDisplay();
    }
    // Ajoutez d'autres sections ici si nécessaire
}


// --- FONCTIONS SPÉCIFIQUES AUX ÉTUDIANTS ---

// Récupère et affiche la liste des étudiants
async function fetchEtudiantsAndDisplay() {
    console.log("Tentative de récupération des étudiants depuis:", API_ETUDIANTS_LIST_URL);
    try {
        const response = await fetch(API_ETUDIANTS_LIST_URL);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${response.statusText} - ${errorText}`);
        }
        const etudiants = await response.json();
        currentEtudiantsData = etudiants; // Stocke les données des étudiants globalement
        console.log("Étudiants récupérés:", etudiants);

        populateEtudiantsList(etudiants);

        if (etudiants.length > 0) {
            if (etudiants[0] && typeof etudiants[0].id === 'number') {
                displayEtudiantDetails(etudiants[0].id); // Affiche les détails du premier étudiant par défaut
            } else {
                console.warn("Le premier étudiant ne contient pas un ID numérique valide:", etudiants[0]);
                displayNoEtudiantSelectedUI();
            }
        } else {
            console.log("Aucun étudiant trouvé.");
            displayNoEtudiantSelectedUI();
        }
    } catch (error) {
        console.error("Erreur lors de la récupération des étudiants:", error);
        alert("Impossible de charger la liste des étudiants. Veuillez réessayer. Détails: " + error.message);
        displayNoEtudiantSelectedUI();
    }
}

// Peuple la liste HTML des étudiants
function populateEtudiantsList(etudiants) {
    const listElement = document.getElementById('etudiants-list');
    listElement.innerHTML = ''; // Vide la liste actuelle

    if (etudiants.length === 0) {
        listElement.innerHTML = '<div class="p-3 text-center text-muted">Aucun étudiant trouvé.</div>';
        return;
    }

    etudiants.forEach(etudiant => {
        const listItem = document.createElement('a');
        listItem.href = "#";
        listItem.className = "list-group-item list-group-item-action etudiant-item";
        listItem.dataset.etudiantId = etudiant.id;
        listItem.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">${etudiant.nom} ${etudiant.prenom}</h5>
                <small class="text-muted">Matricule: ${etudiant.matricule}</small>
            </div>
            <p class="mb-1">${etudiant.filiere} - ${etudiant.niveau}</p>
        `;
        listItem.addEventListener('click', (event) => {
            event.preventDefault();
            displayEtudiantDetails(etudiant.id);
        });
        listElement.appendChild(listItem);
    });
}

// Affiche les détails d'un étudiant spécifique
async function displayEtudiantDetails(etudiantId) {
    if (!etudiantId) {
        displayNoEtudiantSelectedUI();
        return;
    }

    currentlySelectedEtudiantId = etudiantId; // Met à jour l'ID de l'étudiant sélectionné

    const url = getEtudiantDetailApiUrl(etudiantId);
    if (!url) {
        alert("Erreur: Impossible de générer l'URL de détail de l'étudiant.");
        displayNoEtudiantSelectedUI();
        return;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${response.statusText} - ${errorText}`);
        }
        const etudiantDetail = await response.json();
        console.log("Détails étudiant récupérés:", etudiantDetail);

        // Met à jour les éléments HTML avec les détails de l'étudiant
        document.getElementById('etudiant-detail-name').textContent = `${etudiantDetail.nom} ${etudiantDetail.prenom}`;
        document.getElementById('etudiant-detail-matricule').textContent = etudiantDetail.matricule;
        document.getElementById('etudiant-detail-filiere').textContent = etudiantDetail.filiere;
        document.getElementById('etudiant-detail-annee').textContent = etudiantDetail.annee;
        document.getElementById('etudiant-detail-niveau').textContent = etudiantDetail.niveau;

        const profileImage = document.getElementById('etudiant-detail-profile-img');
        profileImage.src = etudiantDetail.profil || DEFAULT_PROFILE_IMAGE_URL;
        profileImage.alt = `Photo de ${etudiantDetail.nom} ${etudiantDetail.prenom}`;

        // Met à jour les champs du modal d'édition
        document.getElementById('edit-etudiant-id').value = etudiantDetail.id;
        document.getElementById('edit-etudiant-matricule').value = etudiantDetail.matricule;
        document.getElementById('edit-etudiant-nom').value = etudiantDetail.nom;
        document.getElementById('edit-etudiant-prenom').value = etudiantDetail.prenom;
        document.getElementById('edit-etudiant-filiere').value = etudiantDetail.filiere;
        document.getElementById('edit-etudiant-annee').value = etudiantDetail.annee;
        document.getElementById('edit-etudiant-niveau').value = etudiantDetail.niveau;

        // Met à jour les forums de l'étudiant (si pertinent pour cette vue)
        const etudiantForumsList = document.getElementById('etudiant-detail-forums-list');
        if (etudiantForumsList) {
            etudiantForumsList.innerHTML = '';
            if (etudiantDetail.forums && etudiantDetail.forums.length > 0) {
                etudiantDetail.forums.forEach(forum => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item';
                    li.textContent = `${forum.nom} (Créateur: ${forum.createur_nom})`;
                    etudiantForumsList.appendChild(li);
                });
            } else {
                etudiantForumsList.innerHTML = '<li class="list-group-item text-muted">Aucun forum d\'appartenance.</li>';
            }
        }


        // Affiche la vue détaillée et active les boutons d'action
        document.getElementById('etudiant-detail-view').style.display = 'block';
        const editEtudiantBtn = document.getElementById('edit-etudiant-btn');
        if (editEtudiantBtn) editEtudiantBtn.style.display = 'inline-block';
        const deleteEtudiantBtn = document.getElementById('delete-etudiant-btn');
        if (deleteEtudiantBtn) deleteEtudiantBtn.style.display = 'inline-block';

        // Gérer la classe active dans la liste des étudiants
        document.querySelectorAll('#etudiants-list .etudiant-item').forEach(item => {
            item.classList.remove('active');
        });
        const activeEtudiantItem = document.querySelector(`#etudiants-list .etudiant-item[data-etudiant-id="${etudiantId}"]`);
        if (activeEtudiantItem) {
            activeEtudiantItem.classList.add('active');
        }

    } catch (error) {
        console.error("Erreur lors de l'affichage des détails de l'étudiant:", error);
        alert("Impossible de charger les détails de l'étudiant. Veuillez réessayer. Détails: " + error.message);
        displayNoEtudiantSelectedUI();
    }
}

// Affiche un message si aucun étudiant n'est sélectionné ou trouvé
function displayNoEtudiantSelectedUI() {
    document.getElementById('etudiant-detail-view').style.display = 'none';
    const messageContainer = document.getElementById('etudiant-detail-card');
    if (messageContainer) { // Assurez-vous que l'élément existe
        messageContainer.innerHTML = '<div class="p-3 text-center text-muted">Sélectionnez un étudiant dans la liste pour voir ses détails.</div>';
    }
}

// Soumet le formulaire de modification d'étudiant
async function submitEtudiantForm(event) {
    event.preventDefault();

    const etudiantId = document.getElementById('edit-etudiant-id').value;
    const url = getEtudiantDetailApiUrl(etudiantId);
    if (!url) {
        alert("Erreur: ID de l'étudiant introuvable pour la mise à jour.");
        return;
    }

    const formData = {
        matricule: document.getElementById('edit-etudiant-matricule').value,
        nom: document.getElementById('edit-etudiant-nom').value,
        prenom: document.getElementById('edit-etudiant-prenom').value,
        filiere: document.getElementById('edit-etudiant-filiere').value,
        annee: parseInt(document.getElementById('edit-etudiant-annee').value),
        niveau: document.getElementById('edit-etudiant-niveau').value
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
            const errorData = await response.json().catch(() => ({error: "Réponse non-JSON", message: response.statusText}));
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || errorData.message || response.statusText}`);
        }

        const result = await response.json();
        alert(result.message || "Étudiant mis à jour avec succès !");

        // Fermer le modal
        const editModalElement = document.getElementById('editEtudiantModal');
        const editModal = bootstrap.Modal.getInstance(editModalElement) || new bootstrap.Modal(editModalElement);
        editModal.hide();

        // Recharger la liste et les détails de l'étudiant
        fetchEtudiantsAndDisplay();

    } catch (error) {
        console.error("Erreur lors de la mise à jour de l'étudiant:", error);
        alert("Échec de la mise à jour: " + error.message + ". Veuillez vérifier la console.");
    }
}

// Supprime un étudiant
async function deleteEtudiant() {
    const etudiantId = document.getElementById('edit-etudiant-id').value;
    if (!etudiantId) {
        alert("Aucun étudiant sélectionné à supprimer.");
        return;
    }

    const confirmDelete = confirm("Êtes-vous sûr de vouloir supprimer cet étudiant ? Cette action est irréversible.");
    if (!confirmDelete) {
        return;
    }

    const url = getEtudiantDetailApiUrl(etudiantId);

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (!response.ok) {
             const errorData = await response.json().catch(() => ({error: "Réponse non-JSON", message: response.statusText}));
             throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || errorData.message || response.statusText}`);
        }

        alert("Étudiant supprimé avec succès !");

        // Fermer le modal si ouvert
        const editModalElement = document.getElementById('editEtudiantModal');
        if (editModalElement) {
            const editModal = bootstrap.Modal.getInstance(editModalElement);
            if (editModal) editModal.hide();
        }

        // Recharger la liste des étudiants
        fetchEtudiantsAndDisplay();

    } catch (error) {
        console.error("Erreur lors de la suppression de l'étudiant:", error);
        alert("Échec de la suppression: " + error.message + ". Veuillez vérifier la console.");
    }
}

// Soumet le formulaire de création d'étudiant
async function submitCreateEtudiantForm(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(API_ETUDIANTS_LIST_URL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData // FormData gère automatiquement le Content-Type pour les fichiers
        });

        if (!response.ok) {
            const errorText = await response.text();
            try {
                const errorData = JSON.parse(errorText);
                throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || errorData.message || response.statusText}`);
            } catch (e) {
                throw new Error(`Erreur HTTP! statut: ${response.status} - ${response.statusText} - ${errorText}`);
            }
        }

        const result = await response.json();
        alert(result.message || "Étudiant créé avec succès !");

        // Réinitialiser le formulaire et fermer le modal
        form.reset();
        const createModalElement = document.getElementById('createEtudiantModal');
        const createModal = bootstrap.Modal.getInstance(createModalElement) || new bootstrap.Modal(createModalElement);
        createModal.hide();

        // Recharger la liste des étudiants
        fetchEtudiantsAndDisplay();

    } catch (error) {
        console.error("Erreur lors de la création de l'étudiant:", error);
        alert("Échec de la création: " + error.message + ". Veuillez vérifier la console.");
    }
}


// --- FONCTIONS SPÉCIFIQUES AUX FORUMS ---

// Récupère et affiche la liste des forums
async function fetchForumsAndDisplay() {
    console.log("Tentative de récupération des forums depuis:", API_FORUMS_LIST_URL);
    try {
        const response = await fetch(API_FORUMS_LIST_URL);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${response.statusText} - ${errorText}`);
        }
        const forums = await response.json();
        currentForumsData = forums; // Stocke les données des forums globalement
        console.log("Forums récupérés:", forums);

        populateForumsList(forums);

        if (forums.length > 0) {
            if (forums[0] && typeof forums[0].id === 'number') {
                displayForumDetails(forums[0].id); // Affiche les détails du premier forum par défaut
            } else {
                console.warn("Le premier forum ne contient pas un ID numérique valide:", forums[0]);
                displayNoForumSelectedUI();
            }
        } else {
            console.log("Aucun forum trouvé.");
            displayNoForumSelectedUI();
        }

        // Charger les étudiants pour les sélecteurs (créateur et membres)
        await fetchEtudiantsForSelectors();

    } catch (error) {
        console.error("Erreur lors de la récupération des forums:", error);
        alert("Impossible de charger la liste des forums. Veuillez réessayer. Détails: " + error.message);
        displayNoForumSelectedUI();
    }
}

// Peuple la liste HTML des forums
function populateForumsList(forums) {
    const listElement = document.getElementById('forums-list');
    listElement.innerHTML = ''; // Vide la liste actuelle

    if (forums.length === 0) {
        listElement.innerHTML = '<div class="p-3 text-center text-muted">Aucun forum trouvé.</div>';
        return;
    }

    forums.forEach(forum => {
        const listItem = document.createElement('a');
        listItem.href = "#";
        listItem.className = "list-group-item list-group-item-action forum-item";
        listItem.dataset.forumId = forum.id;
        listItem.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">${forum.nom}</h5>
                <small class="text-muted">Membres: ${forum.nombre_membres}</small>
            </div>
            <p class="mb-1">${forum.description || 'Pas de description.'}</p>
        `;
        listItem.addEventListener('click', (event) => {
            event.preventDefault();
            displayForumDetails(forum.id);
        });
        listElement.appendChild(listItem);
    });
}

// Affiche les détails d'un forum spécifique
async function displayForumDetails(forumId) {
    if (!forumId) {
        displayNoForumSelectedUI();
        return;
    }

    currentlySelectedForumId = forumId; // Met à jour l'ID du forum sélectionné

    const url = getForumDetailApiUrl(forumId);
    if (!url) {
        alert("Erreur: Impossible de générer l'URL de détail du forum.");
        displayNoForumSelectedUI();
        return;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${response.statusText} - ${errorText}`);
        }
        const forumDetail = await response.json();
        console.log("Détails du forum récupérés:", forumDetail);

        updateForumDetailUI(forumDetail); // Met à jour l'interface utilisateur avec les détails du forum

        // Gérer la classe active dans la liste des forums
        document.querySelectorAll('#forums-list .forum-item').forEach(item => {
            item.classList.remove('active');
        });
        const activeForumItem = document.querySelector(`#forums-list .forum-item[data-forum-id="${forumId}"]`);
        if (activeForumItem) {
            activeForumItem.classList.add('active');
        }

        // S'assurer que le bouton d'ajout de membres est visible et prêt
        const addMembersBtn = document.getElementById('add-members-btn');
        if (addMembersBtn) addMembersBtn.style.display = 'block';


    } catch (error) {
        console.error("Erreur lors de l'affichage des détails du forum:", error);
        alert("Impossible de charger les détails du forum. Veuillez réessayer. Détails: " + error.message);
        displayNoForumSelectedUI();
    }
}

// Affiche un message si aucun forum n'est sélectionné ou trouvé
function displayNoForumSelectedUI() {
    const detailView = document.getElementById('forum-detail-view');
    if (detailView) {
        detailView.innerHTML = `
            <h3 id="forum-detail-name">Sélectionnez un forum</h3>
            <p><span class="label">Description :</span> <span class="value" id="forum-detail-description"></span></p>
            <p><span class="label">Créateur :</span> <span class="value" id="forum-detail-creator"></span></p>
            <p><span class="label">Nombre de membres :</span> <span class="value" id="forum-detail-members-count"></span></p>
            <p><span class="label">Date de création :</span> <span class="value" id="forum-detail-date-creation"></span></p>

            <h5 class="mt-4">Membres Actuels du Forum :</h5>
            <ul id="forum-detail-members-list" class="list-group mb-3">
                <li class="list-group-item text-muted">Sélectionnez un forum pour voir ses membres.</li>
            </ul>

            <div class="d-grid gap-2 mb-4">
                <button class="btn btn-info" type="button" data-bs-toggle="modal" data-bs-target="#addMembersModal" id="add-members-btn" disabled>
                    <i class="fas fa-user-plus me-2"></i> Ajouter des Membres
                </button>
            </div>

            <div class="d-flex justify-content-between mt-4">
                <button type="button" class="btn btn-warning" id="edit-forum-btn" data-bs-toggle="modal" data-bs-target="#editForumModal" disabled>
                    Modifier le Forum
                </button>
                <button type="button" class="btn btn-danger" id="delete-forum-btn" disabled>
                    Supprimer le Forum
                </button>
            </div>
        `;
    }
}

// Peuple le sélecteur du créateur de forum (pour les modals de création)
function populateCreatorSelect(etudiants) {
    const selectElementGlobal = document.getElementById('forum-creator-global');
    // const selectElementLocal = document.getElementById('forum-creator-local'); // Si vous en avez un

    const selectors = [selectElementGlobal]; // Ajoutez d'autres sélecteurs ici si nécessaire

    selectors.forEach(selectElement => {
        if (!selectElement) return;

        selectElement.innerHTML = '<option value="">-- Aucun --</option>'; // Option par défaut

        etudiants.forEach(etudiant => {
            const option = document.createElement('option');
            option.value = etudiant.id;
            option.textContent = `${etudiant.nom} ${etudiant.prenom} (${etudiant.matricule})`;
            selectElement.appendChild(option);
        });
    });
}

// Soumet le formulaire de création de forum (global)
async function submitCreateForumGlobalForm(event) {
    event.preventDefault();

    const form = event.target;
    const formData = {
        nom: document.getElementById('create-forum-name-global').value,
        description: document.getElementById('create-forum-description-global').value,
        createur_id: document.getElementById('forum-creator-global').value ? parseInt(document.getElementById('forum-creator-global').value) : null
    };

    try {
        const response = await fetch(API_CREATE_FORUM_GLOBAL_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({error: "Réponse non-JSON", message: response.statusText}));
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || errorData.message || response.statusText}`);
        }

        const result = await response.json();
        alert(result.message || "Forum créé avec succès !");

        form.reset();
        const createModalElement = document.getElementById('createForumModalGlobal');
        const createModal = bootstrap.Modal.getInstance(createModalElement) || new bootstrap.Modal(createModalElement);
        createModal.hide();

        fetchForumsAndDisplay(); // Recharger la liste des forums

    } catch (error) {
        console.error("Erreur lors de la création du forum global:", error);
        alert("Échec de la création: " + error.message + ". Veuillez vérifier la console.");
    }
}

// Soumet le formulaire d'édition de forum
async function submitEditForumForm(event) {
    event.preventDefault();

    const forumId = document.getElementById('edit-forum-id').value;
    const url = getForumDetailApiUrl(forumId);
    if (!url) {
        alert("Erreur: ID du forum introuvable pour la mise à jour.");
        return;
    }

    const formData = {
        nom: document.getElementById('edit-forum-name').value,
        description: document.getElementById('edit-forum-description').value
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
            const errorData = await response.json().catch(() => ({error: "Réponse non-JSON", message: response.statusText}));
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || errorData.message || response.statusText}`);
        }

        const result = await response.json();
        alert(result.message || "Forum mis à jour avec succès !");

        const editModalElement = document.getElementById('editForumModal');
        const editModal = bootstrap.Modal.getInstance(editModalElement) || new bootstrap.Modal(editModalElement);
        editModal.hide();

        displayForumDetails(parseInt(forumId)); // Recharger les détails pour rafraîchir l'UI
        fetchForumsAndDisplay(); // Recharger la liste pour les compteurs et noms

    } catch (error) {
        console.error("Erreur lors de la mise à jour du forum:", error);
        alert("Échec de la mise à jour: " + error.message + ". Veuillez vérifier la console.");
    }
}

// Supprime un forum
async function deleteForum() {
    const forumId = document.getElementById('edit-forum-id').value;
    if (!forumId) {
        alert("Aucun forum sélectionné à supprimer.");
        return;
    }

    const confirmDelete = confirm("Êtes-vous sûr de vouloir supprimer ce forum ? Cette action est irréversible.");
    if (!confirmDelete) {
        return;
    }

    const url = getForumDetailApiUrl(forumId);

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (!response.ok) {
             const errorData = await response.json().catch(() => ({error: "Réponse non-JSON", message: response.statusText}));
             throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || errorData.message || response.statusText}`);
        }

        alert("Forum supprimé avec succès !");

        const editModalElement = document.getElementById('editForumModal');
        if (editModalElement) {
            const editModal = bootstrap.Modal.getInstance(editModalElement);
            if (editModal) editModal.hide();
        }

        fetchForumsAndDisplay(); // Recharger la liste des forums

    } catch (error) {
        console.error("Erreur lors de la suppression du forum:", error);
        alert("Échec de la suppression: " + error.message + ". Veuillez vérifier la console.");
    }
}

// --- FONCTIONS DE GESTION DES MEMBRES DE FORUM ---

// Met à jour l'interface des détails du forum, y compris la liste des membres
function updateForumDetailUI(forumDetail) {
    document.getElementById('forum-detail-name').textContent = forumDetail.nom;
    document.getElementById('forum-detail-description').textContent = forumDetail.description || 'Pas de description.';
    document.getElementById('forum-detail-creator').textContent = forumDetail.createur || 'Inconnu';
    document.getElementById('forum-detail-members-count').textContent = forumDetail.nombre_membres;
    document.getElementById('forum-detail-date-creation').textContent = new Date(forumDetail.date_creation).toLocaleDateString();

    // Met à jour les membres du forum
    const membersList = document.getElementById('forum-detail-members-list');
    membersList.innerHTML = ''; // Nettoyer la liste existante

    if (forumDetail.membres_details && forumDetail.membres_details.length > 0) {
        forumDetail.membres_details.forEach(member => {
            const li = document.createElement('li');
            li.className = "list-group-item d-flex justify-content-between align-items-center";
            li.innerHTML = `
                <span>${member.nom} ${member.prenom}</span>
                <button type="button" class="btn btn-sm btn-danger remove-member-btn" data-member-id="${member.id}">
                    <i class="fas fa-user-minus"></i>
                </button>
            `;
            membersList.appendChild(li);

            // Attacher l'écouteur d'événement pour le bouton de suppression
            li.querySelector('.remove-member-btn').addEventListener('click', () => {
                removeMemberFromForum(forumDetail.id, member.id, `${member.nom} ${member.prenom}`);
            });
        });
    } else {
        membersList.innerHTML = '<li class="list-group-item text-muted">Aucun membre</li>';
    }

    // Mettre à jour les champs du modal d'édition de forum
    const editForumId = document.getElementById('edit-forum-id');
    const editForumName = document.getElementById('edit-forum-name');
    const editForumDescription = document.getElementById('edit-forum-description');
    if (editForumId) editForumId.value = forumDetail.id;
    if (editForumName) editForumName.value = forumDetail.nom;
    if (editForumDescription) editForumDescription.value = forumDetail.description;


    // Mettre à jour les champs du modal d'ajout de membres
    const addMembersModalForumId = document.getElementById('add-members-modal-forum-id');
    const addMembersModalForumName = document.getElementById('add-members-modal-forum-name');
    if (addMembersModalForumId) addMembersModalForumId.value = forumDetail.id;
    if (addMembersModalForumName) addMembersModalForumName.textContent = forumDetail.nom;

    // Repopuler les membres disponibles chaque fois qu'un forum est sélectionné ou mis à jour
    populateAvailableMembersSelect(currentEtudiantsData, forumDetail.id);


    // Activer les boutons d'action du forum
    const editForumBtn = document.getElementById('edit-forum-btn');
    if (editForumBtn) editForumBtn.style.display = 'inline-block';
    const deleteForumBtn = document.getElementById('delete-forum-btn');
    if (deleteForumBtn) deleteForumBtn.style.display = 'inline-block';
}


// Peuple le sélecteur des étudiants disponibles pour l'ajout de membres à un forum
function populateAvailableMembersSelect(allEtudiants, currentForumId) {
    const selectElement = document.getElementById('available-members-select');
    if (!selectElement) return;

    selectElement.innerHTML = ''; // Nettoyer les options existantes

    if (!currentForumId) {
        selectElement.innerHTML = '<option value="" disabled>Sélectionnez un forum d\'abord</option>';
        return;
    }

    // Trouver le forum actuellement sélectionné pour obtenir ses membres
    const currentForum = currentForumsData.find(f => f.id === currentForumId);
    // Extraire les IDs des membres actuels du forum
    const currentMemberIds = currentForum ? currentForum.membres_details.map(m => m.id) : [];

    // Filtrer les étudiants pour n'inclure que ceux qui ne sont PAS déjà membres du forum
    const nonMembers = allEtudiants.filter(etudiant => !currentMemberIds.includes(etudiant.id));

    if (nonMembers.length === 0) {
        const option = document.createElement('option');
        option.value = "";
        option.textContent = "Tous les étudiants sont déjà membres.";
        option.disabled = true;
        selectElement.appendChild(option);
        // Désactiver le bouton d'ajout si tous sont déjà membres
        const submitAddMembersBtn = document.getElementById('submit-add-members-btn');
        if (submitAddMembersBtn) submitAddMembersBtn.disabled = true;
        return;
    } else {
        const submitAddMembersBtn = document.getElementById('submit-add-members-btn');
        if (submitAddMembersBtn) submitAddMembersBtn.disabled = false;
    }

    nonMembers.forEach(etudiant => {
        const option = document.createElement('option');
        option.value = etudiant.id;
        option.textContent = `${etudiant.nom} ${etudiant.prenom} (${etudiant.matricule})`;
        selectElement.appendChild(option);
    });
}


// Ajoute des membres au forum via l'API
async function addMembersToForum() {
    const forumId = document.getElementById('add-members-modal-forum-id').value;
    const selectElement = document.getElementById('available-members-select');
    const selectedMemberIds = Array.from(selectElement.selectedOptions).map(option => parseInt(option.value));

    if (!forumId) {
        alert("Aucun forum sélectionné.");
        return;
    }
    if (selectedMemberIds.length === 0) {
        alert("Veuillez sélectionner au moins un étudiant à ajouter.");
        return;
    }

    const url = `${API_FORUM_MEMBERS_URL_BASE}${forumId}/members/`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ member_ids: selectedMemberIds })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({error: "Réponse non-JSON", message: response.statusText}));
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || errorData.message || response.statusText}`);
        }

        const result = await response.json();
        alert(result.message || "Membres ajoutés avec succès !");

        const addMembersModalElement = document.getElementById('addMembersModal');
        const addMembersModal = bootstrap.Modal.getInstance(addMembersModalElement) || new bootstrap.Modal(addMembersModalElement);
        addMembersModal.hide();

        displayForumDetails(parseInt(forumId)); // Recharger les détails du forum pour rafraîchir l'UI
        fetchForumsAndDisplay(); // Recharger la liste des forums pour mettre à jour le compte de membres

    } catch (error) {
        console.error("Erreur lors de l'ajout de membres:", error);
        alert("Échec de l'ajout de membres: " + error.message + ". Veuillez vérifier la console.");
    }
}


// Retire un membre du forum via l'API
async function removeMemberFromForum(forumId, memberId, memberName) {
    const confirmRemove = confirm(`Êtes-vous sûr de vouloir retirer ${memberName} de ce forum ?`);
    if (!confirmRemove) {
        return;
    }

    const url = `${API_FORUM_REMOVE_MEMBER_URL_BASE}${forumId}/members/${memberId}/remove/`;

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({error: "Réponse non-JSON", message: response.statusText}));
            throw new Error(`Erreur HTTP! statut: ${response.status} - ${errorData.error || errorData.message || response.statusText}`);
        }

        alert(`${memberName} a été retiré du forum.`);

        displayForumDetails(parseInt(forumId)); // Recharger les détails du forum pour rafraîchir l'UI
        fetchForumsAndDisplay(); // Recharger la liste des forums pour mettre à jour le compte de membres

    } catch (error) {
        console.error("Erreur lors du retrait du membre:", error);
        alert("Échec du retrait du membre: " + error.message + ". Veuillez vérifier la console.");
    }
}


// --- INITIALISATION AU CHARGEMENT DE LA PAGE ---
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM entièrement chargé. Initialisation...");

    // Listeners pour la navigation latérale
    document.querySelectorAll('.sidebar .nav-link[data-target]').forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const targetId = link.dataset.target;
            loadContent(targetId);
        });
    });

    // Listeners pour les formulaires et boutons des ÉTUDIANTS
    const createEtudiantForm = document.getElementById('create-etudiant-form');
    if (createEtudiantForm) {
        createEtudiantForm.addEventListener('submit', submitCreateEtudiantForm);
    }

    const etudiantEditForm = document.getElementById('etudiant-edit-form');
    if (etudiantEditForm) {
        etudiantEditForm.addEventListener('submit', submitEtudiantForm);
    }
    const deleteEtudiantBtn = document.getElementById('delete-etudiant-btn');
    if (deleteEtudiantBtn) {
        deleteEtudiantBtn.addEventListener('click', deleteEtudiant);
    }

    // Listeners pour les FORUMS
    const createForumGlobalForm = document.getElementById('create-forum-form-global');
    if (createForumGlobalForm) {
        createForumGlobalForm.addEventListener('submit', submitCreateForumGlobalForm);
    }

    const editForumForm = document.getElementById('edit-forum-form');
    if (editForumForm) {
        editForumForm.addEventListener('submit', submitEditForumForm);
    }
    const deleteForumBtn = document.getElementById('delete-forum-btn');
    if (deleteForumBtn) {
        deleteForumBtn.addEventListener('click', deleteForum);
    }

    // Listeners pour l'ajout/retrait de membres de forum
    const submitAddMembersBtn = document.getElementById('submit-add-members-btn');
    if (submitAddMembersBtn) {
        submitAddMembersBtn.addEventListener('click', addMembersToForum);
    }
    // L'écouteur pour les boutons de suppression de membre est ajouté dynamiquement
    // dans `updateForumDetailUI()` car les boutons sont créés après le chargement du DOM.


    // Charger la section "Étudiants" par défaut au démarrage
    loadContent('etudiants-content');
});