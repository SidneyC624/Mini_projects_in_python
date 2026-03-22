import asyncio
from googletrans import Translator

code_map = {
    "bn": "Bangla",
    "en": "English",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "he": "Hebrew",
    "hi": "Hindi",
    "it": "Italian",
    "ja": "Japanese",
    "la": "Latin",
    "ms": "Malay",
    "ne": "Nepali",
    "ru": "Russian",
    "ar": "Arabic",
    "zh": "Chinese",
    "es": "Spanish"
}

async def translate_text(code, text):
    async with Translator() as translator:
        result = await translator.translate(text=text, dest=code)
        return [result.src, result.text, result.pronunciation]
        

if __name__ == "__main__":
    valid = False
    while not valid:
        print("Please input desired language code. ")
        ans = input("To see the language code list enter 'options'\n")

        if ans.lower() == "options":
            print("Code : Language")
            for code in code_map:
                print(f"{code} => {code_map[code]}")
            print("")
        elif ans in code_map:
            print(f"You have selected {code_map[ans]}\n")
            valid = True
        else:
            print("You have entered an invalid language code.\n")

    while True:
        print("Write the text you want to translate:")
        text = input("To exit the program write 'close'\n")
        if text.lower() == "close":
            print("Terminating program...")
            break
        else:
            try:
                source, translated_text, pronunciation = asyncio.run(translate_text(ans, text))
                print(f"{code_map[ans]} translation: {translated_text}")
                print(f"Pronunciation: {pronunciation}")
                print(f"Translated from: {code_map[source]}")
            except Exception as e:
                print(f"An error occured: {e}")
