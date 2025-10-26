import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FuelLog } from './fuel-log';

describe('FuelLog', () => {
  let component: FuelLog;
  let fixture: ComponentFixture<FuelLog>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FuelLog]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FuelLog);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
