import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HeroAboutCarComponent } from './hero-about-car-component';

describe('HeroAboutCarComponent', () => {
  let component: HeroAboutCarComponent;
  let fixture: ComponentFixture<HeroAboutCarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HeroAboutCarComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HeroAboutCarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
