import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxEchartsModule } from 'ngx-echarts';
import { OcrFuelService } from '../../services/ocr.service';

interface FuelLog {
  id?: number;
  user_id?: number;
  date: string;
  litres: number;
  price: number;
  odometer: number;
}

@Component({
  selector: 'app-ocr',
  standalone: true,
  imports: [CommonModule, NgxEchartsModule],
  templateUrl: './ocr.html',
  styleUrls: ['./ocr.css']
})
export class OcrComponent {
  @ViewChild('fileInput') fileInputRef!: ElementRef<HTMLInputElement>;

  selectedFile: File | null = null;
  previewUrl: string | null = null;
  extractedText: string | null = null;
  lastOcrLog: FuelLog | null = null;
  fuelLogs: FuelLog[] = [];
  isUploading = false;
  chartOptions: any = {};

  constructor(private fuelService: OcrFuelService) {}

  ngOnInit() {
    this.fetchLogs();
  }

  openFilePicker() {
    this.fileInputRef.nativeElement.click();
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.[0]) {
      this.selectedFile = input.files[0];
      this.previewUrl = URL.createObjectURL(this.selectedFile);
    }
  }

  uploadImage() {
    if (!this.selectedFile) return;
    this.isUploading = true;

    this.fuelService.uploadOcr(this.selectedFile).subscribe({
      next: (res) => {
        this.isUploading = false;
        this.extractedText = res.extracted_text;

        if (res.fuel_log) {
          const log: FuelLog = {
            date: new Date(res.fuel_log.date).toISOString(),
            litres: Number(res.fuel_log.litres),
            price: Number(res.fuel_log.price),
            odometer: Number(res.fuel_log.odometer)
          };
          this.lastOcrLog = log;
          this.fuelLogs = [...this.fuelLogs, log];
          this.buildChart();
        }

        this.fileInputRef.nativeElement.value = '';
        this.selectedFile = null;
        this.previewUrl = null;
      },
      error: (err) => {
        this.isUploading = false;
        console.error('Upload failed', err);
        this.extractedText = 'Extraction failed. Try cropping or improving lighting.';
      }
    });
  }

  fetchLogs() {
    this.fuelService.getFuelLogs().subscribe({
      next: (res) => {
        this.fuelLogs = res.fuel_logs.map((l: any) => ({
          ...l, date: new Date(l.date).toISOString()
        }));
        this.buildChart();
      },
      error: (err) => console.error('Failed fetching logs', err)
    });
  }

  buildChart() {
    if (!this.fuelLogs.length) {
      this.chartOptions = {};
      return;
    }

    const sorted = [...this.fuelLogs].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    const labels = sorted.map(l => new Date(l.date).toLocaleDateString());
    const litresData = sorted.map(l => l.litres);
    const priceData = sorted.map(l => l.price);

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
