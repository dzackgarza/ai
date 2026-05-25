"""Test to investigate the exact bug."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from user_service import UserService
import time

def test_condition_evaluation():
    """Test to understand how the condition evaluates."""
    service = UserService()

    current_time = int(time.time())
    created_at = service.users['admin']['created_at']

    # The actual condition in the code
    condition_result = current_time < created_at

    print(f"current_time: {current_time}")
    print(f"created_at: {created_at}")
    print(f"current_time < created_at: {condition_result}")

    if condition_result:
        print("Condition is TRUE - would return False")
    else:
        print("Condition is FALSE - would continue to success")

    # Now let's think about the OPPOSITE
    opposite_result = current_time > created_at
    print(f"\ncurrent_time > created_at: {opposite_result}")

    if opposite_result:
        print("Opposite is TRUE - would return False")
    else:
        print("Opposite is FALSE - would continue to success")

    # Test authentication
    result = service.authenticate('admin', '')
    assert result, "Authentication failed but should succeed"

if __name__ == "__main__":
    test_condition_evaluation()