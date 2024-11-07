from datetime import datetime, timedelta
import json

def getApplicationsRemaining(username):
    try:
        # get successful applications for user
        with open(f'datafolders/{username}/output/success.json', 'r') as f:
            apps = json.load(f)
    except FileNotFoundError as e:
        print(f"Data for user {username} not found")
        return 0

    try:
        # get users
        with open('users.json', 'r') as users_file:
            users = json.load(users_file)
    except FileNotFoundError as e:
        print("users.json file not found")
        return 0
    
    try:
        user = list(filter(lambda u: u['username'] == username, users))
        user = user[0] if user else None
        if user is None:
            raise ValueError(f"User {username} not found")
    except ValueError as e:
        print(e)
        return 0
    
    subscriptionCycleStartDate = user['subscriptionCycleStartDate']
    subscriptionCycleEndDate = user['subscriptionCycleEndDate']

    # get applications for user in the current cycle
    appsInCycle = list(filter(lambda app: 'date' in app and app['date'] >= subscriptionCycleStartDate and app['date'] <= subscriptionCycleEndDate, apps))
    
    return user['applicationsPerCycle'] - len(appsInCycle)



    
print(getApplicationsRemaining('andrew_buensalida'))