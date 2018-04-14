function drawDonut() {
    console.log(turnout);

    let data = google.visualization.arrayToDataTable([
        ['Turnout', 'Turnout'],
        ['Turnout', turnout],
        ['', 1 - turnout]
    ]);

	let options = {
        pieSliceBorderColor: 'transparent',
        backgroundColor: "#f5f5f5",
        pieStartAngle: (1 - turnout) * 360,
        chartArea: {
            left: 0,
            height: '90%',
            width: 'auto',
		    backgroundColor: {
                stroke: '#e5e5e5',
                strokeWidth: 2
            }
        },
        pieHole: .4,
        pieSliceText: 'none',
        colors: [
            '#C62828',
            'transparent'
        ],
        legend: {position: 'none'}
	};

	let chart = new google.visualization.PieChart(document.getElementById('turnout-donut'));
	chart.draw(data, options);
}

google.charts.load('current', {
	'packages':['geochart', 'corechart', 'bar'],
	// Note: you will need to get a mapsApiKey for your project.
	// See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
	'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
});

function drawCharts() {
    if (drawMap) {
        drawTurnoutMap();
    }

    if (drawBarchart) {
        drawTurnoutBarchart();
    }

    drawDonut();
    drawResultsBarchart();
	drawResultsPiechart();
}

google.charts.setOnLoadCallback(drawCharts);
window.onload = drawCharts;
window.onresize = drawCharts;

document.addEventListener('DOMContentLoaded', function () {
    UIkit.util.on('#results-piechart-container', 'show', function () {
         drawResultsPiechart();
    });

    UIkit.util.on('#results-barchart-container', 'show', function () {
         drawResultsBarchart();
    });

    if (drawBarchart) {
        UIkit.util.on('#turnout-barchart-container', 'show', function () {
            drawTurnoutBarchart();
        });
    }

    if (drawMap) {
        UIkit.util.on('#turnout-map-container', 'show', function () {
             drawTurnoutMap();
        });
    }
});
