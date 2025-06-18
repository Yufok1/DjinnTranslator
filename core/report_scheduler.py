"""
Report Scheduler Module
Handles automated report generation and notifications
"""

import os
import json
import schedule
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Callable
from .analysis_reporter import AnalysisReporter

class ReportScheduler:
    """Manages automated report generation and notifications"""
    
    def __init__(self, 
                 config_file: str = "config/report_schedule.json",
                 email_config: Optional[Dict] = None):
        self.logger = logging.getLogger('ReportScheduler')
        self.config_file = config_file
        self.email_config = email_config
        self.reporter = AnalysisReporter()
        self.scheduler_thread = None
        self.running = False
        
        # Load schedule configuration
        self.schedule_config = self._load_config()
        
        # Initialize schedule
        self._setup_schedule()
    
    def _load_config(self) -> Dict:
        """Load schedule configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                # Default configuration
                config = {
                    'daily': {
                        'enabled': True,
                        'time': '23:00',
                        'time_range': '24h',
                        'notify': True
                    },
                    'weekly': {
                        'enabled': True,
                        'day': 'Sunday',
                        'time': '00:00',
                        'time_range': '7d',
                        'notify': True
                    },
                    'monthly': {
                        'enabled': True,
                        'day': 1,
                        'time': '00:00',
                        'time_range': '30d',
                        'notify': True
                    }
                }
                # Save default configuration
                os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
                with open(self.config_file, 'w') as f:
                    json.dump(config, f, indent=4)
                return config
        except Exception as e:
            self.logger.error(f"Error loading schedule config: {str(e)}")
            return {}
    
    def _setup_schedule(self):
        """Set up scheduled tasks"""
        # Clear existing schedule
        schedule.clear()
        
        # Set up daily report
        if self.schedule_config.get('daily', {}).get('enabled'):
            schedule.every().day.at(
                self.schedule_config['daily']['time']
            ).do(
                self._generate_daily_report
            )
        
        # Set up weekly report
        if self.schedule_config.get('weekly', {}).get('enabled'):
            schedule.every().week.at(
                self.schedule_config['weekly']['time']
            ).do(
                self._generate_weekly_report
            )
        
        # Set up monthly report
        if self.schedule_config.get('monthly', {}).get('enabled'):
            schedule.every().month.at(
                self.schedule_config['monthly']['time']
            ).do(
                self._generate_monthly_report
            )
    
    def _generate_daily_report(self):
        """Generate daily report"""
        try:
            self.logger.info("Generating daily report")
            report_path = self.reporter.generate_report(
                time_range=self.schedule_config['daily']['time_range']
            )
            
            if self.schedule_config['daily'].get('notify'):
                self._send_notification(
                    "Daily System Report",
                    f"Daily system report has been generated: {report_path}"
                )
            
            return report_path
        except Exception as e:
            self.logger.error(f"Error generating daily report: {str(e)}")
            return None
    
    def _generate_weekly_report(self):
        """Generate weekly report"""
        try:
            self.logger.info("Generating weekly report")
            report_path = self.reporter.generate_report(
                time_range=self.schedule_config['weekly']['time_range']
            )
            
            if self.schedule_config['weekly'].get('notify'):
                self._send_notification(
                    "Weekly System Report",
                    f"Weekly system report has been generated: {report_path}"
                )
            
            return report_path
        except Exception as e:
            self.logger.error(f"Error generating weekly report: {str(e)}")
            return None
    
    def _generate_monthly_report(self):
        """Generate monthly report"""
        try:
            self.logger.info("Generating monthly report")
            report_path = self.reporter.generate_report(
                time_range=self.schedule_config['monthly']['time_range']
            )
            
            if self.schedule_config['monthly'].get('notify'):
                self._send_notification(
                    "Monthly System Report",
                    f"Monthly system report has been generated: {report_path}"
                )
            
            return report_path
        except Exception as e:
            self.logger.error(f"Error generating monthly report: {str(e)}")
            return None
    
    def _send_notification(self, subject: str, message: str):
        """Send email notification"""
        if not self.email_config:
            self.logger.warning("Email configuration not provided")
            return
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from']
            msg['To'] = self.email_config['to']
            msg['Subject'] = subject
            
            # Add message body
            msg.attach(MIMEText(message, 'plain'))
            
            # Send email
            with smtplib.SMTP(
                self.email_config['smtp_server'],
                self.email_config['smtp_port']
            ) as server:
                server.starttls()
                server.login(
                    self.email_config['username'],
                    self.email_config['password']
                )
                server.send_message(msg)
            
            self.logger.info("Notification sent successfully")
        except Exception as e:
            self.logger.error(f"Error sending notification: {str(e)}")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def start(self):
        """Start the scheduler"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
            self.logger.info("Report scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        self.logger.info("Report scheduler stopped")
    
    def update_config(self, new_config: Dict):
        """Update schedule configuration"""
        try:
            # Update configuration
            self.schedule_config.update(new_config)
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(self.schedule_config, f, indent=4)
            
            # Update schedule
            self._setup_schedule()
            
            self.logger.info("Schedule configuration updated")
        except Exception as e:
            self.logger.error(f"Error updating schedule config: {str(e)}")
    
    def get_next_run(self) -> Dict[str, datetime]:
        """Get next scheduled run times"""
        next_runs = {}
        
        for job in schedule.get_jobs():
            if job.job_func == self._generate_daily_report:
                next_runs['daily'] = job.next_run
            elif job.job_func == self._generate_weekly_report:
                next_runs['weekly'] = job.next_run
            elif job.job_func == self._generate_monthly_report:
                next_runs['monthly'] = job.next_run
        
        return next_runs

def main():
    """Test the report scheduler"""
    # Example email configuration
    email_config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': 'your-email@gmail.com',
        'password': 'your-app-password',
        'from': 'your-email@gmail.com',
        'to': 'recipient@example.com'
    }
    
    # Create scheduler
    scheduler = ReportScheduler(email_config=email_config)
    
    try:
        # Start scheduler
        scheduler.start()
        
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop scheduler
        scheduler.stop()

if __name__ == '__main__':
    main() 