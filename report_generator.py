import pandas as pd
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, database):
        self.database = database
        
    def generate_attendance_report(self, output_file='attendance_report.xlsx'):
        """Generate an Excel report of all attendance records"""
        try:
            # Get all attendance records
            attendance_records = self.database.get_attendance()
            
            if not attendance_records:
                print("No attendance records found.")
                return False
                
            # Create a DataFrame from the records
            columns = ['ID', 'Student ID', 'Timestamp']
            df = pd.DataFrame(attendance_records, columns=columns)
            
            # Convert timestamp to readable format
            df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
            df['Time'] = pd.to_datetime(df['Timestamp']).dt.time
            
            # Get student information
            students = self.database.get_all_students()
            student_dict = {student[0]: student[1] for student in students}
            
            # Add student name to the DataFrame
            df['Student Name'] = df['Student ID'].map(student_dict)
            
            # Reorder columns for better readability
            final_columns = ['ID', 'Student ID', 'Student Name', 'Date', 'Time']
            df = df[final_columns]
            
            # Save to Excel
            df.to_excel(output_file, index=False)
            
            print(f"Attendance report generated: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error generating report: {e}")
            return False
            
    def generate_daily_report(self, date, output_file='daily_attendance.xlsx'):
        """Generate a daily attendance report"""
        try:
            # Get attendance records for the specific date
            attendance_records = self.database.get_attendance(date=date)
            
            if not attendance_records:
                print(f"No attendance records found for {date}.")
                return False
                
            # Create a DataFrame
            columns = ['ID', 'Student ID', 'Timestamp']
            df = pd.DataFrame(attendance_records, columns=columns)
            
            # Convert timestamp to readable format
            df['Time'] = pd.to_datetime(df['Timestamp']).dt.time
            
            # Get student information
            students = self.database.get_all_students()
            student_dict = {student[0]: student[1] for student in students}
            
            # Add student name
            df['Student Name'] = df['Student ID'].map(student_dict)
            
            # Reorder columns
            final_columns = ['ID', 'Student ID', 'Student Name', 'Time']
            df = df[final_columns]
            
            # Save to Excel
            df.to_excel(output_file, index=False)
            
            print(f"Daily attendance report generated: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error generating daily report: {e}")
            return False

if __name__ == "__main__":
    from database import AttendanceDatabase
    
    # Test the report generator
    db = AttendanceDatabase()
    report_gen = ReportGenerator(db)
    
    # Generate reports
    report_gen.generate_attendance_report()
    report_gen.generate_daily_report(datetime.now().date())