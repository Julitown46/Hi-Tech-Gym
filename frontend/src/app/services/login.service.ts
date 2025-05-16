import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private readonly STORAGE_KEY = 'isLoggedIn';
  private loggedInSubject = new BehaviorSubject<boolean>(this.getStoredStatus());

  loggedIn$ = this.loggedInSubject.asObservable();

  private isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }

  private getStoredStatus(): boolean {
    if (this.isBrowser()) {
      return localStorage.getItem(this.STORAGE_KEY) === 'true';
    }
    return false; 
  }

  login() {
    if (this.isBrowser()) {
      localStorage.setItem(this.STORAGE_KEY, 'true');
      this.loggedInSubject.next(true);
    }
  }

  logout() {
    localStorage.removeItem(this.STORAGE_KEY);
    this.loggedInSubject.next(false);
  }

    isLoggedIn(): boolean {
    return this.loggedInSubject.value;
  }

    syncLoginStatus() {
    this.loggedInSubject.next(this.getStoredStatus());
  }
}
