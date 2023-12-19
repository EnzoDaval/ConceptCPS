import {Component, Input, OnInit} from '@angular/core';
import * as saveAs from 'file-saver';

interface SettingsData {
  fetchFrequency: number;
  camera: SettingData;
  bluetooth: SettingData;
  wifi: SettingData;
}

interface SettingData {
  percentage: number;
  sliderValue: number;
}

@Component({
  selector: 'app-settings-page',
  templateUrl: './settings-page.component.html',
  styleUrls: ['./settings-page.component.css']
})
export class SettingsPageComponent implements OnInit {
  fetchFrequency: number = 15;
  settings: { [key: string]: SettingData } = {
    camera: { percentage: 20, sliderValue: 50 },
    bluetooth: { percentage: 30, sliderValue: 50 },
    wifi: { percentage: 50, sliderValue: 50 }
  };
  constructor() { }

  ngOnInit(): void {
  }

  onSliderChange(setting: string, value: number) {
    this.settings[setting].sliderValue = value;
  }

  onPercentageChange(setting: string, value: number) {
    this.settings[setting].percentage = value;
  }
  generateJsonFile() {
    if (this.getSumOfPercentages() !== 100) {
      alert('La somme des pourcentages doit être égal à 100');
      return;
    }

    const settingsData: SettingsData = {
      fetchFrequency: this.fetchFrequency,
      camera: { percentage: this.settings['camera'].percentage, sliderValue: this.settings['camera'].sliderValue },
      bluetooth: { percentage: this.settings['bluetooth'].percentage, sliderValue: this.settings['bluetooth'].sliderValue },
      wifi: { percentage: this.settings['wifi'].percentage, sliderValue: this.settings['wifi'].sliderValue },
    };

    const jsonContent = JSON.stringify(settingsData, null, 2);
    console.log(jsonContent);

    const blob = new Blob([jsonContent], { type: 'application/json' });
    saveAs(blob, 'settings.json');
  }

  private getSumOfPercentages(): number {
    return Object.values(this.settings).reduce(
      (sum, setting) => sum + setting.percentage,
      0
    );
  }
}
