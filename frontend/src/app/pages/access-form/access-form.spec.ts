import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccecssForm } from './accecss-form';

describe('AccecssForm', () => {
  let component: AccecssForm;
  let fixture: ComponentFixture<AccecssForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AccecssForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AccecssForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
