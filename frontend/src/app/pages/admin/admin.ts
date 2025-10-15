// src/app/components/admin-dashboard/admin-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AdminService, User, FuelLog, Reminder } from '../../services/admin.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-admin',
  imports:[CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './admin.html',
  styleUrls: ['./admin.css']
})
export class AdminComponent implements OnInit {
  users: User[] = [];
  logs: FuelLog[] = [];
  reminders: Reminder[] = [];

  editForm!: FormGroup; 
  editingType: 'user' | 'log' | 'reminder' | null = null;
  editingId: number | null = null;
  loading = false;
  error = '';

  constructor(private adminService: AdminService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.loadAllData();
  }

  loadAllData() {
    this.adminService.getAllUsers().subscribe({
      next: u => this.users = u,
      error: e => console.error(e)
    });
    this.adminService.getAllLogs().subscribe({
      next: l => this.logs = l,
      error: e => console.error(e)
    });
    this.adminService.getAllReminders().subscribe({
      next: r => this.reminders = r,
      error: e => console.error(e)
    });
  }

  startEdit(type: 'user' | 'log' | 'reminder', id: number, data: any) {
    this.editingType = type;
    this.editingId = id;
    // Build a simple form group from the data keys (safe)
    const controls: any = {};
    Object.keys(data).forEach(k => controls[k] = [data[k]]);
    this.editForm = this.fb.group(controls);
    // Scroll into view a bit
    setTimeout(() => document.getElementById('admin-edit-panel')?.scrollIntoView({ behavior: 'smooth' }), 100);
  }

  cancelEdit() {
    this.editingType = null;
    this.editingId = null;
    this.editForm.reset();
  }

  saveEdit() {
    if (!this.editingType || this.editingId === null) return;
    this.loading = true;
    let obs;
    if (this.editingType === 'user') obs = this.adminService.updateUser(this.editingId, this.editForm.value);
    else if (this.editingType === 'log') obs = this.adminService.updateLog(this.editingId, this.editForm.value);
    else obs = this.adminService.updateReminder(this.editingId, this.editForm.value);

    obs.subscribe({
      next: () => {
        this.loading = false;
        this.loadAllData();
        this.cancelEdit();
      },
      error: err => {
        this.loading = false;
        this.error = err?.error?.message || 'Update failed';
        console.error(err);
      }
    });
  }

  deleteItem(type: 'user' | 'log' | 'reminder', id: number) {
    if (!confirm('Are you sure? This action cannot be undone.')) return;
    let obs;
    if (type === 'user') obs = this.adminService.deleteUser(id);
    else if (type === 'log') obs = this.adminService.deleteLog(id);
    else obs = this.adminService.deleteReminder(id);

    obs.subscribe({
      next: () => this.loadAllData(),
      error: err => console.error(err)
    });
  }
}
