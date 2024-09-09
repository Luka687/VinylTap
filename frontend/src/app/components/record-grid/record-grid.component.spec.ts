import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { RecordGridComponent } from './record-grid.component';

describe('RecordGridComponent', () => {
  let component: RecordGridComponent;
  let fixture: ComponentFixture<RecordGridComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [RecordGridComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(RecordGridComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
