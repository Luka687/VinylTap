import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { RecordsService } from 'src/app/services/records.service';
import { CommonModule } from '@angular/common';
import { IonGrid,IonCol,IonRow,IonContent} from '@ionic/angular/standalone';
import { IonIcon } from '@ionic/angular/standalone';
import { star, starHalf, starOutline } from 'ionicons/icons';
import { addIcons } from 'ionicons';

@Component({
  selector: 'app-record-details',
  templateUrl: './record-details.component.html',
  styleUrls: ['./record-details.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    IonGrid,IonCol,IonRow,IonContent,
    IonIcon
  ]
})
export class RecordDetailsComponent  implements OnInit {
  record$: Observable<any>;

  constructor(private route: ActivatedRoute, private recordsService: RecordsService) { 
    const id = +this.route.snapshot.paramMap.get('id')!; 
    this.record$ = this.recordsService.getRecordByID(id);
    addIcons({star, starHalf, starOutline})
  }

  ngOnInit() {
    
  }

  getFullStars(rating: number): number[] {
    return Array(Math.floor(rating)).fill(0);
  }

  getHalfStar(rating: number): boolean {
    return rating % 1 >= 0.5;
  }

  getEmptyStars(rating: number): number[] {
    return Array(5 - Math.ceil(rating));
  }

}
