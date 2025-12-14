"""
Clean Database Script
Removes all test data while preserving user accounts
"""

import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def clean_database():
    """Clean all test data from database while keeping user accounts"""
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'cesms_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres')
        )
        
        cur = conn.cursor()
        
        print("🧹 Starting database cleanup...")
        print("=" * 50)
        
        # Get counts before deletion
        print("\n📊 Current data counts:")
        cur.execute("SELECT COUNT(*) FROM users")
        users_count = cur.fetchone()[0]
        print(f"   Users: {users_count}")
        
        cur.execute("SELECT COUNT(*) FROM event_management")
        events_count = cur.fetchone()[0]
        print(f"   Events: {events_count}")
        
        cur.execute("SELECT COUNT(*) FROM event_requests")
        requests_count = cur.fetchone()[0]
        print(f"   Event Requests: {requests_count}")
        
        cur.execute("SELECT COUNT(*) FROM event_registrations")
        registrations_count = cur.fetchone()[0]
        print(f"   Registrations: {registrations_count}")
        
        cur.execute("SELECT COUNT(*) FROM event_requirements")
        requirements_count = cur.fetchone()[0]
        print(f"   Requirements: {requirements_count}")
        
        cur.execute("SELECT COUNT(*) FROM attendance")
        attendance_count = cur.fetchone()[0]
        print(f"   Attendance: {attendance_count}")
        
        cur.execute("SELECT COUNT(*) FROM event_feedback")
        feedback_count = cur.fetchone()[0]
        print(f"   Feedback: {feedback_count}")
        
        print("\n🗑️  Deleting test data...")
        print("=" * 50)
        
        # Delete in correct order (respecting foreign keys)
        
        # 1. Delete feedback
        cur.execute("DELETE FROM event_feedback")
        print("✓ Deleted all event feedback")
        
        # 2. Delete attendance
        cur.execute("DELETE FROM attendance")
        print("✓ Deleted all attendance records")
        
        # 3. Delete requirements
        cur.execute("DELETE FROM event_requirements")
        print("✓ Deleted all event requirements")
        
        # 4. Delete registrations
        cur.execute("DELETE FROM event_registrations")
        print("✓ Deleted all event registrations")
        
        # 5. Delete events
        cur.execute("DELETE FROM event_management")
        print("✓ Deleted all events from event_management")
        
        cur.execute("DELETE FROM event_requests")
        print("✓ Deleted all event requests")
        
        # 6. Delete email verification codes (optional)
        cur.execute("DELETE FROM email_verification")
        print("✓ Deleted all email verification codes")
        
        # 7. Delete password reset tokens (optional)
        try:
            cur.execute("DELETE FROM password_reset_tokens")
            print("✓ Deleted all password reset tokens")
        except:
            print("⚠ Password reset tokens table not found (skipped)")
        
        # Commit changes
        conn.commit()
        
        print("\n✅ Database cleanup completed!")
        print("=" * 50)
        
        # Verify final counts
        print("\n📊 Final data counts:")
        cur.execute("SELECT COUNT(*) FROM users")
        print(f"   Users: {cur.fetchone()[0]} (preserved)")
        
        cur.execute("SELECT COUNT(*) FROM event_management")
        print(f"   Events: {cur.fetchone()[0]}")
        
        cur.execute("SELECT COUNT(*) FROM event_requests")
        print(f"   Event Requests: {cur.fetchone()[0]}")
        
        cur.execute("SELECT COUNT(*) FROM event_registrations")
        print(f"   Registrations: {cur.fetchone()[0]}")
        
        cur.execute("SELECT COUNT(*) FROM event_requirements")
        print(f"   Requirements: {cur.fetchone()[0]}")
        
        cur.execute("SELECT COUNT(*) FROM attendance")
        print(f"   Attendance: {cur.fetchone()[0]}")
        
        cur.execute("SELECT COUNT(*) FROM event_feedback")
        print(f"   Feedback: {cur.fetchone()[0]}")
        
        print("\n🎉 System is now clean and ready for production!")
        
        # Close connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if conn:
            conn.rollback()
        raise

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("CESMS DATABASE CLEANUP SCRIPT")
    print("=" * 50)
    print("\n⚠️  WARNING: This will delete all test data!")
    print("   - Events, registrations, requirements")
    print("   - Attendance records, feedback")
    print("   - Email verification codes")
    print("\n✓ User accounts will be preserved")
    
    response = input("\n❓ Continue? (yes/no): ").strip().lower()
    
    if response == 'yes':
        clean_database()
    else:
        print("\n❌ Cleanup cancelled.")
