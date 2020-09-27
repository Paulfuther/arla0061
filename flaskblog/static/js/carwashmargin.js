$(document).ready(function () {
    $.ajax({
      url: "http://127.0.0.1:5000/carwashmargin",
      method: "GET",
      success: function (newdata4) {
      var datenew4 = [];
      var commissionnew4 = [];
        for (let i=0; i < newdata4.length; i++)  //var i in newdata4)// 
        {
        datenew4.push(newdata4[i].date);
        commissionnew4.push(newdata4[i].commissions);
        console.log(commissionnew4,datenew4);
          }; 
      var chartdata = {
        labels: datenew4,
        datasets: [{
          label: 'C Store Sales',
          fill: false,
          categorySpacing: 0,
          data: commissionnew4,
          
          backgroundColor: '#b3d9ff',
          }]
          };
      var ctx = $("#carwashmargin");
      var barGraph = new Chart(ctx, {
          type: 'bar',
          data: chartdata, 
          options: {
            legend: {display: false},
            scales: {
                xAxes: [{   
                      offset: true,  
                      gridLines: {
                      display: false
                      },
                     ticks: {
                         autoSkip: false,
                         maxRotation: 90,
                         minRotation: 90
                     },    
                    type: 'time',           
                    time: {
                    parser: "DD-MMM-YYYY HH:mm:ss",
                    unit: 'month',
                    displayFormats: {
                    month: 'MMM YY',
                },
                } 
                }],
                yAxes:[{
                    stacked: true,
                    gridLines:{
                        display:false
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
             }
           }
      })
    },
  });
});