function logout() {
    // Hier verweist du auf die Route /logout und sendest eine GET-Anfrage
    fetch('/logout', {
        method: 'GET'
    })
        .then(response => {
        // Hier wird der Benutzer zurück zur Login-Seite weitergeleitet
        window.location.href = 'login';
        })
        .catch(error => console.error('Error:', error));
  }
