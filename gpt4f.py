import g4f
from g4f.Provider import Bing

def chat(ask):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": ask}])
    return(response)

ask = input("Запрос: ")
print(chat(ask))

