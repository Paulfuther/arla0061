$(document).ready(function () {
    $.ajax({
      url: "http://127.0.0.1:5000/cstoresales",
      method: "GET",
      success: function (newdata) {
      var datenew = [];
      var marginnew = [];
        for (let i=0; i < newdata.length; i++)  //var i in newdata)// 
        {
        datenew.push(newdata[i].date);
        marginnew.push(newdata[i].sales);
          }; 
      var chartdata = {
        labels: datenew,
        datasets: [{
          label: 'C Store Sales',
          fill: false,
          data: marginnew,
          backgroundColor: '#b3d9ff',
          }]
          };
      var ctx = $("#storemargin");
      var barGraph = new Chart(ctx, {
          type: 'line',
          data: chartdata, 
            options: {
              legend: {
                display: false
              },
              scales: {
                xAxes: [{
                  offset: true,
                  ticks: {
                    autoSkip: false,
                        autoSkip: false,
                        maxRotation: 90,
                        minRotation: 90,  
                    beginAtZero: true,
                  },
                  gridLines:{
                    display:false},
                    type: 'time',
                    time: {
                      parser: "DD-MMM-YYYY HH:mm:ss",
                      unit: 'month',                   
                      displayFormats: {
                      month: 'MMM YY',}
                    }
              }],
             yAxes:[{
               gridLines:{
                 display:false
               },
               ticks: {
                 beginAtZero:false
               }
             }]
             }
           }
      })
    },
  });
});