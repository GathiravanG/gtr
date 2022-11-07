import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadNowComponent } from './upload-now.component';

describe('UploadNowComponent', () => {
  let component: UploadNowComponent;
  let fixture: ComponentFixture<UploadNowComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UploadNowComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadNowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
