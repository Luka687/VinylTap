import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
  },
  {
    path: 'record/:id',
    loadComponent: () => import('./components/record-details/record-details.component').then(m => m.RecordDetailsComponent),
  },
  {
    path: '',
    loadComponent: () => import('./components/record-grid/record-grid.component').then(m => m.RecordGridComponent),
  }
];
