import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import{  IonGrid,IonCol,IonRow, 
  IonMenu, IonMenuButton, IonButtons, IonLabel, IonIcon, IonItem, IonList} from '@ionic/angular/standalone';
import { Observable, of } from 'rxjs';
import { RecordsService } from 'src/app/services/records.service';
import { RecordCardComponent } from '../record-card/record-card.component';


@Component({
  selector: 'app-record-grid',
  templateUrl: './record-grid.component.html',
  styleUrls: ['./record-grid.component.scss'],
  standalone: true,
  imports: [
    IonGrid,IonCol,IonRow, 
    IonMenu, IonMenuButton, IonButtons, IonLabel, IonIcon,
    IonItem, IonList,
    RecordCardComponent, CommonModule
  ]
})
export class RecordGridComponent  implements OnInit {

  records$: Observable<any[]>;

  constructor(private recordService: RecordsService){
    this.records$ = this.recordService.getRecords();
  }

  ngOnInit() {}

}
