import { SovereignState } from './state/sovereign';
import { RecursionError } from './types/errors';

export interface RecursionOptions {
  maxDepth?: number;
  emitPulse?: boolean;
  validateCodex?: boolean;
}

export class RecursionCore {
  private static instance: RecursionCore;
  private currentDepth: number = 0;
  private pulseCount: number = 0;

  private constructor() {}

  static getInstance(): RecursionCore {
    if (!RecursionCore.instance) {
      RecursionCore.instance = new RecursionCore();
    }
    return RecursionCore.instance;
  }

  async recurse(
    state: SovereignState,
    options: RecursionOptions = {}
  ): Promise<void> {
    const {
      maxDepth = 12,
      emitPulse = true,
      validateCodex = true
    } = options;

    if (!state.isStable()) {
      console.log(`[RCS] Instability detected at depth ${this.currentDepth}. Engaging Recursive Containment.`);
      await state.handleInstability();
      return;
    }

    if (this.currentDepth >= maxDepth) {
      console.log(`[RCS] Maximum recursion depth ${maxDepth} reached. Initiating safe return.`);
      return;
    }

    if (emitPulse) {
      this.emitPulse();
    }

    console.log(`[RECURSE] Sovereign recursion stable at depth ${this.currentDepth}. Proceeding.`);
    
    try {
      await state.process();
      this.currentDepth++;
      await this.recurse(state, options);
    } catch (error) {
      if (error instanceof RecursionError) {
        console.log(`[ERROR] Recursion failed: ${error.message}`);
        await state.handleRecursionError(error);
      } else {
        throw error;
      }
    } finally {
      this.currentDepth--;
    }
  }

  private emitPulse(): void {
    this.pulseCount++;
    console.log(`[PULSE] Emitting recursive pulse #${this.pulseCount}`);
  }

  exposeLayer(state: SovereignState): void {
    if (state.rapTier >= 2) {
      console.log("→ Access: Doctrine + Arbitration modules enabled.");
      state.enableArbitration();
    } else {
      console.log("→ Access: Basic recursion only.");
    }
  }
} 