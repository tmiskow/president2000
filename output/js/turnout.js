function drawTurnoutMap() {
	let data = google.visualization.arrayToDataTable(turnoutArray);

	let options = {
		region: 'PL',
		resolution: 'provinces',
		colorAxis: {
		    colors: [
                '#FFCDD2',
                '#C62828'
            ]
        },
        width: '100%',
        height: '100%',
        chartArea: {
		    width: '100%',
            height: '100%'
        },
		backgroundColor: {
		    fill: '#f5f5f5',
			stroke: '#e5e5e5',
			strokeWidth: 2
		}
	};

	let chart = new google.visualization.GeoChart(document.getElementById('turnout-map'));
	chart.draw(data, options);
}

function drawTurnoutBarchart() {
    let data = google.visualization.arrayToDataTable(turnoutArray);

    let options = {
        colors: ['#C62828'],
        chart: {
            title: 'Company Performance',
            subtitle: 'Sales, Expenses, and Profit: 2014-2017',
        },
        bars: 'horizontal',
        legend: {position: 'none'},
        width: '100%',
        height: '100%',
        chartArea: {
		    width: '55%',
            height: '80%'
        },
        backgroundColor: {
            fill: '#f5f5f5',
            stroke: '#e5e5e5',
            strokeWidth: 2
        }
    };

    let chart = new google.visualization.BarChart(document.getElementById('turnout-barchart'));
    chart.draw(data, options);
}