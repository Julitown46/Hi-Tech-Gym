import { TestBed } from '@angular/core/testing';

import { PistaService } from './pista.service';

describe('PistaService', () => {
  let service: PistaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PistaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
