import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { AdminService, User, FuelLog, Reminder } from '../../services/admin.service';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.html',
  styleUrls: ['./admin.css']
})
export class AdminDashboardComponent implements OnInit {
  users: User[] = [];
  logs: FuelLog[] = [];
  reminders: Reminder[] = [];

  editForm: FormGroup;
  editingType: 'user' | 'log' | 'reminder' | null = null;
  editingId: number | null = null;

  constructor(private adminService: AdminService, private fb: FormBuilder) {
    this.editForm = this.fb.group({});
  }

  ngOnInit(): void {
    this.loadAllData();
  }

  loadAllData() {
    this.adminService.getAllUsers().subscribe(users => this.users = users);
    this.adminService.getAllLogs().subscribe(logs => this.logs = logs);
    this.adminService.getAllReminders().subscribe(reminders => this.reminders = reminders);
  }

  startEdit(type: 'user' | 'log' | 'reminder', id: number, data: any) {
    this.editingType = type;
    this.editingId = id;
    this.editForm = this.fb.group({...data}); // prefill form
  }

  cancelEdit() {
    this.editingType = null;
    this.editingId = null;
  }

  saveEdit() {
    if (!this.editingType || this.editingId === null) return;

    const obs = this.editingType === 'user'
      ? this.adminService.updateUser(this.editingId, this.editForm.value)
      : this.editingType === 'log'
      ? this.adminService.updateLog(this.editingId, this.editForm.value)
      : this.adminService.updateReminder(this.editingId, this.editForm.value);

    obs.subscribe({
      next: () => {
        this.loadAllData();
        this.cancelEdit();
      },
      error: err => console.error(err)
    });
  }

  deleteItem(type: 'user' | 'log' | 'reminder', id: number) {
    const obs = type === 'user'
      ? this.adminService.deleteUser(id)
      : type === 'log'
      ? this.adminService.deleteLog(id)
      : this.adminService.deleteReminder(id);

    obs.subscribe({
      next: () => this.loadAllData(),
      error: err => console.error(err)
    });
  }
}
