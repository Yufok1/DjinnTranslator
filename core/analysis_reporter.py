"""
Analysis Reporter Module
Generates detailed analysis reports for system performance
"""

import os
import json
import glob
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import logging
from jinja2 import Template
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class AnalysisReporter:
    """Generates detailed analysis reports"""
    
    def __init__(self, 
                 state_dump_dir: str = "state_dumps",
                 report_dir: str = "reports"):
        self.state_dump_dir = state_dump_dir
        self.report_dir = report_dir
        self.logger = logging.getLogger('AnalysisReporter')
        
        # Create report directory if it doesn't exist
        os.makedirs(report_dir, exist_ok=True)
    
    def generate_report(self, 
                       time_range: str = "24h",
                       metrics: Optional[List[str]] = None) -> str:
        """Generate a comprehensive analysis report"""
        try:
            # Load state data
            data = self._load_state_data(time_range)
            if not data:
                return "No data available for analysis"
            
            # Convert to DataFrame
            df = self._prepare_dataframe(data)
            
            # Generate report sections
            sections = {
                'summary': self._generate_summary(df),
                'performance': self._generate_performance_analysis(df),
                'stability': self._generate_stability_analysis(df),
                'recovery': self._generate_recovery_analysis(df),
                'trends': self._generate_trend_analysis(df)
            }
            
            # Generate visualizations
            plots = self._generate_plots(df, metrics)
            
            # Generate HTML report
            report_path = self._generate_html_report(sections, plots)
            
            return f"Report generated: {report_path}"
            
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return f"Error generating report: {str(e)}"
    
    def _load_state_data(self, time_range: str) -> List[Dict]:
        """Load state data for the specified time range"""
        # Calculate cutoff time
        now = datetime.now()
        if time_range == "24h":
            cutoff = now - timedelta(hours=24)
        elif time_range == "7d":
            cutoff = now - timedelta(days=7)
        elif time_range == "30d":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = now - timedelta(hours=24)  # Default to 24h
        
        # Load state dumps
        data = []
        for file in glob.glob(os.path.join(self.state_dump_dir, "system_state_*.json")):
            try:
                timestamp = datetime.strptime(
                    os.path.basename(file).split('_')[2].split('.')[0],
                    "%Y%m%d_%H%M%S"
                )
                if timestamp >= cutoff:
                    with open(file, 'r') as f:
                        data.append(json.load(f))
            except Exception as e:
                self.logger.error(f"Error loading {file}: {str(e)}")
        
        return sorted(data, key=lambda x: x['timestamp'])
    
    def _prepare_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """Convert state data to DataFrame"""
        records = []
        for state in data:
            record = {
                'timestamp': datetime.strptime(state['timestamp'], "%Y%m%d_%H%M%S"),
                'cpu_usage': state['process_info']['cpu_percent'],
                'memory_usage': state['process_info']['memory_percent'],
                'cycle_time': state['performance_metrics']['cycle_times']['average'],
                'error_count': state['performance_metrics']['error_count'],
                'audio_buffer': state['audio_info']['buffer_size'],
                'thread_count': state['process_info']['num_threads']
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def _generate_summary(self, df: pd.DataFrame) -> Dict:
        """Generate summary statistics"""
        return {
            'time_range': {
                'start': df['timestamp'].min(),
                'end': df['timestamp'].max(),
                'duration': df['timestamp'].max() - df['timestamp'].min()
            },
            'metrics': {
                'cpu': {
                    'mean': df['cpu_usage'].mean(),
                    'max': df['cpu_usage'].max(),
                    'min': df['cpu_usage'].min()
                },
                'memory': {
                    'mean': df['memory_usage'].mean(),
                    'max': df['memory_usage'].max(),
                    'min': df['memory_usage'].min()
                },
                'cycle_time': {
                    'mean': df['cycle_time'].mean(),
                    'max': df['cycle_time'].max(),
                    'min': df['cycle_time'].min()
                },
                'errors': {
                    'total': df['error_count'].sum(),
                    'max_per_interval': df['error_count'].max()
                }
            }
        }
    
    def _generate_performance_analysis(self, df: pd.DataFrame) -> Dict:
        """Generate performance analysis"""
        return {
            'cpu_analysis': {
                'trend': self._calculate_trend(df['cpu_usage']),
                'spikes': self._detect_spikes(df['cpu_usage']),
                'correlation': self._calculate_correlations(df, 'cpu_usage')
            },
            'memory_analysis': {
                'trend': self._calculate_trend(df['memory_usage']),
                'spikes': self._detect_spikes(df['memory_usage']),
                'correlation': self._calculate_correlations(df, 'memory_usage')
            },
            'cycle_analysis': {
                'trend': self._calculate_trend(df['cycle_time']),
                'spikes': self._detect_spikes(df['cycle_time']),
                'correlation': self._calculate_correlations(df, 'cycle_time')
            }
        }
    
    def _generate_stability_analysis(self, df: pd.DataFrame) -> Dict:
        """Generate stability analysis"""
        return {
            'error_analysis': {
                'error_rate': df['error_count'].mean(),
                'error_patterns': self._analyze_error_patterns(df),
                'recovery_success': self._analyze_recovery_success(df)
            },
            'resource_stability': {
                'cpu_stability': self._calculate_stability_score(df['cpu_usage']),
                'memory_stability': self._calculate_stability_score(df['memory_usage']),
                'cycle_stability': self._calculate_stability_score(df['cycle_time'])
            }
        }
    
    def _generate_recovery_analysis(self, df: pd.DataFrame) -> Dict:
        """Generate recovery analysis"""
        return {
            'recovery_attempts': self._count_recovery_attempts(df),
            'recovery_success_rate': self._calculate_recovery_success_rate(df),
            'recovery_impact': self._analyze_recovery_impact(df)
        }
    
    def _generate_trend_analysis(self, df: pd.DataFrame) -> Dict:
        """Generate trend analysis"""
        return {
            'hourly_trends': self._calculate_hourly_trends(df),
            'daily_trends': self._calculate_daily_trends(df),
            'anomalies': self._detect_anomalies(df)
        }
    
    def _generate_plots(self, 
                       df: pd.DataFrame,
                       metrics: Optional[List[str]] = None) -> Dict[str, str]:
        """Generate visualization plots"""
        if metrics is None:
            metrics = ['cpu_usage', 'memory_usage', 'cycle_time', 
                      'error_count', 'audio_buffer', 'thread_count']
        
        plots = {}
        
        # Time series plots
        for metric in metrics:
            if metric in df.columns:
                plots[f'{metric}_time_series'] = self._plot_time_series(df, metric)
        
        # Correlation heatmap
        plots['correlation_heatmap'] = self._plot_correlation_heatmap(df)
        
        # Distribution plots
        for metric in metrics:
            if metric in df.columns:
                plots[f'{metric}_distribution'] = self._plot_distribution(df, metric)
        
        return plots
    
    def _plot_time_series(self, df: pd.DataFrame, metric: str) -> str:
        """Generate time series plot"""
        fig = go.Figure()
        
        # Add main line
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df[metric],
            mode='lines',
            name=metric
        ))
        
        # Add trend line
        z = np.polyfit(range(len(df)), df[metric], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=p(range(len(df))),
            mode='lines',
            name='Trend',
            line=dict(dash='dash')
        ))
        
        # Update layout
        fig.update_layout(
            title=f'{metric} Over Time',
            xaxis_title='Time',
            yaxis_title=metric,
            showlegend=True
        )
        
        # Save plot
        plot_path = os.path.join(self.report_dir, f'{metric}_time_series.html')
        fig.write_html(plot_path)
        
        return plot_path
    
    def _plot_correlation_heatmap(self, df: pd.DataFrame) -> str:
        """Generate correlation heatmap"""
        # Calculate correlations
        corr = df.corr()
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu'
        ))
        
        # Update layout
        fig.update_layout(
            title='Metric Correlations',
            xaxis_title='Metrics',
            yaxis_title='Metrics'
        )
        
        # Save plot
        plot_path = os.path.join(self.report_dir, 'correlation_heatmap.html')
        fig.write_html(plot_path)
        
        return plot_path
    
    def _plot_distribution(self, df: pd.DataFrame, metric: str) -> str:
        """Generate distribution plot"""
        fig = go.Figure()
        
        # Add histogram
        fig.add_trace(go.Histogram(
            x=df[metric],
            name=metric,
            nbinsx=30
        ))
        
        # Add KDE
        kde = sns.kdeplot(df[metric])
        fig.add_trace(go.Scatter(
            x=kde.get_lines()[0].get_xdata(),
            y=kde.get_lines()[0].get_ydata(),
            name='KDE',
            line=dict(color='red')
        ))
        
        # Update layout
        fig.update_layout(
            title=f'{metric} Distribution',
            xaxis_title=metric,
            yaxis_title='Frequency',
            showlegend=True
        )
        
        # Save plot
        plot_path = os.path.join(self.report_dir, f'{metric}_distribution.html')
        fig.write_html(plot_path)
        
        return plot_path
    
    def _generate_html_report(self, 
                            sections: Dict,
                            plots: Dict[str, str]) -> str:
        """Generate HTML report"""
        # Load template
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>System Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .section { margin: 20px 0; }
                .plot { margin: 20px 0; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>System Analysis Report</h1>
            
            <div class="section">
                <h2>Summary</h2>
                <p>Time Range: {{ sections.summary.time_range.start }} to {{ sections.summary.time_range.end }}</p>
                <p>Duration: {{ sections.summary.time_range.duration }}</p>
                
                <h3>Key Metrics</h3>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Mean</th>
                        <th>Max</th>
                        <th>Min</th>
                    </tr>
                    {% for metric, stats in sections.summary.metrics.items() %}
                    <tr>
                        <td>{{ metric }}</td>
                        <td>{{ "%.2f"|format(stats.mean) }}</td>
                        <td>{{ "%.2f"|format(stats.max) }}</td>
                        <td>{{ "%.2f"|format(stats.min) }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
            
            <div class="section">
                <h2>Performance Analysis</h2>
                {% for metric, analysis in sections.performance.items() %}
                <h3>{{ metric }}</h3>
                <p>Trend: {{ analysis.trend }}</p>
                <p>Spikes: {{ analysis.spikes }}</p>
                {% endfor %}
            </div>
            
            <div class="section">
                <h2>Stability Analysis</h2>
                {% for aspect, analysis in sections.stability.items() %}
                <h3>{{ aspect }}</h3>
                <p>{{ analysis }}</p>
                {% endfor %}
            </div>
            
            <div class="section">
                <h2>Recovery Analysis</h2>
                {% for aspect, analysis in sections.recovery.items() %}
                <h3>{{ aspect }}</h3>
                <p>{{ analysis }}</p>
                {% endfor %}
            </div>
            
            <div class="section">
                <h2>Trend Analysis</h2>
                {% for aspect, analysis in sections.trends.items() %}
                <h3>{{ aspect }}</h3>
                <p>{{ analysis }}</p>
                {% endfor %}
            </div>
            
            <div class="section">
                <h2>Visualizations</h2>
                {% for name, path in plots.items() %}
                <div class="plot">
                    <h3>{{ name }}</h3>
                    <iframe src="{{ path }}" width="100%" height="500px" frameborder="0"></iframe>
                </div>
                {% endfor %}
            </div>
        </body>
        </html>
        """
        
        template = Template(template_str)
        html = template.render(sections=sections, plots=plots)
        
        # Save report
        report_path = os.path.join(
            self.report_dir,
            f'analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        )
        
        with open(report_path, 'w') as f:
            f.write(html)
        
        return report_path
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """Calculate trend direction and magnitude"""
        z = np.polyfit(range(len(series)), series, 1)
        slope = z[0]
        
        if abs(slope) < 0.1:
            return "Stable"
        elif slope > 0:
            return f"Increasing ({slope:.2f} per interval)"
        else:
            return f"Decreasing ({abs(slope):.2f} per interval)"
    
    def _detect_spikes(self, series: pd.Series) -> List[Tuple[datetime, float]]:
        """Detect significant spikes in the data"""
        mean = series.mean()
        std = series.std()
        threshold = mean + 2 * std
        
        spikes = []
        for i, value in enumerate(series):
            if value > threshold:
                spikes.append((series.index[i], value))
        
        return spikes
    
    def _calculate_correlations(self, 
                              df: pd.DataFrame,
                              metric: str) -> Dict[str, float]:
        """Calculate correlations with other metrics"""
        correlations = {}
        for col in df.columns:
            if col != metric and col != 'timestamp':
                correlations[col] = df[metric].corr(df[col])
        
        return correlations
    
    def _analyze_error_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze error patterns"""
        return {
            'error_rate': df['error_count'].mean(),
            'error_clusters': self._detect_error_clusters(df),
            'error_correlations': self._calculate_correlations(df, 'error_count')
        }
    
    def _detect_error_clusters(self, df: pd.DataFrame) -> List[Dict]:
        """Detect clusters of errors"""
        clusters = []
        current_cluster = None
        
        for i, row in df.iterrows():
            if row['error_count'] > 0:
                if current_cluster is None:
                    current_cluster = {
                        'start': row['timestamp'],
                        'errors': [row['error_count']]
                    }
                else:
                    current_cluster['errors'].append(row['error_count'])
            elif current_cluster is not None:
                current_cluster['end'] = row['timestamp']
                current_cluster['total_errors'] = sum(current_cluster['errors'])
                clusters.append(current_cluster)
                current_cluster = None
        
        return clusters
    
    def _calculate_stability_score(self, series: pd.Series) -> float:
        """Calculate stability score (0-1)"""
        # Calculate coefficient of variation
        cv = series.std() / series.mean()
        
        # Convert to stability score (1 - normalized CV)
        return max(0, 1 - cv)
    
    def _count_recovery_attempts(self, df: pd.DataFrame) -> int:
        """Count number of recovery attempts"""
        # This would need to be implemented based on your recovery tracking
        return 0
    
    def _calculate_recovery_success_rate(self, df: pd.DataFrame) -> float:
        """Calculate recovery success rate"""
        # This would need to be implemented based on your recovery tracking
        return 0.0
    
    def _analyze_recovery_impact(self, df: pd.DataFrame) -> Dict:
        """Analyze impact of recovery attempts"""
        # This would need to be implemented based on your recovery tracking
        return {}
    
    def _calculate_hourly_trends(self, df: pd.DataFrame) -> Dict:
        """Calculate hourly trends"""
        df['hour'] = df['timestamp'].dt.hour
        hourly_means = df.groupby('hour').mean()
        
        return {
            'cpu': hourly_means['cpu_usage'].to_dict(),
            'memory': hourly_means['memory_usage'].to_dict(),
            'cycle_time': hourly_means['cycle_time'].to_dict()
        }
    
    def _calculate_daily_trends(self, df: pd.DataFrame) -> Dict:
        """Calculate daily trends"""
        df['day'] = df['timestamp'].dt.day_name()
        daily_means = df.groupby('day').mean()
        
        return {
            'cpu': daily_means['cpu_usage'].to_dict(),
            'memory': daily_means['memory_usage'].to_dict(),
            'cycle_time': daily_means['cycle_time'].to_dict()
        }
    
    def _detect_anomalies(self, df: pd.DataFrame) -> Dict:
        """Detect anomalies in the data"""
        anomalies = {}
        
        for column in ['cpu_usage', 'memory_usage', 'cycle_time']:
            # Calculate z-scores
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            
            # Find anomalies (z-score > 3)
            anomaly_indices = df.index[z_scores > 3]
            anomalies[column] = [
                {
                    'timestamp': df.loc[i, 'timestamp'],
                    'value': df.loc[i, column],
                    'z_score': z_scores[i]
                }
                for i in anomaly_indices
            ]
        
        return anomalies

def main():
    """Test the analysis reporter"""
    reporter = AnalysisReporter()
    
    # Generate report
    result = reporter.generate_report(time_range="24h")
    print(result)

if __name__ == '__main__':
    main() 