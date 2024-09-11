import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { RecordsService } from 'src/app/services/records.service';
import { CommonModule } from '@angular/common';
import { IonGrid,IonCol,IonRow,IonContent} from '@ionic/angular/standalone';
import { IonIcon } from '@ionic/angular/standalone';
import { star, starHalf, starOutline } from 'ionicons/icons';
import { addIcons } from 'ionicons';
import { RatingsService } from 'src/app/services/ratings.service';
import { IonButton } from '@ionic/angular/standalone';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-record-user',
  templateUrl: './record-user.component.html',
  styleUrls: ['./record-user.component.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule,
    IonGrid,IonCol,IonRow,IonContent,
    IonIcon, IonButton
  ]
})
export class RecordUserComponent  implements OnInit {
  record$: Observable<any>;
  record_id: number = 0;
  user_id: number = 0;
  rating: number = 0;
  ratingOptions: number[] = [1, 2, 3, 4, 5];
  is_rated : boolean = false;

  constructor(private route: ActivatedRoute, private recordsService: RecordsService, private ratingsService: RatingsService) { 
    this.record_id = +this.route.snapshot.paramMap.get('record_id')!; 
    this.user_id = +this.route.snapshot.paramMap.get('user_id')!; 
    this.record$ = this.recordsService.getRecordByID(this.record_id);
    addIcons({star, starHalf, starOutline})
  }

  ngOnInit() {
    this.isRated();
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

  isRated(){
    this.ratingsService.getRatingExists(this.user_id, this.record_id).subscribe(exists => {
      if (exists) {
        this.is_rated = true;
      } else {
        this.is_rated = false;
      }
    });
  }

  rate(){
    if(this.rating!=0){
      if(this.is_rated){
        this.ratingsService.editRating(this.user_id, this.record_id, this.rating);
        this.isRated();
      }
      else{
        this.ratingsService.createRating(this.user_id, this.record_id, this.rating );
        this.isRated();
      }
    }   
  }
}
