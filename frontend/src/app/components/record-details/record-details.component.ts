import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { RecordsService } from 'src/app/services/records.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-record-details',
  templateUrl: './record-details.component.html',
  styleUrls: ['./record-details.component.scss'],
  standalone: true,
  imports: [
    CommonModule
  ]
})
export class RecordDetailsComponent  implements OnInit {
  record$: Observable<any>;

  constructor(private route: ActivatedRoute, private recordsService: RecordsService) { 
    const id = +this.route.snapshot.paramMap.get('id')!; 
    this.record$ = this.recordsService.getRecordByID(id);
  }

  ngOnInit() {
    
  }

}
