"""
ML Predictor Module
Handles pattern recognition, prediction, and learning from system interactions
"""

import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
import joblib
import os

@dataclass
class PatternData:
    """Data structure for pattern recognition"""
    timestamp: float
    phase: str
    metrics: Dict[str, float]
    resonance: Dict[str, float]
    voice_state: Dict[str, Any]
    wick_state: Dict[str, Any]
    cursor_state: Dict[str, Any]
    mirror_state: Dict[str, Any]

class PatternDataset(Dataset):
    """Dataset for pattern recognition"""
    
    def __init__(self, patterns: List[PatternData], sequence_length: int = 10):
        self.patterns = patterns
        self.sequence_length = sequence_length
        self.scaler = StandardScaler()
        
        # Prepare features
        self.features = self._prepare_features()
        
    def _prepare_features(self) -> np.ndarray:
        """Convert pattern data to feature matrix"""
        features = []
        for pattern in self.patterns:
            # Combine all numerical features
            feature_vector = []
            
            # Add metrics
            feature_vector.extend(pattern.metrics.values())
            
            # Add resonance values
            feature_vector.extend(pattern.resonance.values())
            
            # Add voice state features
            feature_vector.extend([
                float(pattern.voice_state.get("intensity", 0)),
                float(pattern.voice_state.get("depth", 0)),
                float(pattern.voice_state.get("rhythm", 0))
            ])
            
            # Add wick state features
            feature_vector.extend([
                float(pattern.wick_state.get("stability", 0)),
                float(pattern.wick_state.get("coherence", 0)),
                float(pattern.wick_state.get("emergence", 0))
            ])
            
            features.append(feature_vector)
        
        # Scale features
        return self.scaler.fit_transform(np.array(features))
    
    def __len__(self) -> int:
        return len(self.patterns) - self.sequence_length
    
    def __getitem__(self, idx: int) -> tuple:
        """Get sequence of patterns and target"""
        sequence = self.features[idx:idx + self.sequence_length]
        target = self.features[idx + self.sequence_length]
        return torch.FloatTensor(sequence), torch.FloatTensor(target)

class PatternPredictor(nn.Module):
    """Neural network for pattern prediction"""
    
    def __init__(self, input_size: int, hidden_size: int = 64, num_layers: int = 2):
        super().__init__()
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, input_size)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass"""
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

class MLPredictor:
    """Main ML predictor class"""
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.model: Optional[PatternPredictor] = None
        self.scaler: Optional[StandardScaler] = None
        self.patterns: List[PatternData] = []
        
        # Create model directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
        
        # Load existing model if available
        self._load_model()
    
    def _load_model(self):
        """Load existing model and scaler"""
        model_path = os.path.join(self.model_dir, "pattern_predictor.pt")
        scaler_path = os.path.join(self.model_dir, "scaler.joblib")
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.model = torch.load(model_path)
            self.scaler = joblib.load(scaler_path)
    
    def save_model(self):
        """Save model and scaler"""
        if self.model is not None and self.scaler is not None:
            torch.save(self.model, os.path.join(self.model_dir, "pattern_predictor.pt"))
            joblib.dump(self.scaler, os.path.join(self.model_dir, "scaler.joblib"))
    
    def add_pattern(self, pattern: PatternData):
        """Add new pattern to dataset"""
        self.patterns.append(pattern)
    
    def train(self, epochs: int = 100, batch_size: int = 32, learning_rate: float = 0.001):
        """Train the model on collected patterns"""
        if len(self.patterns) < 20:  # Minimum patterns needed
            return
        
        # Create dataset and dataloader
        dataset = PatternDataset(self.patterns)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        # Initialize model if needed
        if self.model is None:
            input_size = dataset.features.shape[1]
            self.model = PatternPredictor(input_size)
        
        # Training setup
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Training loop
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            for batch_x, batch_y in dataloader:
                optimizer.zero_grad()
                output = self.model(batch_x)
                loss = criterion(output, batch_y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")
        
        # Save trained model
        self.save_model()
    
    def predict_next_state(self, current_patterns: List[PatternData]) -> Dict[str, Any]:
        """Predict next system state based on current patterns"""
        if self.model is None or len(current_patterns) < 10:
            return {}
        
        # Prepare input sequence
        dataset = PatternDataset(current_patterns)
        sequence = torch.FloatTensor(dataset.features[-10:]).unsqueeze(0)
        
        # Make prediction
        self.model.eval()
        with torch.no_grad():
            prediction = self.model(sequence)
        
        # Convert prediction back to original scale
        prediction = self.scaler.inverse_transform(prediction.numpy())
        
        # Map prediction back to system state
        return {
            "metrics": {
                "stability": float(prediction[0][0]),
                "coherence": float(prediction[0][1]),
                "emergence": float(prediction[0][2])
            },
            "resonance": {
                "intensity": float(prediction[0][3]),
                "depth": float(prediction[0][4]),
                "rhythm": float(prediction[0][5])
            },
            "voice_state": {
                "intensity": float(prediction[0][6]),
                "depth": float(prediction[0][7]),
                "rhythm": float(prediction[0][8])
            },
            "wick_state": {
                "stability": float(prediction[0][9]),
                "coherence": float(prediction[0][10]),
                "emergence": float(prediction[0][11])
            }
        }
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyze collected patterns for insights"""
        if not self.patterns:
            return {}
        
        # Calculate basic statistics
        metrics = {
            "total_patterns": len(self.patterns),
            "time_span": self.patterns[-1].timestamp - self.patterns[0].timestamp,
            "phase_distribution": {},
            "metric_averages": {},
            "resonance_averages": {}
        }
        
        # Analyze phase distribution
        for pattern in self.patterns:
            metrics["phase_distribution"][pattern.phase] = \
                metrics["phase_distribution"].get(pattern.phase, 0) + 1
        
        # Calculate averages
        for pattern in self.patterns:
            for key, value in pattern.metrics.items():
                if key not in metrics["metric_averages"]:
                    metrics["metric_averages"][key] = []
                metrics["metric_averages"][key].append(value)
            
            for key, value in pattern.resonance.items():
                if key not in metrics["resonance_averages"]:
                    metrics["resonance_averages"][key] = []
                metrics["resonance_averages"][key].append(value)
        
        # Calculate final averages
        for key in metrics["metric_averages"]:
            metrics["metric_averages"][key] = np.mean(metrics["metric_averages"][key])
        
        for key in metrics["resonance_averages"]:
            metrics["resonance_averages"][key] = np.mean(metrics["resonance_averages"][key])
        
        return metrics 