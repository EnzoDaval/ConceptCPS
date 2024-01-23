import { HttpClient } from "@angular/common/http";
import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-classe',
  templateUrl: './classe.component.html',
  styleUrls: ['./classe.component.css']
})
export class ClasseComponent implements OnInit {
  @Input() className: string = 'Classe';
  @Input() classNumber: string = '';

  constructor(private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
  }

  calculateThePresence() {
    const requestData = {
      classNumber: this.classNumber
    };

    this.http.post('http://127.0.0.1:5000/calculate', requestData)
      .subscribe(response => {
        console.log('Notification envoyée avec succès', response);

        // Après avoir reçu la notification avec succès, chargez l'image mise à jour
        this.router.navigate(['/dashboard']);
      }, error => {
        console.error('Erreur lors de l\'envoi de la notification', error);
      });
  }

}
