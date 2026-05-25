import hashlib

# Test what hash we get for empty string
empty_hash = hashlib.sha256(''.encode()).hexdigest()
print(f"Hash of empty string: {empty_hash}")
print("Expected: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
print(f"Match: {empty_hash == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}")

# Test what hash we get for 'password'
password_hash = hashlib.sha256('password'.encode()).hexdigest()
print(f"\nHash of 'password': {password_hash}")
print("Expected: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8")
print(f"Match: {password_hash == '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'}")