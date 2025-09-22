import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CarModel } from './car-model';

describe('CarModel', () => {
  let component: CarModel;
  let fixture: ComponentFixture<CarModel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CarModel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CarModel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
