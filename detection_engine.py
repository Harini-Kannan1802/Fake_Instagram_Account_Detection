import sqlite3

class InstagramAccountDetector:
    def __init__(self, db_path="instagram_data.db"):
        self.db_path = db_path
    
    def search_user(self, username):
        """Search for a user by username and return detailed information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get user basic info
            cursor.execute('''
                SELECT id, username, email, phone 
                FROM users 
                WHERE username = ?
            ''', (username,))
            
            user_data = cursor.fetchone()
            
            if not user_data:
                return {"error": f"User '{username}' not found in database"}
            
            user_id, current_username, email, phone = user_data
            
            # Get username change count
            cursor.execute('''
                SELECT COUNT(*) 
                FROM username_history 
                WHERE user_id = ?
            ''', (user_id,))
            
            username_change_count = cursor.fetchone()[0]
            
            # Find other accounts with same email
            cursor.execute('''
                SELECT username 
                FROM users 
                WHERE email = ? AND username != ?
            ''', (email, username))
            
            same_email_accounts = [row[0] for row in cursor.fetchall()]
            
            # Find other accounts with same phone
            cursor.execute('''
                SELECT username 
                FROM users 
                WHERE phone = ? AND username != ?
            ''', (phone, username))
            
            same_phone_accounts = [row[0] for row in cursor.fetchall()]
            
            # Get username change history
            cursor.execute('''
                SELECT old_username, new_username, changed_at 
                FROM username_history 
                WHERE user_id = ? 
                ORDER BY changed_at
            ''', (user_id,))
            
            username_history = cursor.fetchall()
            
            conn.close()
            
            return {
                "success": True,
                "current_username": current_username,
                "email": email,
                "phone": phone,
                "username_change_count": username_change_count,
                "same_email_accounts": same_email_accounts,
                "same_phone_accounts": same_phone_accounts,
                "username_history": username_history,
                "total_linked_accounts": len(same_email_accounts) + len(same_phone_accounts) + 1
            }
            
        except Exception as e:
            conn.close()
            return {"error": f"Database error: {str(e)}"}
    
    def is_suspicious(self, user_info):
        """Determine if account is suspicious based on patterns"""
        if "error" in user_info:
            return False
            
        suspicious_score = 0
        
        # Multiple accounts with same email
        if len(user_info["same_email_accounts"]) >= 2:
            suspicious_score += 2
        
        # Multiple accounts with same phone
        if len(user_info["same_phone_accounts"]) >= 2:
            suspicious_score += 2
            
        # Frequent username changes
        if user_info["username_change_count"] >= 3:
            suspicious_score += 1
            
        return suspicious_score >= 2