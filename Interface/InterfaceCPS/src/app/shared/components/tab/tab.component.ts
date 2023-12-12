import { Component, OnInit } from '@angular/core';

export interface CourseExample {
  nom: string;
  prenom: string;
  classe: string;
  certitudePercentage: number;
  presence: boolean;
}

const ELEMENT_DATA: CourseExample[] = [
  {nom: 'DAVAL', prenom: 'Enzo', classe: 'SI5-IOT', certitudePercentage: 95, presence: true},
  {nom: 'PERRAUDEAU', prenom: 'Emilien', classe: 'SI5-IHM', certitudePercentage: 90, presence: false},
  {nom: 'TRICOT', prenom: 'Thomas', classe: 'SI5-IHM', certitudePercentage: 92, presence: true},
  {nom: 'LORCERY', prenom: 'Morgane', classe: 'SI5-IHM', certitudePercentage: 95, presence: true},
];



@Component({
  selector: 'app-tab',
  templateUrl: './tab.component.html',
  styleUrls: ['./tab.component.css']
})
export class TabComponent implements OnInit {

  dataSource = ELEMENT_DATA;
  displayedColumns: string[] = ['nom', 'prenom', 'classe', 'certitudePercentage', 'presence'];

  constructor() { }

  ngOnInit(): void {
  }

}
