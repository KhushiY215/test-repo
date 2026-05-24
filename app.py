def login(username, password):
    query = f"SELECT * FROM users WHERE name='{username}' AND password='{password}'"
    return query


def danger_function(user_input): 
    eval(user_input)

    