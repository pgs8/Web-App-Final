<canvas id="myChart" width="400" height="400"></canvas>

<script>
    const config = {
  type: 'bar',
  data: data,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Chart.js Bar Chart'
      }
    }
  },
};
</script>

<script>
const DATA_COUNT = 12;
const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

const labels = Utils.months({count: 12});
const data = {
  labels: labels,
  datasets: [
    {
      label: 'YEAR 1958',
      data: Utils.numbers(340, 318, 362, 348, 363, 435, 491, 505, 404, 359, 310, 337),
      borderColor: Utils.CHART_COLORS.red,
      backgroundColor: Utils.transparentize(Utils.CHART_COLORS.red, 0.5),
    },
    {
      label: 'YEAR 1959',
      data: Utils.numbers(360, 342, 406, 396, 420, 472, 548, 559, 463, 407, 362, 405),
         borderColor: Utils.CHART_COLORS.blue,
      backgroundColor: Utils.transparentize(Utils.CHART_COLORS.blue, 0.5),
    },
    {
      label: 'YEAR 1960',
      data: Utils.numbers(417, 391, 419, 461, 472, 535, 622, 606, 508, 461, 390, 432),
         borderColor: Utils.CHART_COLORS.yellow,
      backgroundColor: Utils.transparentize(Utils.CHART_COLORS.yellow, 0.5),
    }
  ]
};
</script>


  // === include 'setup' then 'config' above ===

  var myChart = new Chart(
    document.getElementById('myChart'),
    config
  );
</script>
