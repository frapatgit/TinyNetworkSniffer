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

  function loadtable() {
    // Datenbank-Abfrage, um alle Domains abzurufen
    fetch("/")
      .then(response => response.json())
      .then(data => {
        // Selektiert die Tabelle und leert sie
        const table = document.querySelector("table tbody");
        table.innerHTML = "";
        
        // Fügt jede Domain als neue Zeile in die Tabelle ein
        data.forEach(domain => {
          const row = table.insertRow();
          const destinationCell = row.insertCell();
          const hostCell = row.insertCell();
          const countCell = row.insertCell();

          destinationCell.innerText = dns_queries.destination_ip;
          hostCell.innerText = dns_queries.source_ip; // Hier muss der Host der Domain ermittelt werden
          countCell.innerText = dns_queries.destination_ip;
        });
      })
      .catch(error => console.error(error));
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