import requests


def text_to_speech_yandex(text, language, speed):
    api_key = "860ff42f5fc847343d4e2a3ff87114fc6bf7151e"

    url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
    headers = {
        "Authorization": f"Api-Key {api_key}"
    }
    data = {
        "text": text,
        "lang": language,
        "speed": speed
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        with open("output.wav", "wb") as file:
            file.write(response.content)
