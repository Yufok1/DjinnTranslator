"""
System Subsystem Module

Handles system transformations and domain merges.
Manages system modes, domain states, and merge operations.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime

@dataclass
class SystemTransformation:
    """Represents a system transformation operation."""
    id: str
    type: str
    scope: str
    start_time: datetime
    duration: float
    success: bool = False
    active: bool = True

@dataclass
class DomainMerge:
    """Represents a domain merge operation."""
    id: str
    target: str
    mode: str
    start_time: datetime
    duration: float
    success: bool = False
    active: bool = True

class SystemSubsystem:
    """Manages system transformations and domain merges."""
    
    def __init__(self):
        self.active_transformations: List[SystemTransformation] = []
        self.active_merges: List[DomainMerge] = []
        self.system_state: Dict = {
            'current_mode': 'passive',
            'active_domains': [],
            'merge_progress': 0.0,
            'transformation_progress': 0.0
        }
        
    def transform(self, type: str, scope: str) -> SystemTransformation:
        """
        Transform the system to the specified type and scope.
        
        Args:
            type: The type of transformation
            scope: The scope of the transformation
            
        Returns:
            The transformation operation
        """
        # Create transformation operation
        transformation = SystemTransformation(
            id=f"transform_{len(self.active_transformations)}",
            type=type,
            scope=scope,
            start_time=datetime.now(),
            duration=5.0  # Default duration in seconds
        )
        
        self.active_transformations.append(transformation)
        self._update_system_state()
        
        return transformation
    
    def merge(self, target: str, mode: str) -> DomainMerge:
        """
        Merge the specified target domain in the given mode.
        
        Args:
            target: The target domain to merge
            mode: The merge mode
            
        Returns:
            The merge operation
        """
        # Create merge operation
        merge = DomainMerge(
            id=f"merge_{len(self.active_merges)}",
            target=target,
            mode=mode,
            start_time=datetime.now(),
            duration=3.0  # Default duration in seconds
        )
        
        self.active_merges.append(merge)
        self._update_system_state()
        
        return merge
    
    def _update_system_state(self):
        """Update the overall system state based on active operations."""
        # Update transformation progress
        active_transforms = [t for t in self.active_transformations if t.active]
        if active_transforms:
            self.system_state['transformation_progress'] = sum(
                (datetime.now() - t.start_time).total_seconds() / t.duration
                for t in active_transforms
            ) / len(active_transforms)
            
            # Update current mode based on most recent transformation
            latest_transform = max(active_transforms, key=lambda t: t.start_time)
            self.system_state['current_mode'] = latest_transform.type
        
        # Update merge progress
        active_merges = [m for m in self.active_merges if m.active]
        if active_merges:
            self.system_state['merge_progress'] = sum(
                (datetime.now() - m.start_time).total_seconds() / m.duration
                for m in active_merges
            ) / len(active_merges)
            
            # Update active domains based on successful merges
            self.system_state['active_domains'] = [
                m.target for m in active_merges
                if m.success and m.active
            ]
    
    def get_system_state(self) -> Dict:
        """Get the current system state."""
        return self.system_state
    
    def cleanup(self):
        """Clean up resources and reset state."""
        self.active_transformations.clear()
        self.active_merges.clear()
        self.system_state = {
            'current_mode': 'passive',
            'active_domains': [],
            'merge_progress': 0.0,
            'transformation_progress': 0.0
        } 