import hashlib

class User:
    def __init__(self, id, name, personal_id, tel_no, address, username, password, role):
        self.id = id
        self.name = name
        self.personal_id = personal_id
        self.tel_no = tel_no
        self.address = address
        self.username = username
        self.password = password  # This should already be the hashed password in DB
        self.role = role

     # Getters and setters
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_role(self):
        return self.role

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email



    # Hash password (Abstraction: hides hashing logic)
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        hashed_input_password = User.hash_password(password)
        print(f"Comparing {hashed_input_password} with {self.password}")  # Debugging line
        return self.password == hashed_input_password
    
    # Polymorphism: Override in subclasses
    def display_info(self):
        return f"User: {self.__name}, Email: {self.__email}, Role: {self.__role}"


# Inheritance
class Customer(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, "customer", password)

    # Override display_info (Polymorphism)
    def display_info(self):
        return f"Customer: {self.get_name()}, Email: {self.get_email()}"

    def get_user_id(self):
        return self.__user_id


class Admin(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, "admin", password)

    # Override display_info (Polymorphism)
    def display_info(self):
        return f"Admin: {self.get_name()}, Email: {self.get_email()}"
