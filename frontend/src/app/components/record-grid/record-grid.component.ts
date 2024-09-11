import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import{  IonGrid,IonCol,IonRow, 
  IonMenu, IonMenuButton, IonButtons, IonLabel, IonIcon, IonItem, IonList} from '@ionic/angular/standalone';
import { Observable, of,map } from 'rxjs';
import { RecordsService } from 'src/app/services/records.service';
import { RecordCardComponent } from '../record-card/record-card.component';
import { ActivatedRoute } from '@angular/router';


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

  records$: Observable<any[]> = of([]);
  @Input() name: string = '';

  constructor(private recordService: RecordsService, private route: ActivatedRoute){}

  ngOnInit() {
    this.route.queryParamMap.subscribe(params => {
      const nameParam = params.get('name');
      if (nameParam === null || nameParam.trim() === '') {
        this.name = '';
      } else {
        this.name = nameParam;
      }
      this.records$ = this.getRecordsByName(this.name);
    });
  }

  getRecordsByName(name:string): Observable<any[]>{
    return this.recordService.getRecords().pipe(
      map(records => records.filter(record => record.name.toLowerCase().includes(name.toLowerCase())))
    )
  }

}
