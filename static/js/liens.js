// Obtenir tous les liens de navigation
 const navLinks = document.querySelectorAll('.nav-link');

// Récupérer l'URL actuelle
const currentUrl = window.location.href;

// Ajouter la classe "active" au lien correspondant
navLinks.forEach(link => {
      if (link.href === currentUrl) {
            link.classList.add('active');
      } else {
                link.classList.remove('active');
       }
      });