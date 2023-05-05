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

function setbutton() {
  document.getElementById('check-button').addEventListener('click', function() {
    var url = document.getElementById('url-input').value;
    var data = { 'url': url };
    var options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    };
    fetch('/check-url', options)
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        var result = JSON.stringify(data, null, 2);
        document.getElementById('result').innerText = result;
      })
      .catch(function(error) {
        console.log(error);
      });
  });
}
window.onload = setbutton;