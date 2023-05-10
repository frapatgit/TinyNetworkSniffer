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


function createCharts() {
    let labels = [];
    let counts = [];
    // Holen der Daten aus Flask-Route
    fetch('/charts')
        .then(response => response.json())
        .then(data => {
            // Extrahieren der Daten aus dem JSON-Objekt
            labels = data.map(row => row[0]);
            counts = data.map(row => row[1]);
            console.log(labels)
            console.log(counts)
            // Erstellen des Chart.js-Datasets
            const dataset = {
                label: 'Requests',
                data: counts,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            };
            var data1 = {
                labels:  labels,
                datasets: [dataset]
            };
            var options1 = {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            };
            var ctx1 = document.getElementById('myChart').getContext('2d');
            var myChart1 = new Chart(ctx1, {
                type: 'bar',
                data: data1,
                options: options1
            });
        })

    // Daten für den zweiten Chart
    var data2 = {
        labels: ['Smart TV', 'Smartphone', 'PC'],
        datasets: [{
            label: 'Dataset 2',
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 1,
            data: [12, 19, 3]
        }]
    };

    // Optionen für den zweiten Chart
    var options2 = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    };

 

    // Erstellt den zweiten Chart
    var ctx2 = document.getElementById('myChart2').getContext('2d');
    var myChart2 = new Chart(ctx2, {
        type: 'pie',
        data: data2,
        options: options2
    });
}

window.onload = createCharts;