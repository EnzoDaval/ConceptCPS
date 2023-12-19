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
  @Input() sliderValue: number = 50;

  @Output() sliderChange: EventEmitter<number> = new EventEmitter<number>();

  tickInterval: number = 10;
  tickLabels: string[] = Array.from({ length: 11 }, (_, i) => (i * 10).toString());

  onSliderChange(event: any) {
    console.log("change in slider");
    this.sliderValue = event.value;
    this.sliderChange.emit(this.sliderValue);
  }
}
