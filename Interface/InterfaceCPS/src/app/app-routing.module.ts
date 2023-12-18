import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HomePageComponent} from "./pages/home-page/home-page.component";
import {DashboardPageComponent} from "./pages/dashboard-page/dashboard-page.component";
import {SettingsPageComponent} from "./pages/settings-page/settings-page.component";

const routes: Routes = [
  { path: 'home', component: HomePageComponent },
  { path: 'dashboard', component: DashboardPageComponent },
  { path: 'settings', component: SettingsPageComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
