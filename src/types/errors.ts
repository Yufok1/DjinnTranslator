export class RecursionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RecursionError';
  }
}

export class CodexViolationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'CodexViolationError';
  }
}

export class StabilityError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'StabilityError';
  }
} 