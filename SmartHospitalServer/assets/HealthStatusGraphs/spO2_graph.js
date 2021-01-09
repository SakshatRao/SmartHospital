// Graphing SpO2 values

var $spO2Graph = $(".spO2_graph");
var spO2_ctx = $spO2Graph[0].getContext("2d");

var spO2_myChart = new Chart(spO2_ctx, {
    type: 'line',
    data: {
        labels: ['', '', ''],
        datasets: [{
            label: 'SpO2',
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
                    min: 90,
                    max: 110,
                    fontColor: 'white',
                    fontSize: 15
                },
                scaleLabel: {
                    display: true,
                    labelString: 'SpO2 %',
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
        url: $spO2Graph.data("url"),
        type: 'GET',
        data: {patient_id: document.getElementById('patient-id').value},
        success: function (data) {
            spO2_myChart.data.datasets[0].data = data.spO2s;
            spO2_myChart.data.labels = data.timeline;
            spO2_myChart.options.scales.xAxes[0].scaleLabel.fontSize = data.axesLabelSize;
            spO2_myChart.options.scales.xAxes[0].scaleLabel.labelString = data.axesLabel;
            spO2_myChart.options.scales.xAxes[0].scaleLabel.fontColor = data.axesLabelColor;
            spO2_myChart.update();
        }
    });
}, 5 * 1000);