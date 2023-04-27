function createCharts() {
    // Daten für den ersten Chart
    var data1 = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'Request amount',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            data: [12, 19, 3, 5, 2, 3, 7]
        }]
    };

    // Optionen für den ersten Chart
    var options1 = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    };

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

    // Erstellt den ersten Chart
    var ctx1 = document.getElementById('myChart').getContext('2d');
    var myChart1 = new Chart(ctx1, {
        type: 'bar',
        data: data1,
        options: options1
    });

    // Erstellt den zweiten Chart
    var ctx2 = document.getElementById('myChart2').getContext('2d');
    var myChart2 = new Chart(ctx2, {
        type: 'pie',
        data: data2,
        options: options2
    });
}

window.onload = createCharts;
