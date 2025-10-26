import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Ocr } from './ocr';

describe('Ocr', () => {
  let component: Ocr;
  let fixture: ComponentFixture<Ocr>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Ocr]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Ocr);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
