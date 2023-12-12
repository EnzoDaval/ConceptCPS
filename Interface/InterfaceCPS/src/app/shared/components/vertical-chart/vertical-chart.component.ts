import { Component, Input, OnInit } from '@angular/core';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-vertical-chart',
  templateUrl: './vertical-chart.component.html',
  styleUrls: ['./vertical-chart.component.css']
})
export class VerticalChartComponent implements OnInit {
  @Input() chartLabels: string[] = [];
  @Input() chartData: string[] = [];
  @Input() chartDataName: string = "";

  public chart: any;

  ngOnInit(): void {
    this.createChart();
  }

  createChart() {
    this.chart = new Chart("MyChart", {
      type: 'bar',

      data: {
        labels: this.chartLabels,
        datasets: [
          {
            label: this.chartDataName,
            data: this.chartData,
            backgroundColor: 'blue'
          }
        ]
      },
      options: {
        aspectRatio: 2.5
      }
    });
  }
}
