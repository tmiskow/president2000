function drawResultsPiechart() {
	let data = google.visualization.arrayToDataTable(resultsArray);

	let options = {
	    sliceVisibilityThreshold: .02,
        colors: [
            '#631414',
            '#b12424',
            '#cd7275',
            '#e6b9bd',
            '#FFEBEE'
        ],
        backgroundColor: {
            fill: '#f5f5f5',
            stroke: '#e5e5e5',
            strokeWidth: 2
        }
	};

	let chart = new google.visualization.PieChart(document.getElementById('results-piechart'));
	chart.draw(data, options);
}

function drawResultsBarchart() {
    let data = google.visualization.arrayToDataTable(resultsArray);

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

    let chart = new google.visualization.BarChart(document.getElementById('results-barchart'));
    chart.draw(data, options);
}