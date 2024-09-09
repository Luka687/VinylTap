import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    redirectTo: '/records',
    pathMatch: 'full'
  },
  {
    path: '',
    redirectTo: '/records',
    pathMatch: 'full'
  },
  {
    path: 'record/:id',
    loadComponent: () => import('./components/record-details/record-details.component').then(m => m.RecordDetailsComponent),
  },
  {
    path: 'records',
    loadComponent: () => import('./components/record-grid/record-grid.component').then(m => m.RecordGridComponent),
  },
  {
    path: 'records/search',
    loadComponent: () => import('./components/record-grid/record-grid.component').then(m => m.RecordGridComponent)
  }
  ,
  {
    path: 'login',
    loadComponent: () => import('./components/login/login.component').then(m => m.LoginComponent)
  }
];
