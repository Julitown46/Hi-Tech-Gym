import { TestBed } from '@angular/core/testing';

import { MembresiaService } from './membresia.service';

describe('MembresiaService', () => {
  let service: MembresiaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MembresiaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
