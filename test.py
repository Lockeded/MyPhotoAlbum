from zhipuai import ZhipuAI
client = ZhipuAI(api_key='c6d315f6befd6898be35ccf8cbbd1d1b.rl7aaq6xjvDtRBe3')
response = client.chat.completions.create(
    model="glm-4",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "请提供这张照片的描述"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "http://www.lockede.me/images/08153038518cd048af09d61da590d22f_JxkYU2H.jpg"
                }
            }
        ]
        }]
)
print(response.choices[0].message.content)
#   sk-5499188e2c7c4fd1bf392dae4686f367