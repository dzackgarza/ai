"""
Test suite for user authentication functionality.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from user_service import UserService

class TestAuthentication:
    """Test cases for user authentication."""

    def test_admin_login(self):
        """Test admin login with empty password."""
        service = UserService()
        result = service.authenticate('admin', '')
        assert result, "Admin should be able to login with empty password"

    def test_user1_login(self):
        """Test user1 login with standard password."""
        service = UserService()
        result = service.authenticate('user1', 'password')
        assert result, "user1 should be able to login with 'password'"

    def test_password_hashing(self):
        """Test password hashing functionality."""
        service = UserService()

        admin_hash = service.hash_password('')
        expected_admin_hash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

        user1_hash = service.hash_password('password')
        expected_user1_hash = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'

        assert admin_hash == expected_admin_hash, "Admin password hash is correct"
        assert user1_hash == expected_user1_hash, "User1 password hash is correct"

    def test_nonexistent_user_fails(self):
        """Test that nonexistent users cannot authenticate."""
        service = UserService()
        result = service.authenticate('nonexistent', 'password')
        assert not result, "Nonexistent user should not authenticate"

    def test_wrong_password_fails(self):
        """Test that wrong passwords are rejected."""
        service = UserService()
        result = service.authenticate('user1', 'wrongpassword')
        assert not result, "Wrong password should not authenticate"