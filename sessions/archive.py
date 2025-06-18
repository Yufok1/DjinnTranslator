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
Session Archive System
Manages system state snapshots and session history
"""

import os
import json
import yaml
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import hashlib
from pathlib import Path

@dataclass
class SessionState:
    """Represents a complete system state snapshot"""
    timestamp: str
    rap_tier: int
    stability_score: float
    agent_status: Dict[str, Dict[str, Any]]
    preservation_hash: str
    codex_manifest: Dict[str, Any]
    agent_trace: Dict[str, Any]
    pulse_log: Dict[str, Any]

class SessionArchive:
    """Manages system session archives and snapshots"""
    
    def __init__(self, base_dir: str = "sessions"):
        self.base_dir = Path(base_dir)
        self.sessions_dir = self.base_dir / "snapshots"
        self.logs_dir = self.base_dir / "logs"
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
    def create_snapshot(self, 
                       rap_tier: int,
                       stability_score: float,
                       agent_status: Dict[str, Dict[str, Any]],
                       preservation_hash: str,
                       codex_manifest: Dict[str, Any],
                       agent_trace: Dict[str, Any],
                       pulse_log: Dict[str, Any]) -> str:
        """Create a new session snapshot"""
        
        # Create session state
        state = SessionState(
            timestamp=datetime.utcnow().isoformat(),
            rap_tier=rap_tier,
            stability_score=stability_score,
            agent_status=agent_status,
            preservation_hash=preservation_hash,
            codex_manifest=codex_manifest,
            agent_trace=agent_trace,
            pulse_log=pulse_log
        )
        
        # Generate snapshot ID
        snapshot_id = self._generate_snapshot_id(state)
        
        # Save snapshot
        self._save_snapshot(snapshot_id, state)
        
        # Update session log
        self._update_session_log(snapshot_id, state)
        
        return snapshot_id
    
    def _generate_snapshot_id(self, state: SessionState) -> str:
        """Generate unique snapshot ID"""
        data = f"{state.timestamp}{state.rap_tier}{state.stability_score}{state.preservation_hash}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _save_snapshot(self, snapshot_id: str, state: SessionState):
        """Save snapshot to disk"""
        # Save as JSON
        json_path = self.sessions_dir / f"{snapshot_id}.json"
        with open(json_path, 'w') as f:
            json.dump(asdict(state), f, indent=2)
            
        # Save as YAML
        yaml_path = self.sessions_dir / f"{snapshot_id}.yaml"
        with open(yaml_path, 'w') as f:
            yaml.dump(asdict(state), f, default_flow_style=False)
    
    def _update_session_log(self, snapshot_id: str, state: SessionState):
        """Update session log with new snapshot"""
        log_path = self.logs_dir / "session_log.yaml"
        
        # Load existing log or create new
        if log_path.exists():
            with open(log_path, 'r') as f:
                log = yaml.safe_load(f) or {}
        else:
            log = {'snapshots': []}
            
        # Add new snapshot entry
        log['snapshots'].append({
            'id': snapshot_id,
            'timestamp': state.timestamp,
            'rap_tier': state.rap_tier,
            'stability_score': state.stability_score,
            'preservation_hash': state.preservation_hash
        })
        
        # Save updated log
        with open(log_path, 'w') as f:
            yaml.dump(log, f, default_flow_style=False)
    
    def get_snapshot(self, snapshot_id: str) -> Optional[SessionState]:
        """Retrieve a specific snapshot"""
        json_path = self.sessions_dir / f"{snapshot_id}.json"
        if not json_path.exists():
            return None
            
        with open(json_path, 'r') as f:
            data = json.load(f)
            return SessionState(**data)
    
    def list_snapshots(self) -> Dict[str, Dict[str, Any]]:
        """List all available snapshots"""
        log_path = self.logs_dir / "session_log.yaml"
        if not log_path.exists():
            return {}
            
        with open(log_path, 'r') as f:
            log = yaml.safe_load(f) or {}
            return {s['id']: s for s in log.get('snapshots', [])}
    
    def compare_snapshots(self, snapshot_id1: str, snapshot_id2: str) -> Dict[str, Any]:
        """Compare two snapshots"""
        snap1 = self.get_snapshot(snapshot_id1)
        snap2 = self.get_snapshot(snapshot_id2)
        
        if not snap1 or not snap2:
            return {'error': 'One or both snapshots not found'}
            
        return {
            'rap_tier_change': snap2.rap_tier - snap1.rap_tier,
            'stability_change': snap2.stability_score - snap1.stability_score,
            'time_difference': (
                datetime.fromisoformat(snap2.timestamp) - 
                datetime.fromisoformat(snap1.timestamp)
            ).total_seconds(),
            'agent_changes': self._compare_agent_states(
                snap1.agent_status,
                snap2.agent_status
            )
        }
    
    def _compare_agent_states(self, 
                            state1: Dict[str, Dict[str, Any]],
                            state2: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Compare agent states between snapshots"""
        changes = {}
        all_agents = set(state1.keys()) | set(state2.keys())
        
        for agent in all_agents:
            if agent not in state1:
                changes[agent] = {'status': 'added', 'details': state2[agent]}
            elif agent not in state2:
                changes[agent] = {'status': 'removed', 'details': state1[agent]}
            else:
                changes[agent] = {
                    'status': 'modified',
                    'changes': self._diff_dicts(state1[agent], state2[agent])
                }
                
        return changes
    
    def _diff_dicts(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two dictionaries and return differences"""
        changes = {}
        all_keys = set(dict1.keys()) | set(dict2.keys())
        
        for key in all_keys:
            if key not in dict1:
                changes[key] = {'status': 'added', 'value': dict2[key]}
            elif key not in dict2:
                changes[key] = {'status': 'removed', 'value': dict1[key]}
            elif dict1[key] != dict2[key]:
                changes[key] = {
                    'status': 'modified',
                    'old_value': dict1[key],
                    'new_value': dict2[key]
                }
                
        return changes
    
    def export_archive(self, output_dir: str):
        """Export entire archive to specified directory"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Copy snapshots
        snapshots_dir = output_path / "snapshots"
        snapshots_dir.mkdir(exist_ok=True)
        for snapshot_file in self.sessions_dir.glob("*.*"):
            with open(snapshot_file, 'r') as src, \
                 open(snapshots_dir / snapshot_file.name, 'w') as dst:
                dst.write(src.read())
                
        # Copy logs
        logs_dir = output_path / "logs"
        logs_dir.mkdir(exist_ok=True)
        for log_file in self.logs_dir.glob("*.*"):
            with open(log_file, 'r') as src, \
                 open(logs_dir / log_file.name, 'w') as dst:
                dst.write(src.read())
                
        # Create archive manifest
        manifest = {
            'export_timestamp': datetime.utcnow().isoformat(),
            'snapshot_count': len(list(self.sessions_dir.glob("*.*"))),
            'log_count': len(list(self.logs_dir.glob("*.*"))),
            'snapshots': self.list_snapshots()
        }
        
        with open(output_path / "archive_manifest.yaml", 'w') as f:
            yaml.dump(manifest, f, default_flow_style=False)

def main():
    """Command-line interface for session archive management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Session Archive Management")
    parser.add_argument("--snapshot", action="store_true", help="Create new snapshot")
    parser.add_argument("--list", action="store_true", help="List all snapshots")
    parser.add_argument("--compare", nargs=2, help="Compare two snapshots")
    parser.add_argument("--export", help="Export archive to directory")
    
    args = parser.parse_args()
    archive = SessionArchive()
    
    if args.snapshot:
        # Example snapshot creation
        snapshot_id = archive.create_snapshot(
            rap_tier=1,
            stability_score=0.95,
            agent_status={
                'cursor': {'active': True, 'stability': 0.9},
                'djinn': {'active': True, 'stability': 0.85},
                'arbiter': {'active': True, 'stability': 0.95},
                'olive_branch': {'active': True, 'stability': 0.9}
            },
            preservation_hash="example_hash",
            codex_manifest={'version': '1.0', 'rules': ['rule1', 'rule2']},
            agent_trace={'cursor': ['action1', 'action2']},
            pulse_log={'timestamp': '2024-01-01T00:00:00Z', 'type': 'heartbeat'}
        )
        print(f"Created snapshot: {snapshot_id}")
        
    elif args.list:
        snapshots = archive.list_snapshots()
        for snapshot_id, data in snapshots.items():
            print(f"\nSnapshot: {snapshot_id}")
            print(f"Timestamp: {data['timestamp']}")
            print(f"RAP Tier: {data['rap_tier']}")
            print(f"Stability: {data['stability_score']}")
            
    elif args.compare:
        comparison = archive.compare_snapshots(args.compare[0], args.compare[1])
        print("\nSnapshot Comparison:")
        print(f"RAP Tier Change: {comparison['rap_tier_change']}")
        print(f"Stability Change: {comparison['stability_change']}")
        print(f"Time Difference: {comparison['time_difference']} seconds")
        print("\nAgent Changes:")
        for agent, changes in comparison['agent_changes'].items():
            print(f"\n{agent}:")
            print(f"Status: {changes['status']}")
            if changes['status'] == 'modified':
                print("Changes:", changes['changes'])
                
    elif args.export:
        archive.export_archive(args.export)
        print(f"Archive exported to: {args.export}")

if __name__ == "__main__":
    main() 