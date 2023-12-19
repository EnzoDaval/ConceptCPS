import {Component, Input, OnInit} from '@angular/core';
import {SettingComponent} from "../../shared/components/setting/setting.component";

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
  fetchFrequency: number = 1;
  settings: { [key: string]: SettingData } = {
    camera: { percentage: 20, sliderValue: 0 },
    bluetooth: { percentage: 30, sliderValue: 0 },
    wifi: { percentage: 50, sliderValue: 0 }
  };
  constructor() { }

  ngOnInit(): void {
  }

  onSliderChange(setting: string, value: number) {
    console.log("slider change")
    this.settings[setting].sliderValue = value;
  }
  generateJsonFile() {
    const settingsData: SettingsData = {
      fetchFrequency: this.fetchFrequency,
      camera: { percentage: this.settings['camera'].percentage, sliderValue: this.settings['camera'].sliderValue },
      bluetooth: { percentage: this.settings['bluetooth'].percentage, sliderValue: this.settings['bluetooth'].sliderValue },
      wifi: { percentage: this.settings['wifi'].percentage, sliderValue: this.settings['wifi'].sliderValue },
    };


    const jsonContent = JSON.stringify(settingsData, null, 2);
    console.log(jsonContent);

    // Enregistrez le fichier JSON ou effectuez l'action nécessaire avec le contenu JSON
    // Par exemple, vous pouvez utiliser FileSaver.js pour enregistrer le fichier localement.
    // Consultez https://github.com/eligrey/FileSaver.js/ pour plus d'informations.

    // Exemple d'utilisation de FileSaver.js
    // import * as FileSaver from 'file-saver';
    // const blob = new Blob([jsonContent], { type: 'application/json' });
    // FileSaver.saveAs(blob, 'settings.json');
  }


}
