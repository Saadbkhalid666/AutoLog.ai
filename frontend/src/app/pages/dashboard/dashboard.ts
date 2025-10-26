// src/app/components/admin-dashboard/admin-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AdminService, User, FuelLog, Reminder } from '../../services/dashboard.service';
import { CommonModule } from '@angular/common';
import { NgxEchartsModule } from 'ngx-echarts';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, NgxEchartsModule],
  templateUrl: './admin.html',
  styleUrls: ['./admin.css'],
})
export class Dashboard implements OnInit {
  users: User[] = [];
  logs: FuelLog[] = [];
  reminders: Reminder[] = [];

  editForm!: FormGroup;
  editingType: 'user' | 'log' | 'reminder' | null = null;
  editingId: number | null = null;
  loading = false;
  error = '';

  // Chart options
  usersChartOptions: any = {};
  logsChartOptions: any = {};
  remindersChartOptions: any = {};

  // chart window (days)
  daysWindow = 14;

  constructor(private adminService: AdminService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.loadAllData();
  }

  loadAllData() {
    this.adminService.getAllUsers().subscribe({
      next: (u) => {
        this.users = Array.isArray(u) ? u : (u as any).users || [];
        this.buildUsersChart();
      },
      error: (e) => console.error(e),
    });

    this.adminService.getAllLogs().subscribe({
      next: (l) => {
        this.logs = Array.isArray(l) ? l : (l as any).fuel_logs || [];
        this.buildLogsChart();
      },
      error: (e) => console.error(e),
    });

    this.adminService.getAllReminders().subscribe({
      next: (r) => {
        this.reminders = Array.isArray(r) ? r : (r as any).reminders || [];
        this.buildRemindersChart();
      },
      error: (e) => console.error(e),
    });
  }

  // ---- Editing helpers ----
  startEdit(type: 'user' | 'log' | 'reminder', id: number, data: any) {
    this.editingType = type;
    this.editingId = id;
    const controls: any = {};
    Object.keys(data).forEach((k) => (controls[k] = [data[k]]));
    this.editForm = this.fb.group(controls);
    setTimeout(
      () => document.getElementById('admin-edit-panel')?.scrollIntoView({ behavior: 'smooth' }),
      100
    );
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
    if (this.editingType === 'user')
      obs = this.adminService.updateUser(this.editingId, this.editForm.value);
    else if (this.editingType === 'log')
      obs = this.adminService.updateLog(this.editingId, this.editForm.value);
    else obs = this.adminService.updateReminder(this.editingId, this.editForm.value);

    obs.subscribe({
      next: () => {
        this.loading = false;
        this.loadAllData();
        this.cancelEdit();
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.message || 'Update failed';
        console.error(err);
      },
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
      error: (err) => console.error(err),
    });
  }

  // ---- Chart helpers ----
  private getDateKey(d: Date) {
    const y = d.getFullYear();
    const m = `${d.getMonth() + 1}`.padStart(2, '0');
    const day = `${d.getDate()}`.padStart(2, '0');
    return `${y}-${m}-${day}`; // YYYY-MM-DD
  }

  private makeWindowLabels(days = this.daysWindow) {
    const arr: string[] = [];
    for (let i = days - 1; i >= 0; i--) {
      const dt = new Date();
      dt.setDate(dt.getDate() - i);
      arr.push(this.getDateKey(dt));
    }
    return arr;
  }

  private buildSeriesCountsByDay(items: any[], dateField: string, days = this.daysWindow) {
    // produce map dateKey -> count for last N days
    const labels = this.makeWindowLabels(days);
    const countsMap: Record<string, number> = {};
    labels.forEach((l) => (countsMap[l] = 0));

    items.forEach((it) => {
      let raw = it[dateField];
      if (!raw) return;
      // support Date object or ISO string
      const dt = raw instanceof Date ? raw : new Date(raw);
      if (isNaN(dt.getTime())) return;
      const key = this.getDateKey(dt);
      if (key in countsMap) countsMap[key] += 1;
    });

    return {
      labels,
      data: labels.map((l) => countsMap[l] || 0),
    };
  }

  private buildUsersChart() {
    const roles = this.users.reduce((acc: Record<string, number>, u) => {
      acc[u.role] = (acc[u.role] || 0) + 1;
      return acc;
    }, {});

    this.usersChartOptions = {
      title: { text: 'User Distribution by Role', left: 'center', textStyle: { color: '#42f5d8' } },
      tooltip: { trigger: 'item' },
      legend: { bottom: 0, textStyle: { color: '#cfeee6' } },
      series: [
        {
          name: 'Users',
          type: 'pie',
          radius: '60%',
          data: Object.keys(roles).map((role) => ({ name: role, value: roles[role] })),
        },
      ],
      textStyle: { color: '#cfeee6' },
    };
  }

  private buildLogsChart() {
    // FuelLog date field is usually 'date'
    const processed = this.buildSeriesCountsByDay(this.logs, 'date');

    this.logsChartOptions = {
      title: { text: 'Fuel Logs (daily)', left: 'center', textStyle: { color: '#42f5d8' } },
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: processed.labels,
        axisLabel: { rotate: 30, color: '#cfeee6' },
      },
      yAxis: { type: 'value', axisLabel: { color: '#cfeee6' } },
      grid: { left: 10, right: 10, bottom: 60 },
      series: [
        {
          name: 'Logs',
          type: 'line',
          data: processed.data,
          smooth: true,
          lineStyle: { width: 2 },
          areaStyle: {},
        },
      ],
      textStyle: { color: '#cfeee6' },
    };
  }

  private buildRemindersChart() {
    // Reminders due_date or dueAt
    const remindersNormalized = this.reminders
      .map((r) => {
        return { date: r.due_date };
      })
      .map((x) => ({ date: x.date }));

    const processed = this.buildSeriesCountsByDay(
      remindersNormalized.map((x) => ({ date: x.date })),
      'date'
    );

    this.remindersChartOptions = {
      title: {
        text: 'Service Reminders (due daily)',
        left: 'center',
        textStyle: { color: '#42f5d8' },
      },
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: processed.labels,
        axisLabel: { rotate: 30, color: '#cfeee6' },
      },
      yAxis: { type: 'value', axisLabel: { color: '#cfeee6' } },
      grid: { left: 10, right: 10, bottom: 60 },
      series: [
        {
          name: 'Reminders',
          type: 'line',
          data: processed.data,
          smooth: true,
          lineStyle: { width: 2 },
          areaStyle: {},
        },
      ],
      textStyle: { color: '#cfeee6' },
    };
  }
}
