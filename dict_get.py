response_message = {
    "content": '''[
        {
            "text": "Hello, World!"
        }
    ]'''
}

response_message["content"][0]["text"] = 'bye'

print(response_message)