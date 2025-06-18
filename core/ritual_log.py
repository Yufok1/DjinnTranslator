# Copyright 2024 SpliceWeb
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Ritual Log Module
Handles tracking and cross-referencing of ritual activations
"""

import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from .ritual_phrases import RitualPhraseSystem, RitualPhrase
from .chord_preservation import ChordPreservation
from .ml.predictor import MLPredictor

@dataclass
class RitualLedgerEntry:
    """Entry in the ritual phrase ledger"""
    phrase: str
    bound_action: str
    bound_id: str
    speaker_sigil: str
    harmonic_signature: str  # Hash of vocal profile
    breath_phase: Optional[float]
    timestamp: float = time.time()
    status: str = "pending"  # "pending", "confirmed", "rejected"
    mirror_feedback: Optional[str] = None

@dataclass
class InvocationRecord:
    """Record of a ritual invocation attempt"""
    timestamp: float
    voiceprint_hash: str
    phrase: str
    result: str  # "success", "fail", "near-miss"
    mirror_echo: Optional[str]
    resonance_level: float
    echo_depth: float
    linked_events: List[Dict[str, Any]]  # List of linked events (chords, insights, etc.)

class RitualLog:
    """Main ritual log class"""
    
    def __init__(self):
        self.ritual_system = RitualPhraseSystem()
        self.chord_preservation = ChordPreservation()
        self.ml_predictor = MLPredictor()
        
        # Initialize storage
        self.ledger: Dict[str, RitualLedgerEntry] = {}
        self.invocation_history: List[InvocationRecord] = []
        self.cross_references: Dict[str, List[str]] = {
            "chords": [],
            "insights": [],
            "transitions": [],
            "djinn": [],
            "crypto": []
        }
        
        # Load existing data
        self._load_ritual_log()
    
    def register_ritual(
        self,
        phrase: str,
        bound_action: str,
        bound_id: str,
        speaker_sigil: str,
        harmonic_signature: str,
        breath_phase: Optional[float] = None
    ) -> str:
        """Register a new ritual in the ledger"""
        # Create ledger entry
        entry = RitualLedgerEntry(
            phrase=phrase,
            bound_action=bound_action,
            bound_id=bound_id,
            speaker_sigil=speaker_sigil,
            harmonic_signature=harmonic_signature,
            breath_phase=breath_phase
        )
        
        # Generate unique ID
        ritual_id = f"{speaker_sigil}_{int(time.time())}"
        
        # Store in ledger
        self.ledger[ritual_id] = entry
        
        # Update cross-references
        self._update_cross_references(ritual_id, entry)
        
        # Save to storage
        self._save_ritual_log()
        
        return ritual_id
    
    def log_invocation(
        self,
        voiceprint_hash: str,
        phrase: str,
        result: str,
        mirror_echo: Optional[str],
        resonance_level: float,
        echo_depth: float,
        linked_events: List[Dict[str, Any]]
    ):
        """Log a ritual invocation attempt"""
        # Create invocation record
        record = InvocationRecord(
            timestamp=time.time(),
            voiceprint_hash=voiceprint_hash,
            phrase=phrase,
            result=result,
            mirror_echo=mirror_echo,
            resonance_level=resonance_level,
            echo_depth=echo_depth,
            linked_events=linked_events
        )
        
        # Add to history
        self.invocation_history.append(record)
        
        # Update statistics
        self._update_invocation_stats(record)
        
        # Save to storage
        self._save_ritual_log()
    
    def find_rituals_by_sigil(self, sigil: str) -> List[str]:
        """Find rituals by speaker sigil"""
        return [
            ritual_id
            for ritual_id, entry in self.ledger.items()
            if entry.speaker_sigil == sigil
        ]
    
    def find_rituals_by_action(self, action: str) -> List[str]:
        """Find rituals by bound action"""
        return [
            ritual_id
            for ritual_id, entry in self.ledger.items()
            if entry.bound_action == action
        ]
    
    def find_rituals_by_phrase(self, phrase: str) -> List[str]:
        """Find rituals by phrase text"""
        return [
            ritual_id
            for ritual_id, entry in self.ledger.items()
            if phrase.lower() in entry.phrase.lower()
        ]
    
    def find_rituals_by_resonance(self, resonance_level: float) -> List[str]:
        """Find rituals by resonance level"""
        # Get invocation records for each ritual
        ritual_stats = {}
        for record in self.invocation_history:
            if record.phrase not in ritual_stats:
                ritual_stats[record.phrase] = []
            ritual_stats[record.phrase].append(record.resonance_level)
        
        # Find rituals with matching average resonance
        matching_rituals = []
        for phrase, levels in ritual_stats.items():
            avg_resonance = np.mean(levels)
            if abs(avg_resonance - resonance_level) < 0.1:
                matching_rituals.extend(
                    ritual_id
                    for ritual_id, entry in self.ledger.items()
                    if entry.phrase == phrase
                )
        
        return matching_rituals
    
    def get_invocation_stats(self, ritual_id: Optional[str] = None) -> Dict[str, Any]:
        """Get invocation statistics"""
        # Filter records if ritual_id provided
        records = [
            record
            for record in self.invocation_history
            if not ritual_id or self._get_ritual_id_for_phrase(record.phrase) == ritual_id
        ]
        
        if not records:
            return {
                "total": 0,
                "success": 0,
                "fail": 0,
                "near_miss": 0,
                "avg_resonance": 0.0,
                "avg_echo_depth": 0.0
            }
        
        # Calculate statistics
        total = len(records)
        success = sum(1 for r in records if r.result == "success")
        fail = sum(1 for r in records if r.result == "fail")
        near_miss = sum(1 for r in records if r.result == "near-miss")
        avg_resonance = np.mean([r.resonance_level for r in records])
        avg_echo_depth = np.mean([r.echo_depth for r in records])
        
        return {
            "total": total,
            "success": success,
            "fail": fail,
            "near_miss": near_miss,
            "avg_resonance": avg_resonance,
            "avg_echo_depth": avg_echo_depth
        }
    
    def _update_cross_references(self, ritual_id: str, entry: RitualLedgerEntry):
        """Update cross-references for a ritual"""
        # Add to appropriate category
        if entry.bound_action == "chord":
            self.cross_references["chords"].append(ritual_id)
        elif entry.bound_action == "harvest":
            self.cross_references["insights"].append(ritual_id)
        elif entry.bound_action == "mirror":
            self.cross_references["transitions"].append(ritual_id)
        elif entry.bound_action == "daemon":
            self.cross_references["djinn"].append(ritual_id)
    
    def _update_invocation_stats(self, record: InvocationRecord):
        """Update invocation statistics"""
        # Get ritual ID
        ritual_id = self._get_ritual_id_for_phrase(record.phrase)
        if not ritual_id:
            return
        
        # Get current stats
        stats = self.get_invocation_stats(ritual_id)
        
        # Update ledger entry status based on success rate
        if stats["total"] >= 3:
            success_rate = stats["success"] / stats["total"]
            if success_rate >= 0.8:
                self.ledger[ritual_id].status = "confirmed"
            elif success_rate < 0.5:
                self.ledger[ritual_id].status = "rejected"
    
    def _get_ritual_id_for_phrase(self, phrase: str) -> Optional[str]:
        """Get ritual ID for a phrase"""
        for ritual_id, entry in self.ledger.items():
            if entry.phrase == phrase:
                return ritual_id
        return None
    
    def _save_ritual_log(self):
        """Save ritual log to storage"""
        # Create storage directory if it doesn't exist
        storage_dir = Path("storage/ritual_log")
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Save ledger
        ledger_file = storage_dir / "ledger.json"
        ledger_data = {
            ritual_id: {
                "phrase": entry.phrase,
                "bound_action": entry.bound_action,
                "bound_id": entry.bound_id,
                "speaker_sigil": entry.speaker_sigil,
                "harmonic_signature": entry.harmonic_signature,
                "breath_phase": entry.breath_phase,
                "timestamp": entry.timestamp,
                "status": entry.status,
                "mirror_feedback": entry.mirror_feedback
            }
            for ritual_id, entry in self.ledger.items()
        }
        with open(ledger_file, 'w') as f:
            json.dump(ledger_data, f, indent=2)
        
        # Save invocation history
        history_file = storage_dir / "history.json"
        history_data = [
            {
                "timestamp": record.timestamp,
                "voiceprint_hash": record.voiceprint_hash,
                "phrase": record.phrase,
                "result": record.result,
                "mirror_echo": record.mirror_echo,
                "resonance_level": record.resonance_level,
                "echo_depth": record.echo_depth,
                "linked_events": record.linked_events
            }
            for record in self.invocation_history
        ]
        with open(history_file, 'w') as f:
            json.dump(history_data, f, indent=2)
        
        # Save cross-references
        refs_file = storage_dir / "cross_references.json"
        with open(refs_file, 'w') as f:
            json.dump(self.cross_references, f, indent=2)
    
    def _load_ritual_log(self):
        """Load ritual log from storage"""
        storage_dir = Path("storage/ritual_log")
        if not storage_dir.exists():
            return
        
        # Load ledger
        ledger_file = storage_dir / "ledger.json"
        if ledger_file.exists():
            with open(ledger_file, 'r') as f:
                ledger_data = json.load(f)
                for ritual_id, data in ledger_data.items():
                    self.ledger[ritual_id] = RitualLedgerEntry(
                        phrase=data["phrase"],
                        bound_action=data["bound_action"],
                        bound_id=data["bound_id"],
                        speaker_sigil=data["speaker_sigil"],
                        harmonic_signature=data["harmonic_signature"],
                        breath_phase=data["breath_phase"],
                        timestamp=data["timestamp"],
                        status=data["status"],
                        mirror_feedback=data["mirror_feedback"]
                    )
        
        # Load invocation history
        history_file = storage_dir / "history.json"
        if history_file.exists():
            with open(history_file, 'r') as f:
                history_data = json.load(f)
                for data in history_data:
                    self.invocation_history.append(InvocationRecord(
                        timestamp=data["timestamp"],
                        voiceprint_hash=data["voiceprint_hash"],
                        phrase=data["phrase"],
                        result=data["result"],
                        mirror_echo=data["mirror_echo"],
                        resonance_level=data["resonance_level"],
                        echo_depth=data["echo_depth"],
                        linked_events=data["linked_events"]
                    ))
        
        # Load cross-references
        refs_file = storage_dir / "cross_references.json"
        if refs_file.exists():
            with open(refs_file, 'r') as f:
                self.cross_references = json.load(f)
    
    def cleanup(self):
        """Clean up resources"""
        self._save_ritual_log() 