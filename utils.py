def get_valid_input(prompt, validation_func):
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        else:
            print("Invalid input. Please try again.")

def is_positive_int(value):
    return value.isdigit() and int(value) > 0

def is_string(value):
    return isinstance(value, str) and value.strip() != ""

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
