"""Test to investigate the authentication bug."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from user_service import UserService
import time

def test_trace_authentication():
    """Test that demonstrates the authentication issue."""
    service = UserService()

    # Get current time to understand the comparison
    current_time = int(time.time())
    created_at = service.users['admin']['created_at']

    print(f"Current time: {current_time}")
    print(f"Created at: {created_at}")
    print(f"Difference: {current_time - created_at} seconds")
    print(f"current_time < created_at: {current_time < created_at}")

    # Test the condition that's in the authenticate method
    if current_time < created_at:
        print("WOULD RETURN FALSE - account not yet created")
    else:
        print("WOULD CONTINUE - account is old enough")

    # Now test actual authentication
    result = service.authenticate('admin', '')
    print(f"\nAuthentication result: {result}")

    # Check each condition manually
    print("\nManual condition checks:")
    print(f"1. User exists: {'admin' in service.users}")
    print(f"2. Not locked: {service.users['admin']['failed_attempts'] < 3}")
    print(f"3. Password matches: {service.hash_password('') == service.users['admin']['password_hash']}")
    print(f"4. Time check passes: {not (current_time < created_at)}")

    assert result, f"Expected True but got {result}"

if __name__ == "__main__":
    test_trace_authentication()