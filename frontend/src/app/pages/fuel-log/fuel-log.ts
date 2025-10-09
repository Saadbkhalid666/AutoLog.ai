import { Component, OnInit } from '@angular/core';
import { FuelLogService, FuelLog } from '../../services/fuel-log-service';
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
  manualLog: FuelLog = { date: '', litres: 0, price: 0, odometer: 0 };
  ocrFile!: File;
  chartOptions: any = {};

  constructor(private fuelService: FuelLogService) {}

  ngOnInit() {
    this.loadFuelLogs();
  }

  loadFuelLogs() {
    this.fuelService.getFuelLogs().subscribe((res) => {
      this.fuelLogs = res.fuel_logs || [];

      if (this.fuelLogs.length > 0) {
        const sortedLogs = this.fuelLogs
          .slice()
          .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

        const labels = sortedLogs.map((log) => new Date(log.date).toLocaleDateString());
        const litresData = sortedLogs.map((log) => log.litres);
        const priceData = sortedLogs.map((log) => log.price);

        this.chartOptions = {
          tooltip: { trigger: 'axis' },
          legend: { data: ['Litres', 'Price'] },
          xAxis: { type: 'category', data: labels },
          yAxis: { type: 'value' },
          series: [
            { name: 'Litres', type: 'line', data: litresData, smooth: true },
            { name: 'Price', type: 'line', data: priceData, smooth: true },
          ],
        };
      }
    });
  }
  addManualLog() {
    const logPayload = {
      ...this.manualLog,
      litres: Number(this.manualLog.litres),
      price: Number(this.manualLog.price),
      odometer: Number(this.manualLog.odometer),
    };

    this.fuelService.addManualFuelLog(logPayload).subscribe(() => {
      // Reset manualLog with proper number types
      this.manualLog = { date: '', litres: 0, price: 0, odometer: 0 };
      this.loadFuelLogs();
    });
  }

  onFileSelected(event: any) {
    this.ocrFile = event.target.files[0];
  }

  uploadOCR() {
    if (!this.ocrFile) return;
    this.fuelService.uploadOCRFuelLog(this.ocrFile).subscribe(() => {
      this.ocrFile = undefined as any;
      this.loadFuelLogs();
    });
  }

  deleteLog(id: number) {
    this.fuelService.deleteFuelLog(id).subscribe(() => this.loadFuelLogs());
  }

  updateLog(log: FuelLog) {
    this.fuelService.updateFuelLog(log.id!, log).subscribe(() => this.loadFuelLogs());
  }
}
