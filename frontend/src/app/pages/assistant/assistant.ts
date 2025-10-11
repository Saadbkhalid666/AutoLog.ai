import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AiService } from '../../services/assistant.service';
interface Message {
  id?: string;
  role: 'user' | 'assistant' | 'system';
  text: string;
  ts: number;
}

@Component({
  selector: 'app-ai-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './assistant.html',
  styleUrls: ['./assistant.css'],
})
export class AiChatComponent {
  @ViewChild('inputBox') inputBox!: ElementRef<HTMLInputElement>;

  messages: Message[] = [];
  input = '';
  loading = false;
  error = '';

  private storageKey = 'autolog_ai_conversation';

  constructor(private ai: AiService) {
    this.loadFromStorage();
  }

    private cleanReply(reply: string): string {
  if (!reply) return reply;
  return reply
    .replace(/^\s*velix reporting[:\s\-\.\,]*/i, '')   
    .replace(/\s*velix reporting[:\s\-\.\,]*$/i, '')   
    .trim();
}

  send() {
    const prompt = this.input.trim();
    if (!prompt) return;

    const userMsg: Message = { role: 'user', text: prompt, ts: Date.now() };
    this.messages.push(userMsg);
    this.input = '';
    this.loading = true;
    this.error = '';
    this.saveToStorage();

    this.ai.chat({ message: prompt }).subscribe({
      next: (res) => {
        const cleaned = this.cleanReply(res.reply);
        const assistant: Message = { role: 'assistant', text: cleaned, ts: Date.now() };

        this.messages.push(assistant);
        this.loading = false;
        this.saveToStorage();
        setTimeout(() => this.scrollToBottom(), 50);
      },
      error: (err) => {
        console.error('AI chat failed:', err);
        this.error = 'Failed to contact AI. Try again.';
        this.loading = false;
      },
    });
  }

  clearConversation() {
    this.messages = [];
    localStorage.removeItem(this.storageKey);
  }

  private saveToStorage() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.messages));
    } catch (e) {
      // storage might fail in some environments — ignore gracefully
      console.warn('Could not save conversation locally', e);
    }
  }

  private loadFromStorage() {
    try {
      const raw = localStorage.getItem(this.storageKey);
      if (raw) {
        this.messages = JSON.parse(raw) as Message[];
      }
    } catch (e) {
      console.warn('Could not load saved conversation', e);
      this.messages = [];
    }
  }

  scrollToBottom() {
    const el = document.querySelector('.ai-messages') as HTMLElement | null;
    if (el) el.scrollTop = el.scrollHeight;
  }
}
