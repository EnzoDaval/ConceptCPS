import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-setting',
  templateUrl: './setting.component.html',
  styleUrls: ['./setting.component.css']
})
export class SettingComponent {
  @Input() icon: string = 'settings';
  @Input() title: string = 'Setting Title';
  @Input() percentage: number = 50;
  @Input() sliderValue: number = 15;

  @Output() sliderChange: EventEmitter<number> = new EventEmitter<number>();
  @Output() percentageChange: EventEmitter<number> = new EventEmitter<number>();

  tickInterval: number = 1;
  tickLabels: string[] = Array.from({ length: 18 }, (_, i) => (i * 2 + 1).toString());

  onSliderChange(event: any) {
    this.sliderValue = event.value;
    this.sliderChange.emit(this.sliderValue);
  }

  onPercentageChange(event: any) {
    console.log(event);
    this.percentageChange.emit(this.percentage);
  }
}
