import hashlib

class User:
    def __init__(self, name, personal_id, tel_no, address, username, password, role, user_id=None):
        self.user_id = user_id
        self.name = name
        self.personal_id = personal_id
        self.tel_no = tel_no
        self.address = address
        self.username = username
        self.password = password  # Store the plain text password
        self.hashed_password = self.hash_password(password)  # Store the hashed password
        self.role = role

    def hash_password(self, password):
        """Hash the user's password before saving."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, entered_password):
        """Verify if the entered password matches the stored hashed password."""
        return self.hashed_password == hashlib.sha256(entered_password.encode()).hexdigest()