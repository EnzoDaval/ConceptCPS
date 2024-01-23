// loading.service.ts

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoadingService {
  private loadingSubject: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  // Observable pour permettre aux composants de s'abonner à l'état de chargement
  loading$: Observable<boolean> = this.loadingSubject.asObservable();

  // Méthode pour mettre à jour l'état de chargement
  setLoading(loading: boolean): void {
    this.loadingSubject.next(loading);
  }
}
