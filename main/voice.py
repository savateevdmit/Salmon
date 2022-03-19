import asyncio
import os  # работа с файловой системой

import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)

recognizer = speech_recognition.Recognizer()
microphone = speech_recognition.Microphone()


def record_and_recognize_audio(*args: tuple):
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            audio = recognizer.listen(microphone, 6, 6)
            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())
        except speech_recognition.WaitTimeoutError:
            return
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()
        except speech_recognition.UnknownValueError:
            pass
        except speech_recognition.RequestError:
            print("Trying to use offline recognition...")

        return recognized_data


def voicee(ctx):
    async def main(ctx):
        print('jhb')
        while True:

            # старт записи речи с последующим выводом распознанной речи
            # и удалением записанного в микрофон аудио
            try:
                channel = ctx.author
                voice_input = record_and_recognize_audio()
                os.remove("microphone-results.wav")
                if voice_input == 'стоп':
                    break
                elif 'иди' in voice_input and 'лосось' in voice_input:
                    cha = ctx.author.voice.channel
                    if cha != None:
                        await cha.connect()
                        continue
                    continue
                elif 'уйди' in voice_input and 'лосось' in voice_input and channel.voice != None:
                    await ctx.voice_client.disconnect()
                    continue
                await ctx.send(voice_input)

            except:
                pass

    asyncio.get_running_loop().create_task(main(ctx))
