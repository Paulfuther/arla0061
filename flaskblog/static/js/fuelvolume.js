$(document).ready(function(){
    $.ajax({
      url: "http://127.0.0.1:5000/data",       
      method: "GET",
      success: function (newdata2) {
      var datenew2 = [];
      var volume2 = [];
        for (var i in newdata2) {
          datenew2.push(newdata2[i].date);
          volume2.push(newdata2[i].volume);
           };
      var chartdata = {
        labels: datenew2,
        datasets: [{
          label: 'Fuel Volume',
          data: volume2,
          backgroundColor: '#b3d9ff',
          }]
          };
      var ctx = $("#mycanvas");
      var barGraph = new Chart(ctx, {
          type: 'bar',
          data: chartdata,
            options: {
              legend: {
                display: false
              },
              scales: {
                xAxes: [{
                  gridLines:{
                    display:false
                    },
                    type: 'category',
                    time: {
                      parser: "MMM",
                      unit: 'day',
                      displayFormats: {
                        day: 'MMM YY',
                        'week': 'MMM YY',
                         month: 'MMM',
                        'quarter': 'MMM YY',
                        'year': 'MMM YY',
                        },
                        
                      }
                }],
              
                yAxes: [{
                    gridLines: {
                      display: false
                    },
                    ticks:{
                      beginAtZero: true
                    }
                  }]
                }
              }
              
      })
      },
    });
  });
