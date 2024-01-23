// dashboard-page.component.ts

import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import {DashboardService} from "../../shared/services/dashboard.service";

@Component({
  selector: 'app-dashboard-page',
  templateUrl: './dashboard-page.component.html',
  styleUrls: ['./dashboard-page.component.css']
})
export class DashboardPageComponent implements OnInit {
  imageSrc: string = '';

  constructor(private http: HttpClient, private dashboardService: DashboardService) { }

  ngOnInit(): void {
    this.loadImage();
  }

  loadImage() {
    const apiUrl = 'http://127.0.0.1:5000/get_image';

    this.http.get(apiUrl, { responseType: 'arraybuffer', observe: 'response' })
      .subscribe((response: HttpResponse<ArrayBuffer>) => {
        if (response.status === 200) {
          if (response.body) {
            const base64Image = btoa(String.fromCharCode(...new Uint8Array(response.body)));
            this.imageSrc = `data:image/png;base64,${base64Image}`;

            // Mettez à jour l'URL de l'image dans le service DashboardService
            this.dashboardService.setImageUrl(this.imageSrc);
          } else {
            console.error('Le corps de la réponse est null.');
          }
        } else {
          console.error('Erreur lors de la récupération de l\'image:', response);
        }
      }, error => {
        console.error('Erreur lors de la récupération de l\'image:', error);
      });
  }
}
