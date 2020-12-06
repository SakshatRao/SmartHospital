var $bpmGraph = $(".bpm_graph");
var bpm_ctx = $bpmGraph[0].getContext("2d");

var bpm_myChart = new Chart(bpm_ctx, {
    type: 'line',
    data: {
        labels: ['', '', ''],
        datasets: [{
            label: 'BPM',
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
                    min: 0,
                    max: 120,
                    fontColor: 'white',
                    fontSize: 15
                },
                scaleLabel: {
                    display: true,
                    labelString: 'BPM',
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
        url: $bpmGraph.data("url"),
        type: 'GET',
        data: {patient_id: document.getElementById('patient-id').value},
        success: function (data) {
            bpm_myChart.data.datasets[0].data = data.bpms;
            bpm_myChart.data.labels = data.timeline;
            bpm_myChart.options.scales.xAxes[0].scaleLabel.fontSize = data.axesLabelSize;
            bpm_myChart.options.scales.xAxes[0].scaleLabel.labelString = data.axesLabel;
            bpm_myChart.options.scales.xAxes[0].scaleLabel.fontColor = data.axesLabelColor;
            bpm_myChart.update();
        }
    });
}, 5 * 1000);