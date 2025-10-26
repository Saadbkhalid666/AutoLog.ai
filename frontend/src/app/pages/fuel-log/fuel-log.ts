import { Component, OnInit } from '@angular/core';
import { FuelLogService, FuelLog } from '../../services/fuel-log.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgxEchartsModule } from 'ngx-echarts';

@Component({
  selector: 'app-fuel-logs',
  standalone: true,
  imports: [CommonModule, FormsModule, NgxEchartsModule],
  templateUrl: './fuel-log.html',
  styleUrls: ['./fuel-log.css'],
})
export class FuelLogs implements OnInit {
  fuelLogs: FuelLog[] = [];
  manualLog: Partial<FuelLog> = { date: '', litres: 0, price: 0, odometer: 0 };
  editingLogId: number | null = null;
  editingModel: Partial<FuelLog> = {};
  chartOptions: any = {};
  loading = false;
  errorMsg = '';

  constructor(private fuelService: FuelLogService) {}

  ngOnInit() {
    this.loadFuelLogs();
  }

  loadFuelLogs() {
    this.loading = true;
    this.fuelService.getFuelLogs().subscribe({
      next: (res) => {
        this.fuelLogs = res.fuel_logs || [];
        this.buildChart();
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.errorMsg = 'Failed to load fuel logs';
        this.loading = false;
      }
    });
  }

  addManualLog() {
    this.loading= true
    const payload: Partial<FuelLog> = {
      date: this.manualLog.date || undefined,
      litres: Number(this.manualLog.litres || 0),
      price: Number(this.manualLog.price || 0),
      odometer: Number(this.manualLog.odometer || 0)
    };

    this.fuelService.addManualFuelLog(payload).subscribe({
      next: () => {
        this.manualLog = { date: '', litres: 0, price: 0, odometer: 0 };
        this.loadFuelLogs();
        this.loading = false
      },
      error: (err) => {
        console.error(err);
        this.errorMsg = err.error?.error || 'Failed to add fuel log';
      }
    });
  }

  startEdit(log: FuelLog) {
    this.editingLogId = log.id || null;
    this.editingModel = { ...log }; // shallow copy for editing
  }

  cancelEdit() {
    this.editingLogId = null;
    this.editingModel = {};
  }

 saveEdit() {
  if (!this.editingLogId) return;
  const id = this.editingLogId;
  const payload: Partial<FuelLog> = {
    litres: Number(this.editingModel.litres || 0),
    price: Number(this.editingModel.price || 0),
    odometer: Number(this.editingModel.odometer || 0)
  };

  this.fuelService.updateFuelLog(id, payload).subscribe({
    next: () => {
      const idx = this.fuelLogs.findIndex(l => l.id === id);
      if (idx !== -1) {
        this.fuelLogs[idx] = { ...this.fuelLogs[idx], ...payload } as FuelLog;
      }
      this.editingLogId = null;
      this.editingModel = {};
      this.buildChart();
    },
    error: (err) => {
      console.error(err);
      this.errorMsg = err.error?.error || 'Failed to update fuel log';
    }
  });
}


  deleteLog(id: number) {
    this.fuelService.deleteFuelLog(id).subscribe({
      next: () => {
        this.fuelLogs = this.fuelLogs.filter(l => l.id !== id);
        this.buildChart();
      },
      error: (err) => {
        console.error(err);
        this.errorMsg = err.error?.error || 'Failed to delete fuel log';
      }
    });
  }

  buildChart() {
    if (!this.fuelLogs || this.fuelLogs.length === 0) {
      this.chartOptions = {};
      return;
    }
    const sorted = this.fuelLogs.slice().sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    const labels = sorted.map(s => new Date(s.date).toLocaleDateString());
    const litresData = sorted.map(s => s.litres);
    const priceData = sorted.map(s => s.price);

    this.chartOptions = {
      tooltip: { trigger: 'axis' },
      legend: { data: ['Litres', 'Price'] },
      xAxis: { type: 'category', data: labels },
      yAxis: { type: 'value' },
      series: [
        { name: 'Litres', type: 'line', data: litresData, smooth: true },
        { name: 'Price', type: 'line', data: priceData, smooth: true }
      ]
    };
  }
}
