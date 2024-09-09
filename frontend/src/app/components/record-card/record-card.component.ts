import { Component, OnInit, Input } from '@angular/core';
import { IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle, IonList, IonItem, IonLabel } from '@ionic/angular/standalone';
import { Router } from '@angular/router';

@Component({
  selector: 'app-record-card',
  templateUrl: './record-card.component.html',
  styleUrls: ['./record-card.component.scss'],
  standalone: true,
  imports: [
    IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle, IonCardHeader, IonList, IonItem, IonLabel
  ]
})
export class RecordCardComponent implements OnInit{

  @Input() id! : number;
  @Input() title: string = 'Album Title';
  @Input() img_link: string = '';
  @Input() subtitle: string = 'Artist Name';
  content: string = 'Description';

  constructor(private router: Router) {}

  navigateToRecordDetails() {
    if (this.id !== undefined) {
      this.router.navigate(['/record', this.id]);
    }
  }

  ngOnInit(){
    if (this.img_link == null){
      this.img_link = 'https://ionicframework.com/docs/img/demos/card-media.png';
    }
    console.log(this.img_link)   
  }
}
