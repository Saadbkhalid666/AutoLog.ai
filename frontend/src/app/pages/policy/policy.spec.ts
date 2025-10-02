import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Policy } from './policy';

describe('Policy', () => {
  let component: Policy;
  let fixture: ComponentFixture<Policy>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Policy]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Policy);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
