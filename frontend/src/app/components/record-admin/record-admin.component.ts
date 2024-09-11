import { Component, OnInit } from '@angular/core';
import { Observable, of, map } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { RecordsService } from 'src/app/services/records.service';
import { CommonModule } from '@angular/common';
import { star, starHalf, starOutline } from 'ionicons/icons';
import { addIcons } from 'ionicons';
import { FormsModule } from '@angular/forms';
import { AuthService } from 'src/app/services/auth.service';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-record-admin',
  templateUrl: './record-admin.component.html',
  styleUrls: ['./record-admin.component.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule, IonicModule,
  ]
})
export class RecordAdminComponent  implements OnInit {
  record$: Observable<any>;
  addMode: boolean;
  name: string= '';
  year: number = 0;
  genre: string = '';
  artist: string = '';
  img_link:string = '';
  id:number = 0;

  constructor(private route: ActivatedRoute, private recordsService: RecordsService, private authService :AuthService, private router: Router ) {
    const id = +this.route.snapshot.paramMap.get('record_id')!;
    if (id == 0){
      this.addMode = true;
      this.record$ = of();
    }
    else{
      this.addMode = false;
      this.id = id;
      this.record$ = this.recordsService.getRecordByID(id);
      this.record$.subscribe(
        (response) => {
          this.name = response.name;
          this.year = response.year_of_release;
          this.genre = response.genre;
          this.artist = response.artist;
          this.img_link = response.img_link;
        }
        )
    }
   }

  ngOnInit() {}

  onSubmit(){
    if (this.addMode){
      this.recordsService.createRecord(this.name, this.year, this.genre,this.artist,this.img_link);
    }
    else{
      this.recordsService.updateRecord(this.id,this.name, this.year, this.genre,this.artist,this.img_link);
    }
  }

  async deleteRecord(){
    if (this.id!=0){
      this.recordsService.deleteRecord(this.id);
      await this.router.navigate(['/']);
      window.location.reload();
    }   
  }

}
