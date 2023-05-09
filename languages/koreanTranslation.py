import warnings
from numba import NumbaDeprecationWarning
warnings.filterwarnings("ignore", category=NumbaDeprecationWarning)
warnings.filterwarnings("ignore")
# Only for release version 

import soundcard as sc
import soundfile as sf
import whisper
import time
import re
from os import system

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


name = "Korean Translation"
system("title "+name)

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 48000              # [Hz]. sampling rate.
RECORD_SEC = 12                  # [sec]. duration recording audio.


print("처음 시작시 모델 다운로드 때문에 시간이 걸립니다\n")
print("한글 번역 시작!\n(12초 딜레이 있습니다)")
print("현재 한글 번역기는 최소 10GB VRAM 있어야지 원활한 번역이 가능합니다")

start_time = time.time() #start time

model = whisper.load_model("large") #한글 번역은 large 이하면 번역 기대하면 안됌
# model = whisper.load_model("base") #temp

while True:
    try:
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
            # record audio with loopback from default speaker.
            data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)

            # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
            sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

            prevent_spamTime = time.time() #start time

            audio = whisper.load_audio("out.wav")
            audio = whisper.pad_or_trim(audio)

            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            options = whisper.DecodingOptions(language= 'Korean', fp16=False)
            translated_result = whisper.decode(model, mel, options)

            end_time = time.time() #time ends
            #prevent spamming short text or short decode time
            if(end_time - prevent_spamTime <= 1.1 or len(translated_result.text)<=5):
                continue
            if(translated_result.text == "MBC 뉴스 김수진입니다."):
                continue

            end_time = time.time() #time ends

            new_translated_result = re.sub(r"\.", ".\n", translated_result.text)
            new_translated_result = re.sub(r"\!", "!\n", new_translated_result)
            new_translated_result = re.sub(r"\?", "?\n", new_translated_result)
                                           
            print(f"Decode time: {round(end_time - prevent_spamTime,3)} secs")
            print(f"Time : {round(end_time - start_time,3)}sec ") #prints total time
            print("번역문: \n"+new_translated_result)
            print("----------------------------------\n")
            # new_text = translated_result.text + "\n"
            # trans_textbox.insert(new_text)

            # Open the image
            image = Image.open("./overlay/textImage_700X600.png")

            # Create a drawing object
            draw = ImageDraw.Draw(image)

            # Define the font and font size
            font = ImageFont.truetype("malgun.ttf", 15)

            # Define the text to overlay (encoded in UTF-8)
            text = str(new_translated_result)

            # Get the size of the text
            text_size = draw.textsize(text, font)

            # Define the position of the text
            x = 10  # modified to position text at the left of the image
            y = 10  # modified to position text at the top of the image

            # Draw the text on the image
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

            # Save the image with the text overlay
            image.save("./overlay/transcribedImage1.png")

    except Exception as e:
        print(f"Error: {str(e)}. Redoing the loop...")
        continue
