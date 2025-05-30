# REQUIREMENTS

# 1) Read the file.
# If you are not able to accomplish this, you can skip this requirement by copying and pasting JSON content as string.
import json
from collections import Counter, defaultdict

import requests

orders = requests.get(
    "https://git.toptal.com/screeners/calories-json/-/raw/main/calories.json"
)
# 2) Parse JSON data
# You can use www.quicktype.io or any other tool of your preference to parse the data to a structured object.

parsed_orders = json.loads(orders.text)
print(parsed_orders[0])
# {'id': 1, 'user_id': '18', 'age': '33', 'user_weight': '91.88', 'name': 'Pasta Carbonara', 'price': 10.39, 'weight': 630, 'calories': 383, 'fat': 10.3, 'carbs': 5.95, 'protein': 12.67, 'time_consumed': '11:58', 'date_consumed': '2022-09-25', 'type': 'lunch', 'favorite': 'false', 'procedence': 'purchased'}

# 3) List all the favorite dishes that are under 1000 calories.
# Format the output in the following structure:
# Output: Food name, Date consumed and the Calories. Sort the list by the number of calories descending and display top 3 results.
parsed_orders.sort(key=lambda o: o["calories"], reverse=True)
# print(parsed_orders[:3])

fav_orders_under_1000_cal = [
    f"Name: {order['name']}, Date Consumed: {order['date_consumed']}, Calories: {order['calories']}"
    for order in parsed_orders
    if order["calories"] < 1000 and order["favorite"] == "true"
]

print(fav_orders_under_1000_cal[:3])
# 4) Find the user with the highest calorie consumption in November 2022.
# Output: user ID and calorie consumption in November 2022

user_consumption = {}

nov_2022_orders = [
    order
    for order in parsed_orders
    if order["date_consumed"] >= "2022-11-01" and order["date_consumed"] <= "2022-11-30"
]

for order in nov_2022_orders:
    user_id = order["user_id"]
    user_consumption[user_id] = user_consumption.get(user_id, 0) + order["calories"]
    # OR
    # if user_consumption.get(user_id):
    #     user_consumption[user_id] += order['calories']
    # else:
    #     user_consumption[user_id] = order['calories']

# print(user_consumption)
sorted_user_consumption = sorted(user_consumption.items(), key=lambda item: item[1])
print(sorted_user_consumption[-1:])

# alternative
max_user_consumption = max(user_consumption.items(), key=lambda item: item[1])
print(max_user_consumption)

# 5) List the 3 most frequent foods for a specific user with ID 10 in November 2022.
# Output: Lines in format “<name> - <occurrences>”

orders_for_user_id_10_nov_2022 = [
    order for order in nov_2022_orders if order["user_id"] == "10"
]

food_count = defaultdict(int)  # instead of dict so no need to check if key exists

for order in orders_for_user_id_10_nov_2022:
    food_count[order["name"]] += 1

sorted_food_count = sorted(food_count.items(), key=lambda f: f[1])

for food in sorted_food_count[-3:]:
    print(f"{food[0]} - {food[1]}")

# alternative
food_counter = Counter([order["name"] for order in orders_for_user_id_10_nov_2022])

for name, count in food_counter.most_common(3):
    print(f"{name} - {count}")
