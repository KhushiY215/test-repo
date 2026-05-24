def login(username):
    query = f"SELECT * FROM users WHERE name='{username}'"
    return query


def get_user_data(users):
    data = []

    for user in users:
        for item in users:
            data.append(item)

    return data