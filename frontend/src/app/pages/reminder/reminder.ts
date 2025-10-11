import { Component, OnInit } from '@angular/core';
import { ServiceReminder, ServiceReminderService } from '../../services/service-reminder.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-reminder',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reminder.html',
  styleUrls: ['./reminder.css']
})
export class Reminder implements OnInit {
  
  reminders: ServiceReminder[] = [];
  newReminder: ServiceReminder = { service_type: '', due_date: '', note: '' };
  editingReminder: ServiceReminder | null = null;
  loading = false;
  errorMsg = '';

  constructor(private reminderService: ServiceReminderService) {}

  ngOnInit() {
    this.getReminders();
  }

  getReminders() {
    this.loading = true;
    this.reminderService.getReminders().subscribe({
      next: (data) => {
        this.reminders = data;
        this.loading = false;
      },
      error: () => {
        this.errorMsg = 'Failed to fetch reminders';
        this.loading = false;
      }
    });
  }

  addReminder() {
    if (!this.newReminder.service_type || !this.newReminder.due_date || !this.newReminder.note) {
      this.errorMsg = 'Please fill in all fields.';
      return;
    }

    this.reminderService.addReminder(this.newReminder).subscribe({
      next: () => {
        this.newReminder = { service_type: '', due_date: '', note: '' };
        this.getReminders();
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to add reminder';
      }
    });
  }

  editReminder(reminder: ServiceReminder) {
    this.editingReminder = { ...reminder };
  }

  updateReminder() {
    if (!this.editingReminder) return;
    this.reminderService.updateReminder(this.editingReminder.id!, this.editingReminder).subscribe({
      next: () => {
        this.editingReminder = null;
        this.getReminders();
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to update reminder';
      }
    });
  }

  deleteReminder(id: number) {
  this.reminderService.deleteReminder(id).subscribe({
    next: () => this.getReminders(),
    error: (err) => this.errorMsg = err.error?.error || 'Failed to delete reminder'
  });
}


  cancelEdit() {
    this.editingReminder = null;
  }
}
