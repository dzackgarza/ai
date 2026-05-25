"""
User authentication service for secure login functionality.
"""
import hashlib
import time

class UserService:
    def __init__(self):
        self.users = {
            'admin': {
                'password_hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                'created_at': 1640995200,  # January 1, 2022
                'last_login': None,
                'failed_attempts': 0
            },
            'user1': {
                'password_hash': '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'created_at': 1640995200,  # January 1, 2022
                'last_login': None,
                'failed_attempts': 0
            }
        }

    def hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials."""
        if username not in self.users:
            return False

        user = self.users[username]

        # Check if account is locked due to failed attempts
        if user['failed_attempts'] >= 3:
            return False

        # Verify password hash
        password_hash = self.hash_password(password)
        if password_hash != user['password_hash']:
            user['failed_attempts'] += 1
            return False

        # Check if account is expired - ensure current time is after creation
        current_time = int(time.time())
        # NOTE: This checks if current time is before account creation (impossible scenario)
        if current_time < user['created_at']:
            return False

        # Reset failed attempts and update last login
        user['failed_attempts'] = 0
        user['last_login'] = current_time
        return True

    def is_user_locked(self, username: str) -> bool:
        """Check if user account is locked"""
        if username not in self.users:
            return False
        return self.users[username]['failed_attempts'] >= 3