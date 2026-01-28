import sqlite3
import os
from datetime import datetime

class AttendanceDatabase:
    def __init__(self, db_name='attendance.db'):
        self.db_name = db_name
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def add_student(self, student_id, name=None, email=None):
        """Add a new student to the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO students (id, name, email)
                VALUES (?, ?, ?)
            ''', (student_id, name, email))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Student already exists
            return False
        finally:
            conn.close()
            
    def mark_attendance(self, student_id):
        """Mark attendance for a student"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Check if student exists, if not add them
            cursor.execute('SELECT id FROM students WHERE id = ?', (student_id,))
            if not cursor.fetchone():
                self.add_student(student_id)
                
            # Mark attendance
            cursor.execute('''
                INSERT INTO attendance (student_id, timestamp)
                VALUES (?, ?)
            ''', (student_id, datetime.now()))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error marking attendance: {e}")
            return False
        finally:
            conn.close()
            
    def get_attendance(self, student_id=None, date=None):
        """Get attendance records"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM attendance'
        params = []
        
        if student_id:
            query += ' WHERE student_id = ?'
            params.append(student_id)
            
        if date:
            if student_id:
                query += ' AND'
            else:
                query += ' WHERE'
            
            query += ' DATE(timestamp) = DATE(?)'
            params.append(date)
            
        query += ' ORDER BY timestamp DESC'
        
        cursor.execute(query, params)
        records = cursor.fetchall()
        
        conn.close()
        return records
        
    def get_all_students(self):
        """Get all students from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students ORDER BY name')
        students = cursor.fetchall()
        
        conn.close()
        return students

if __name__ == "__main__":
    db = AttendanceDatabase()
    
    # Test the database
    print("Testing database...")
    
    # Add a student
    db.add_student("STUDENT123", "John Doe", "john@example.com")
    
    # Mark attendance
    db.mark_attendance("STUDENT123")
    
    # Get attendance
    attendance = db.get_attendance("STUDENT123")
    print(f"Attendance records: {attendance}")
    
    # Get all students
    students = db.get_all_students()
    print(f"Students: {students}")