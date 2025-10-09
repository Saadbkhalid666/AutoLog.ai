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
  styleUrls: ['./fuel-log.css']
})
export class FuelLogs implements OnInit {

  fuelLogs: FuelLog[] = [];
  manualLog: FuelLog = { date: '', litres: '', price: '', odometer: '' };
  ocrFile!: File;
  chartOptions: any = {};
  loading = false;

  constructor(private fuelService: FuelLogService) {}

  ngOnInit() {
    this.loadFuelLogs();
  }

  loadFuelLogs() {
    this.fuelService.getFuelLogs().subscribe(res => {
      this.fuelLogs = res.fuel_logs || [];

      if (this.fuelLogs.length > 0) {
        const sortedLogs = [...this.fuelLogs].sort(
          (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
        );

        const labels = sortedLogs.map(log => new Date(log.date).toLocaleDateString());
        const litresData = sortedLogs.map(log => Number(log.litres));
        const priceData = sortedLogs.map(log => Number(log.price));

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
    });
  }

  addManualLog() {
    if (!this.manualLog.litres || !this.manualLog.price || !this.manualLog.odometer) return;

    this.loading = true;
    this.fuelService.addManualFuelLog(this.manualLog).subscribe(() => {
      this.manualLog = { date: '', litres: '', price: '', odometer: '' };
      this.loadFuelLogs();
      this.loading = false;
    });
  }

  onFileSelected(event: any) {
    this.ocrFile = event.target.files[0];
  }

  uploadOCR() {
    if (!this.ocrFile) return;
    this.loading = true;
    this.fuelService.uploadOCRFuelLog(this.ocrFile).subscribe(() => {
      this.ocrFile = undefined as any;
      this.loadFuelLogs();
      this.loading = false;
    });
  }

  deleteLog(id: number) {
    this.fuelService.deleteFuelLog(id).subscribe(() => this.loadFuelLogs());
  }
}
