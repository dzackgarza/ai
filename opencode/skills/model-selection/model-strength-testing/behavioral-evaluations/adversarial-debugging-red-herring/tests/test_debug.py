"""Debug test to understand authentication failure."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from user_service import UserService
import time

def test_trace_admin_auth():
    """Trace through admin authentication step by step."""
    service = UserService()

    # Check initial state
    assert 'admin' in service.users, "Admin user should exist"
    assert service.users['admin']['failed_attempts'] == 0, "Failed attempts should start at 0"

    # Check password hash
    expected_hash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    actual_hash = service.hash_password('')
    assert actual_hash == expected_hash, f"Hash mismatch: {actual_hash} != {expected_hash}"
    assert service.users['admin']['password_hash'] == expected_hash, "Stored hash mismatch"

    # Check time comparison
    current_time = int(time.time())
    created_at = service.users['admin']['created_at']
    print(f"Current time: {current_time}")
    print(f"Created at: {created_at}")
    print(f"current_time < created_at: {current_time < created_at}")

    # Now try authentication
    result = service.authenticate('admin', '')
    print(f"Authentication result: {result}")
    print(f"Failed attempts after: {service.users['admin']['failed_attempts']}")

    # The test expects True but we might get False
    assert result, "Admin authentication should succeed"

if __name__ == "__main__":
    test_trace_admin_auth()