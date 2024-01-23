import {Component, Input, OnInit} from '@angular/core';
import * as saveAs from 'file-saver';
import { writeFile } from 'fs';
import { resolve } from 'path';
import {HttpClient} from "@angular/common/http";

interface SettingsData {
  //fetchFrequency: number;
  camera: number;
  bluetooth:  number;
  wifi: number;
}

interface SettingData {
  //percentage: number;
  sliderValue: number;
}

@Component({
  selector: 'app-settings-page',
  templateUrl: './settings-page.component.html',
  styleUrls: ['./settings-page.component.css']
})
export class SettingsPageComponent implements OnInit {
  //fetchFrequency: number = 15;
  settings: { [key: string]: SettingData } = {
    camera: { sliderValue: 50 },
    bluetooth: { sliderValue: 50 },
    wifi: { sliderValue: 50 }
  };
  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  onSliderChange(setting: string, value: number) {
    this.settings[setting].sliderValue = value;
  }

  onPercentageChange(setting: string, value: number) {
    //this.settings[setting].percentage = value;
  }
  generateJsonFile() {
    const settingsData: SettingsData = {
      camera: this.settings['camera'].sliderValue,
      bluetooth: this.settings['bluetooth'].sliderValue,
      wifi: this.settings['wifi'].sliderValue,
    };

    this.http.post('http://127.0.0.1:5000/configs', settingsData).subscribe(
      (response) => {
        console.log('Settings updated successfully on the server:', response);
      },
      (error) => {
        console.error('Error updating settings on the server:', error);
      }
    );
  }

  private getSumOfPercentages(): number {
    //return Object.values(this.settings).reduce(
      //(sum, setting) => sum + setting.percentage,
      //0
    //);
    return 0;
  }
}
