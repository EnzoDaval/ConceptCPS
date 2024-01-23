import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatSidenavModule} from "@angular/material/sidenav";
import {MatIconModule} from "@angular/material/icon";
import { TabComponent } from './shared/components/tab/tab.component';
import {MatTableModule} from "@angular/material/table";
import { VerticalChartComponent } from './shared/components/vertical-chart/vertical-chart.component';
import {MatSliderModule} from "@angular/material/slider";
import {FormsModule} from "@angular/forms";
import { SettingsPageComponent } from './pages/settings-page/settings-page.component';
import { DashboardPageComponent } from './pages/dashboard-page/dashboard-page.component';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { AppRoutingModule } from './app-routing.module';
import { SettingComponent } from './shared/components/setting/setting.component';
import {HttpClientModule} from "@angular/common/http";
import { ClasseComponent } from './shared/components/classe/classe.component';

@NgModule({
  declarations: [
    AppComponent,
    TabComponent,
    VerticalChartComponent,
    SettingsPageComponent,
    DashboardPageComponent,
    HomePageComponent,
    SettingComponent,
    ClasseComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatSidenavModule,
    MatIconModule,
    MatTableModule,
    MatSliderModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
