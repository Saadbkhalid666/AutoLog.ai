// src/app/components/contact/contact.component.ts
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ContactService, ContactPayload } from '../../services/contact.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-contact',
  imports: [
    CommonModule,
    ReactiveFormsModule, // ✅ Replace FormsModule with this
  ],
  templateUrl: './contact.html',
  styleUrl: './contact.css',
})
export class ContactComponent implements OnInit {
  contactForm!: FormGroup;
  loading = false;
  successMsg = '';
  errorMsg = '';

  constructor(private fb: FormBuilder, private contactService: ContactService) {}

  ngOnInit(): void {
    this.contactForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      message: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  get f() {
    return this.contactForm.controls;
  }

  onSubmit(): void {
    this.successMsg = '';
    this.errorMsg = '';

    if (this.contactForm.invalid) {
      this.contactForm.markAllAsTouched();
      return;
    }

    this.loading = true;
    const payload: ContactPayload = {
      name: this.f['name'].value,
      email: this.f['email'].value,
      message: this.f['message'].value,
    };

    this.contactService.submitContact(payload).subscribe({
      next: (res) => {
        this.loading = false;
        this.successMsg = res?.message || 'Message sent — shukriya, Jani! 🌿';
        this.contactForm.reset();
      },
      error: (err) => {
        this.loading = false;
        this.errorMsg = err?.error?.message || 'Failed to send message. Try again later.';
      },
    });
  }
}
