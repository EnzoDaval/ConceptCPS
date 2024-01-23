import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {LoadingService} from "../../shared/services/loading.service";

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {
  loading: boolean = false;
  constructor(private loadingService: LoadingService) { }

  ngOnInit(): void {
    this.loadingService.loading$.subscribe(loading => {
      this.loading = loading;
    });
  }



}
