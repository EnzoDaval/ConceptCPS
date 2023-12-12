import {Component, Input, OnInit} from '@angular/core';
import {SettingComponent} from "../../shared/components/setting/setting.component";

@Component({
  selector: 'app-settings-page',
  templateUrl: './settings-page.component.html',
  styleUrls: ['./settings-page.component.css']
})
export class SettingsPageComponent implements OnInit {

  @Input() title = "Réglage"
  constructor() { }

  ngOnInit(): void {
  }

}
