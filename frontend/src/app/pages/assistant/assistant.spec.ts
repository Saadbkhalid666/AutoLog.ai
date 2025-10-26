import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Assistant } from './assistant';

describe('Assistant', () => {
  let component: Assistant;
  let fixture: ComponentFixture<Assistant>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Assistant]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Assistant);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
