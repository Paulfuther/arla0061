$(document).ready(function(){
    $.ajax({
      url: "http://127.0.0.1:5000/cstoremargin",       
      method: "GET",
      success: function (newdata3) {
      var datenew3 = [];
      var volume3 = [];
      var store3 =[];
        for (var i in newdata3) {
          datenew3.push(newdata3[i].date);
          volume3.push(newdata3[i].margin);
          store3.push(newdata3[i].margin)
           };
      var chartdata = {
        labels: datenew3,
        datasets: [{
          label: 'Margin $',
          data: volume3,
          backgroundColor: '#b3d9ff',
          }]
          };
      var ctx = $("#cstoremargin");
      var barGraph = new Chart(ctx, {
          type: 'doughnut',
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
                    unit: 'month',
                    displayFormats: {
                        'day': 'MMM YY',
                        'week': 'MMM YY',
                        'month': 'MMM YY',
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
