from config import supabase

class EventFeedback:
    @staticmethod
    def submit_feedback(registration_id, event_id, student_id, rating, comment=None):
        """Student submits feedback for an event they attended"""
        try:
            result = supabase.table("event_feedback").insert({
                "registration_id": registration_id,
                "event_id": event_id,
                "student_id": student_id,
                "rating": rating,
                "comment": comment
            }).execute()
            return result
        except Exception as e:
            print(f"Error submitting feedback: {e}")
            return None

    @staticmethod
    def update_feedback(registration_id, rating, comment=None):
        """Student updates their feedback"""
        try:
            result = supabase.table("event_feedback").update({
                "rating": rating,
                "comment": comment
            }).eq("registration_id", registration_id).execute()
            return result
        except Exception as e:
            print(f"Error updating feedback: {e}")
            return None

    @staticmethod
    def get_feedback_by_registration(registration_id):
        """Get feedback for a specific registration"""
        try:
            result = supabase.table("event_feedback").select("*").eq("registration_id", registration_id).execute()
            return result
        except Exception as e:
            print(f"Error fetching feedback: {e}")
            return None

    @staticmethod
    def has_submitted_feedback(registration_id):
        """Check if student has already submitted feedback"""
        try:
            result = supabase.table("event_feedback").select("id").eq("registration_id", registration_id).execute()
            return result.data and len(result.data) > 0
        except Exception as e:
            print(f"Error checking feedback: {e}")
            return False

    @staticmethod
    def get_event_feedback(event_id):
        """Get all feedback for an event (for department view)"""
        try:
            result = supabase.table("event_feedback").select(
                "*, users!event_feedback_student_id_fkey(full_name, student_id, email)"
            ).eq("event_id", event_id).order("created_at", desc=True).execute()
            return result
        except Exception as e:
            print(f"Error fetching event feedback: {e}")
            return None

    @staticmethod
    def get_event_feedback_summary(event_id):
        """Get feedback summary statistics for an event"""
        try:
            result = supabase.table("event_feedback").select("rating").eq("event_id", event_id).execute()
            
            if not result.data:
                return {
                    "total_feedback": 0,
                    "average_rating": 0,
                    "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                }
            
            ratings = [f["rating"] for f in result.data]
            total = len(ratings)
            average = sum(ratings) / total if total > 0 else 0
            
            distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for rating in ratings:
                distribution[rating] += 1
            
            return {
                "total_feedback": total,
                "average_rating": round(average, 1),
                "rating_distribution": distribution
            }
        except Exception as e:
            print(f"Error calculating feedback summary: {e}")
            return {
                "total_feedback": 0,
                "average_rating": 0,
                "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }

    @staticmethod
    def get_student_feedback_history(student_id):
        """Get all feedback submitted by a student"""
        try:
            result = supabase.table("event_feedback").select(
                "*, events!event_feedback_event_id_fkey(event_name, date)"
            ).eq("student_id", student_id).order("created_at", desc=True).execute()
            return result
        except Exception as e:
            print(f"Error fetching student feedback history: {e}")
            return None
