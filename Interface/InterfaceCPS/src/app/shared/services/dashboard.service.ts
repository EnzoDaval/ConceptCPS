// dashboard.service.ts

import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  private imageUrl: string = '';

  setImageUrl(url: string) {
    this.imageUrl = url;
  }

  getImageUrl(): string {
    return this.imageUrl;
  }
}
