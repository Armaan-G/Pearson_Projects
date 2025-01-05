from openai import AzureOpenAI

# gets the API Key from environment variable AZURE_OPENAI_API_KEY
client = AzureOpenAI(
    api_key="181834e9dfb84c5290ac02465c8898c2",
    azure_endpoint="https://vue-sb-bi-openai.openai.azure.com/",
     api_version="2024-05-01-preview"
)

query = input("Query: ")
messages = None
completion = client.chat.completions.create(
    model="gpt-4",  # e.g. gpt-35-instant
    messages=[
        {
            "role": "user",
            "content": query,
        },
    ],
)
previousresponse = completion.choices[0].message.content

#messages.append({"role": "user", "content": "Which country won the most medals in that? Just tell me the country name?"} )
print("The answer to:" ,  query , "is")
print(completion.choices[0].message.content)