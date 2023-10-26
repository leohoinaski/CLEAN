
var ctx = document.getElementById('myChart');


var graphData = {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', '','', '', '', '', '', '', '','', '', '', '', '', '', ''],
        datasets: [{
            label: 'datas',
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
                'rgba(75, 192, 192, 0.5)'
            ],
            fill: true
        }]
    }
}

function addDataLinear(chart, label, data) {
    chart.data.labels.push(label);
    var newGraphData = graphData.data.datasets[0].data;
    newGraphData.shift();
    newGraphData.push(data);
    graphData.data.datasets[0].data = newGraphData;
    chart.update();
}

var myChart = new Chart(ctx, graphData);
var socket = new WebSocket('ws://localhost:8000/ws/CLEANview/');

socket.onmessage = function(e){

	var djangoData = JSON.parse(e.data);
	console.log(djangoData);

    var newGraphData = graphData.data.datasets[0].data;
    newGraphData.shift();
    newGraphData.push(djangoData.value);

    graphData.data.datasets[0].data = newGraphData;
    myChart.update();
}

