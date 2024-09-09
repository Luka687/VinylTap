import { Component, OnInit } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonMenu, IonMenuButton, IonButtons, IonApp} from '@ionic/angular/standalone';
import { RouterModule, RouterOutlet } from '@angular/router';
import { routes } from './app.routes';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  standalone: true,
  imports: [
    IonHeader,IonTitle,IonToolbar,IonContent, 
    IonMenu, IonMenuButton, IonButtons, IonApp,
    RouterModule, RouterOutlet
  ],
})
export class AppComponent implements OnInit{

  constructor() { }

  ngOnInit(){
  }
}
