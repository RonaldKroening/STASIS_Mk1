        var idx = 1;
        function changeText() {
            document.getElementById("text").textContent = "You clicked the button!";
        }

        const ctx = document.getElementById('myChart').getContext('2d');

        function generateRandomData(points) {
            return Array.from({ length: points }, () => Math.floor(Math.random() * 100));
        }

        let data = {
            labels: Array.from({ length: 30 }, (_, i) => `Day ${i + 1}`),
            datasets: [{
                label: 'Random Data',
                data: generateRandomData(30),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        };

        // Create the chart
        const myChart = new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        function formatMoney(value) {
            if (typeof value === 'object' && value.$numberDouble !== undefined) {
                value = parseFloat(value.$numberDouble);
            }else if (typeof value === 'string' && !isNaN(value)) {
                value = parseFloat(value);
            }else{
                return;
            }
            if (value >= 1e12) {
                return `$${(value / 1e12).toFixed(3)} T`;
            } else if (value >= 1e9) {
                return `$${(value / 1e9).toFixed(3)} B`;
            } else if (value >= 1e6) {
                return `$${(value / 1e6).toFixed(3)} M`;
            } else if (value >= 1e3) {
                return `$${(value / 1e3).toFixed(3)} K`;
            } else {
                return `$${value.toFixed(2)}`;
            }
        }
        function loadData() {
            fetch('dummydata.json')
                .then(response => response.json())
                .then(dataAsJSON => {
                    fillTable(dataAsJSON["marketItems"]);
                    
                })
                .catch(error => console.error('Error loading JSON:', error));
        }
        function fillTable(json){
            let entries = Object.entries(json); // Convert object to array of entries
                    for (let [key, value] of entries) {
                        value = formatMoney(value);
                        console.log(key, " ", value);
                        let new_tr = document.createElement('tr');
                        new_tr.innerHTML = `<td>${key}</td><td>${value.$numberDouble || value}</td>`; // Access value correctly
                        document.getElementById("company-table").appendChild(new_tr);
                    }
        }
        function predict(){
            const v = "";
        }

        function updateChart(timeframe) {
            let points;
            let labels;
            switch (timeframe) {
                case 'day':
                    points = 24;
                    idx = 1;
                    labels = Array.from({ length: points }, (_, i) => `Hour ${i + 1}`);
                    break;
                case 'week':
                    points = 7;
                    idx = 2;
                    labels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
                    break;
                case 'month':
                    points = 30;
                    idx = 3;
                    labels = Array.from({ length: points }, (_, i) => `Day ${i + 1}`);
                    break;
                case 'year':
                    points = 12;
                    idx= 4;
                    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
                    break;
                default:
                    points = 30;
                    labels = Array.from({ length: points }, (_, i) => `Day ${i + 1}`);
            }
        
            const newData = generateRandomData(points);
            myChart.data.labels = labels;
            myChart.data.datasets[0].data = newData;
            myChart.update();
        
            const highestPoint = Math.max(...newData);
            const lowestPoint = Math.min(...newData);
            const currentPoint = newData[newData.length - 1];
            const startPoint = newData[0];
            const percentageChange = ((currentPoint - startPoint) / startPoint) * 100;
        
            const ncdv = document.getElementById("navinfoholders");
            ncdv.innerHTML = 
            `<h3>Current: ${currentPoint} | </h3>
            <h3> High: ${highestPoint}  | </h3>
            <h3> Low: ${lowestPoint} | </h3>
            <h3> % Change: ${percentageChange.toFixed(2)}%</h3>`;
            console.log(ncdv);
        }
        
        
        // Load data on page load
        window.onload = loadData;
        updateChart("day");
