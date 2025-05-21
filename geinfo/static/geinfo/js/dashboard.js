<script>
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
        // Convertir l'ID (ex: "user-profile-content") en titre lisible (ex: "USER PROFILE")
        const formattedTitle = targetId.replace(/-content$/, '').replace(/-/g, ' ').toUpperCase();
        pageTitle.textContent = formattedTitle;
    }

    // Gérer les clics sur les liens de la sidebar
    document.addEventListener('DOMContentLoaded', () => {
        const navLinks = document.querySelectorAll('.sidebar .nav-link[data-target]'); // Sélectionne seulement les liens avec data-target
        navLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault(); // Empêche le comportement par défaut du lien (recharger la page)
                const targetId = link.dataset.target; // Récupère la valeur de l'attribut data-target
                loadContent(targetId);
            });
        });

        // Charger le contenu "User Profile" par défaut au chargement de la page
        loadContent('user-profile-content');
    });
</script>