// Graphing temperature values

var $temperatureGraph = $(".temperature_graph");
var temperature_ctx = $temperatureGraph[0].getContext("2d");

var temperature_myChart = new Chart(temperature_ctx, {
    type: 'line',
    data: {
        labels: ['', '', ''],
        datasets: [{
            label: 'Temperature',
            data: [0, 0, 0],
            fill: false,
            borderWidth: 3,
            borderColor: '#90BEDE',
            pointRadius: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
            display: false,
        },
        title: {
            display: false,
        },
        scales: {
            yAxes: [{
                ticks: {
                    min: 30,
                    max: 40,
                    fontColor: 'white',
                    fontSize: 15
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Temperature (in Celcius)',
                    fontSize: 20,
                    fontColor: 'white'
                },
                gridLines: {
                    display: true,
                    color: 'rgb(255, 255, 255, 0.2)'
                }
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Loading Data',
                    fontSize: 15,
                    fontColor: 'white'
                },
                gridLines: {
                    display: false
                },
                ticks: {
                    autoSkip: false,
                    minRotation: 0,
                    maxRotation: 0,
                    padding: 5,
                    fontColor: 'white'
                }
            }],
        }
    }
});

setInterval(function () {
    $.ajax({
        url: $temperatureGraph.data("url"),
        type: 'GET',
        data: {patient_id: document.getElementById('patient-id').value},
        success: function (data) {
            temperature_myChart.data.datasets[0].data = data.temperatures;
            temperature_myChart.data.labels = data.timeline;
            temperature_myChart.options.scales.xAxes[0].scaleLabel.fontSize = data.axesLabelSize;
            temperature_myChart.options.scales.xAxes[0].scaleLabel.labelString = data.axesLabel;
            temperature_myChart.options.scales.xAxes[0].scaleLabel.fontColor = data.axesLabelColor;
            temperature_myChart.update();
        }
    });
}, 5 * 1000);