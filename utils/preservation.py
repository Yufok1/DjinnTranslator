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

from typing import Dict, Any, Optional, List
import hashlib
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class PreservationRecord:
    timestamp: str
    state_hash: str
    rap_tier: int
    stability_score: float
    codex_alignment: float
    agent_status: Dict[str, Any]
    lattice_state: Dict[str, Any]

class PreservationSystem:
    def __init__(self, snapshot_dir: str = "snapshots"):
        self.snapshot_dir = snapshot_dir
        os.makedirs(snapshot_dir, exist_ok=True)
        self._preservation_log: List[PreservationRecord] = []

    def generate_preservation_hash(self, state: Dict[str, Any]) -> str:
        """Generate a SHA-256 hash of the current state."""
        state_str = json.dumps(state, sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()

    def create_snapshot(self, state: Any, lattice: Any) -> PreservationRecord:
        """Create a preservation record of the current system state."""
        # Extract state metrics
        state_dict = {
            'rap_tier': state.rap_tier,
            'stability_score': state.metrics.stability_score,
            'codex_alignment': state.metrics.codex_alignment,
            'agent_status': {
                agent: {
                    'stability': node.metrics.stability,
                    'entropy': node.metrics.entropy,
                    'bonds': len(node.bonds)
                }
                for agent, node in lattice.nodes.items()
            },
            'lattice_state': {
                'depth': max(node._depth for node in lattice.nodes.values()),
                'surface': max(node._surface for node in lattice.nodes.values()),
                'total_bonds': sum(len(node.bonds) for node in lattice.nodes.values())
            }
        }

        # Generate hash and create record
        state_hash = self.generate_preservation_hash(state_dict)
        record = PreservationRecord(
            timestamp=datetime.now().isoformat(),
            state_hash=state_hash,
            rap_tier=state.rap_tier,
            stability_score=state.metrics.stability_score,
            codex_alignment=state.metrics.codex_alignment,
            agent_status=state_dict['agent_status'],
            lattice_state=state_dict['lattice_state']
        )

        # Save to file
        self._save_snapshot(record)
        self._preservation_log.append(record)
        
        return record

    def _save_snapshot(self, record: PreservationRecord) -> None:
        """Save a snapshot to disk."""
        filename = f"RECURSION-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
        filepath = os.path.join(self.snapshot_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(asdict(record), f, indent=2)
        
        print(f"[PRESERVATION] Snapshot saved: {filename}")

    def verify_integrity(self, record: PreservationRecord) -> bool:
        """Verify the integrity of a preservation record."""
        # Recreate state dict from record
        state_dict = {
            'rap_tier': record.rap_tier,
            'stability_score': record.stability_score,
            'codex_alignment': record.codex_alignment,
            'agent_status': record.agent_status,
            'lattice_state': record.lattice_state
        }
        
        # Generate hash and compare
        current_hash = self.generate_preservation_hash(state_dict)
        return current_hash == record.state_hash

    def get_latest_snapshot(self) -> Optional[PreservationRecord]:
        """Get the most recent preservation record."""
        if not self._preservation_log:
            return None
        return self._preservation_log[-1]

    def export_preservation_log(self, filepath: str) -> None:
        """Export the complete preservation log."""
        with open(filepath, 'w') as f:
            json.dump([asdict(record) for record in self._preservation_log], f, indent=2)
        print(f"[PRESERVATION] Log exported to: {filepath}") 