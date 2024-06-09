import dashscope
dashscope.api_key="sk-5499188e2c7c4fd1bf392dae4686f367"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "http://www.lockede.me/images/08153038518cd048af09d61da590d22f_JxkYU2H.jpg"},
            {"text": "这是什么?"}
        ]
    }
]
response = dashscope.MultiModalConversation.call(model=dashscope.MultiModalConversation.Models.qwen_vl_chat_v1,
                                                messages=messages)
print(response.output.choices[0].message.content)