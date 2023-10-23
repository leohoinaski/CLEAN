
var ctx = document.getElementById('myChart');


var graphData = {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', ''],
        datasets: [{
            label: 'datas',
            data: [0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
            ],
            fill: true
        }]
    },
    options: {
        bezierCurve: true,
        scales: {
            x: {
                ticks: {
                    // Include dynamic date in x axe
                    callback: function(value, index, values) {
                        var date = new Date();
                        return ((date.getDate() )) + "/" + ((date.getMonth() + 1)) + "/" + date.getFullYear() + '-' + date.getHours() + ':' + date.getMinutes() +':' + date.getSeconds(); 
                    }
                }
            }
        }
    }
}

function addDataLinear(chart, label, data) {

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
	document.querySelector('#app').innerText = djangoData.value;
	document.querySelector('#app1').innerText = djangoData.date;
	addDataLinear(myChart, 1, djangoData.value)

}

