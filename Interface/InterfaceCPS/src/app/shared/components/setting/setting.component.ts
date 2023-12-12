import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-setting',
  templateUrl: './setting.component.html',
  styleUrls: ['./setting.component.css']
})
export class SettingComponent {
  @Input() icon: string = 'settings';
  @Input() title: string = 'Setting Title';
  @Input() percentage: number = 50;
  sliderValue: number = 50;

  // Définissez les niveaux (étiquettes) et l'intervalle souhaités
  tickInterval: number = 10;
  tickLabels: string[] = Array.from({ length: 11 }, (_, i) => (i * 10).toString());

  // Update the percentage when the slider value changes
  onSliderChange(event: any) {
    this.percentage = event.value;
  }
}
