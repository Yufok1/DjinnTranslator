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
Mirror Confirmation Module
Handles ritual confirmation and canonization through mirror resonance
"""

import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import numpy as np
from .ritual_log import RitualLog, RitualLedgerEntry
from .ml.predictor import MLPredictor
from .voice_processor import VoiceProcessor

@dataclass
class MirrorConfirmation:
    """Confirmation result from mirror resonance"""
    ritual_id: str
    timestamp: float
    insight_resonance: float  # Resonance with Mirror of Insight
    portent_resonance: float  # Resonance with Mirror of Portent
    harmonic_validity: float  # Overall harmonic validity
    confirmation_status: str  # "pending", "confirmed", "rejected"
    insight_feedback: Optional[str] = None
    portent_feedback: Optional[str] = None
    echo_depth: float = 0.0
    recursion_level: int = 0

class MirrorConfirmationSystem:
    """System for handling mirror confirmation of rituals"""
    
    def __init__(self, ritual_log: RitualLog):
        self.ritual_log = ritual_log
        self.ml_predictor = MLPredictor()
        self.voice_processor = VoiceProcessor()
        
        # Initialize confirmation history
        self.confirmation_history: Dict[str, List[MirrorConfirmation]] = {}
        
        # Load existing confirmations
        self._load_confirmations()
    
    def confirm_ritual(
        self,
        ritual_id: str,
        voice_data: np.ndarray,
        breath_phase: float,
        recursion_level: int = 0
    ) -> MirrorConfirmation:
        """Confirm a ritual through mirror resonance"""
        # Get ritual entry
        entry = self.ritual_log.ledger[ritual_id]
        
        # Check Mirror of Insight resonance
        insight_resonance, insight_feedback = self._check_insight_resonance(
            entry, voice_data, breath_phase
        )
        
        # Check Mirror of Portent resonance
        portent_resonance, portent_feedback = self._check_portent_resonance(
            entry, voice_data, breath_phase
        )
        
        # Calculate overall harmonic validity
        harmonic_validity = self._calculate_harmonic_validity(
            insight_resonance,
            portent_resonance,
            breath_phase,
            recursion_level
        )
        
        # Determine confirmation status
        confirmation_status = self._determine_confirmation_status(
            ritual_id,
            harmonic_validity,
            insight_resonance,
            portent_resonance
        )
        
        # Create confirmation record
        confirmation = MirrorConfirmation(
            ritual_id=ritual_id,
            timestamp=time.time(),
            insight_resonance=insight_resonance,
            portent_resonance=portent_resonance,
            harmonic_validity=harmonic_validity,
            confirmation_status=confirmation_status,
            insight_feedback=insight_feedback,
            portent_feedback=portent_feedback,
            echo_depth=self._calculate_echo_depth(voice_data),
            recursion_level=recursion_level
        )
        
        # Add to history
        if ritual_id not in self.confirmation_history:
            self.confirmation_history[ritual_id] = []
        self.confirmation_history[ritual_id].append(confirmation)
        
        # Update ritual status if confirmed
        if confirmation_status == "confirmed":
            entry.status = "confirmed"
            self.ritual_log._save_ritual_log()
        
        # Save confirmations
        self._save_confirmations()
        
        return confirmation
    
    def _check_insight_resonance(
        self,
        entry: RitualLedgerEntry,
        voice_data: np.ndarray,
        breath_phase: float
    ) -> Tuple[float, Optional[str]]:
        """Check resonance with Mirror of Insight"""
        # Extract voice features
        features = self.voice_processor.extract_features(voice_data)
        
        # Calculate resonance with ritual's harmonic signature
        resonance = self.ml_predictor.calculate_resonance(
            features,
            entry.harmonic_signature,
            breath_phase
        )
        
        # Generate feedback based on resonance
        if resonance > 0.8:
            feedback = "Strong resonance with insight patterns"
        elif resonance > 0.6:
            feedback = "Moderate resonance, potential for growth"
        else:
            feedback = "Weak resonance, consider realignment"
        
        return resonance, feedback
    
    def _check_portent_resonance(
        self,
        entry: RitualLedgerEntry,
        voice_data: np.ndarray,
        breath_phase: float
    ) -> Tuple[float, Optional[str]]:
        """Check resonance with Mirror of Portent"""
        # Extract voice features
        features = self.voice_processor.extract_features(voice_data)
        
        # Calculate predictive validity
        validity = self.ml_predictor.predict_harmonic_validity(
            features,
            entry.bound_action,
            breath_phase
        )
        
        # Generate feedback based on validity
        if validity > 0.8:
            feedback = "Strong portent alignment"
        elif validity > 0.6:
            feedback = "Moderate portent alignment"
        else:
            feedback = "Weak portent alignment"
        
        return validity, feedback
    
    def _calculate_harmonic_validity(
        self,
        insight_resonance: float,
        portent_resonance: float,
        breath_phase: float,
        recursion_level: int
    ) -> float:
        """Calculate overall harmonic validity"""
        # Base validity on resonance scores
        base_validity = (insight_resonance + portent_resonance) / 2
        
        # Adjust for breath phase alignment
        phase_alignment = 1.0 - abs(breath_phase - 0.5) * 2  # 1.0 at 0.5, 0.0 at 0.0 or 1.0
        phase_factor = 0.3 * phase_alignment
        
        # Adjust for recursion depth
        recursion_factor = min(0.2 * recursion_level, 0.2)
        
        # Calculate final validity
        validity = base_validity + phase_factor + recursion_factor
        
        return min(max(validity, 0.0), 1.0)
    
    def _determine_confirmation_status(
        self,
        ritual_id: str,
        harmonic_validity: float,
        insight_resonance: float,
        portent_resonance: float
    ) -> str:
        """Determine confirmation status based on resonance and history"""
        # Get confirmation history
        history = self.confirmation_history.get(ritual_id, [])
        
        # Check if we have enough history
        if len(history) < 2:
            return "pending"
        
        # Get recent confirmations
        recent = history[-2:]
        
        # Check if all recent confirmations are strong
        all_strong = all(
            c.harmonic_validity > 0.8 and
            c.insight_resonance > 0.8 and
            c.portent_resonance > 0.8
            for c in recent
        )
        
        if all_strong:
            return "confirmed"
        
        # Check if all recent confirmations are weak
        all_weak = all(
            c.harmonic_validity < 0.5 or
            c.insight_resonance < 0.5 or
            c.portent_resonance < 0.5
            for c in recent
        )
        
        if all_weak:
            return "rejected"
        
        return "pending"
    
    def _calculate_echo_depth(self, voice_data: np.ndarray) -> float:
        """Calculate echo depth from voice data"""
        # Extract echo features
        echo_features = self.voice_processor.extract_echo_features(voice_data)
        
        # Calculate depth
        depth = self.ml_predictor.calculate_echo_depth(echo_features)
        
        return depth
    
    def get_confirmation_history(self, ritual_id: str) -> List[MirrorConfirmation]:
        """Get confirmation history for a ritual"""
        return self.confirmation_history.get(ritual_id, [])
    
    def get_confirmation_stats(self, ritual_id: str) -> Dict[str, Any]:
        """Get confirmation statistics for a ritual"""
        history = self.confirmation_history.get(ritual_id, [])
        
        if not history:
            return {
                "total": 0,
                "confirmed": 0,
                "rejected": 0,
                "pending": 0,
                "avg_insight_resonance": 0.0,
                "avg_portent_resonance": 0.0,
                "avg_harmonic_validity": 0.0
            }
        
        # Calculate statistics
        total = len(history)
        confirmed = sum(1 for c in history if c.confirmation_status == "confirmed")
        rejected = sum(1 for c in history if c.confirmation_status == "rejected")
        pending = sum(1 for c in history if c.confirmation_status == "pending")
        
        avg_insight = np.mean([c.insight_resonance for c in history])
        avg_portent = np.mean([c.portent_resonance for c in history])
        avg_validity = np.mean([c.harmonic_validity for c in history])
        
        return {
            "total": total,
            "confirmed": confirmed,
            "rejected": rejected,
            "pending": pending,
            "avg_insight_resonance": avg_insight,
            "avg_portent_resonance": avg_portent,
            "avg_harmonic_validity": avg_validity
        }
    
    def _save_confirmations(self):
        """Save confirmation history to storage"""
        # Create storage directory if it doesn't exist
        storage_dir = Path("storage/mirror_confirmations")
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Save confirmation history
        history_file = storage_dir / "confirmations.json"
        history_data = {
            ritual_id: [
                {
                    "timestamp": c.timestamp,
                    "insight_resonance": c.insight_resonance,
                    "portent_resonance": c.portent_resonance,
                    "harmonic_validity": c.harmonic_validity,
                    "confirmation_status": c.confirmation_status,
                    "insight_feedback": c.insight_feedback,
                    "portent_feedback": c.portent_feedback,
                    "echo_depth": c.echo_depth,
                    "recursion_level": c.recursion_level
                }
                for c in confirmations
            ]
            for ritual_id, confirmations in self.confirmation_history.items()
        }
        with open(history_file, 'w') as f:
            json.dump(history_data, f, indent=2)
    
    def _load_confirmations(self):
        """Load confirmation history from storage"""
        storage_dir = Path("storage/mirror_confirmations")
        if not storage_dir.exists():
            return
        
        # Load confirmation history
        history_file = storage_dir / "confirmations.json"
        if history_file.exists():
            with open(history_file, 'r') as f:
                history_data = json.load(f)
                for ritual_id, confirmations in history_data.items():
                    self.confirmation_history[ritual_id] = [
                        MirrorConfirmation(
                            ritual_id=ritual_id,
                            timestamp=c["timestamp"],
                            insight_resonance=c["insight_resonance"],
                            portent_resonance=c["portent_resonance"],
                            harmonic_validity=c["harmonic_validity"],
                            confirmation_status=c["confirmation_status"],
                            insight_feedback=c["insight_feedback"],
                            portent_feedback=c["portent_feedback"],
                            echo_depth=c["echo_depth"],
                            recursion_level=c["recursion_level"]
                        )
                        for c in confirmations
                    ]
    
    def cleanup(self):
        """Clean up resources"""
        self._save_confirmations() 