
$(document).ready(function(){
    $.ajax({
      url: "http://127.0.0.1:5000/cstoresales",
      method: "GET",
      success: function(newdata) {   
      var datenew = [];
      var marginnew = [];
      i=0
      for(var i in newdata) {
        datenew.push(newdata[i].date);
        marginnew.push(newdata[i].margin);
        }
       
      var chartdata = {
          //labels: ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"],
          labels: datenew,
          datasets : [
            {
              label: 'C Store Margin Dollars',
              fill: false,
              data: marginnew,
              backgroundColor: '#b3d9ff',
              borderColor: 'blue',
            }
          ]
        };
  
      var ctx = $("#storemargin2");
  
      var barGraph = new Chart(ctx, {
          type: 'bar',
          data: chartdata,
          options: {
            responsive:true,
            scales: {
              xAxes: [{
                type: 'time',
                //distribution: 'series',
                time: {
                  unit: 'month',
                  
                  //min: datenew[2],
                  //max: datenew[12],
                  displayFormats: {
                   
                   'day': 'MMM DD',
                   'month': 'MMM',
                    'quarter': 'MMM YY',
                    'year': 'MMM YY',
                  }
                },
                ticks: {
                  source: 'data',
                  beginAtZero: true
               }
              }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
        });
      },
    });
} );