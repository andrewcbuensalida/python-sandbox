x = ['a']
y = ['b']
z = x + y
# print(z)

class Message:
    def __init__(self, role):
        self.role = role

m = Message("role")

messages = [
    {
        "role":"system"
    }, # if it's a dictionary, have to use m['role']
    m, # if it's a class instance, have to use m.role
    {
        "role":"assistant",
        "tool_calls":[
            {
                "id": "1",
            }
        ]
    },
    {
        "role":"tool",
        "tool_call_id": "1"
    }
]


for message in messages:
    if isinstance(message, dict):
        print(message['role'])
    elif isinstance(message, Message):
        print(message.role)