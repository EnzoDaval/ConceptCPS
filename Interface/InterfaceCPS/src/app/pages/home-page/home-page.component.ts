import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  calculateThePresence(){
    this.http.post('http://localhost:5000/calculate', {})
      .subscribe(response => {
        console.log('Notification envoyée avec succès', response);
      }, error => {
        console.error('Erreur lors de l\'envoi de la notification', error);
      });
  }

}
