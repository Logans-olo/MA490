def generate_user(**kwargs):
    for k, v in kwargs.items():
        with open(v, 'r') as file:
            content = file.read()
            A = content #TODO: Define some standard for taking a user's matrix
    return A