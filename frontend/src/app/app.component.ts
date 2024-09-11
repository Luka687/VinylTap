import { Component, OnInit, ViewChild } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent, 
  IonMenu, IonMenuButton, IonButtons, IonButton, IonApp, IonLabel, IonList, IonItem, IonIcon, IonModal, IonSearchbar, IonToast } from '@ionic/angular/standalone';
import { RouterModule, RouterOutlet, Router } from '@angular/router';
import { routes } from './app.routes';
import { MenuController } from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { addCircle, home, personCircle, search, } from 'ionicons/icons';
import { AuthService } from './services/auth.service';
import { CommonModule } from '@angular/common';
import { ToastController } from '@ionic/angular';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  standalone: true,
  imports: [
    IonHeader,IonTitle,IonToolbar,IonContent, 
    IonMenu, IonMenuButton, IonButtons, IonApp,
    RouterModule, RouterOutlet,
    IonLabel, IonList, IonIcon, IonItem, IonButton, IonModal, IonSearchbar, IonToast,
    CommonModule
  ],
})
export class AppComponent implements OnInit{
  @ViewChild(IonModal) modal!: IonModal;
  @ViewChild (IonSearchbar) searchbar!: IonSearchbar;

  name:string = '';

  constructor(private router: Router, 
    private menuController: MenuController, 
    public authService: AuthService,
    private toastController: ToastController) { 
    addIcons({home, search, personCircle, addCircle})
  }

  ngOnInit(){
    console.log(localStorage.getItem('userIsAdmin'))
    console.log(localStorage.getItem('token'))
    console.log(localStorage.getItem('user_id'))
  }

  async navigateToLogIn(){
    // Navigate to the home route
    //await this.router.navigate(['/']);
    await this.router.navigate(['/login']);
    // Close the side menu
    await this.menuController.close();
  }

  async navigateAdd(){
    await this.router.navigate(['/admin/0']);
    await this.menuController.close();
  }

  openModal() {
    this.modal.present();
  }

  closeModal() {
    this.modal.dismiss();
  }

  async navigateHome() {
    // Navigate to the home route
    //await this.router.navigate(['/']);
    await this.router.navigate(['/']);
    // Close the side menu
    await this.menuController.close();
  }

  async navigateToSearch() {
    if(this.searchbar.value){
      this.name = this.searchbar.value;
    }
    await this.router.navigate(['/records/search'], {
      queryParams: {name: this.name}
    });
    // Close the side menu
    await this.menuController.close();
    this.closeModal();
  }

  async logOut(){
    // Navigate to the home route
    //await this.router.navigate(['/']);
    this.authService.logout();
    // Close the side menu
    await this.menuController.close();
    const toast = await this.toastController.create({
      message: 'The user has signed out',
      duration: 5000
    });
    toast.present();
  }
}
