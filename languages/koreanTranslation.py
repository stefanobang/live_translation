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
import textwrap
from os import system

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


name = "Korean Translation"
system("title "+name)

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 48000              # [Hz]. sampling rate.
RECORD_SEC = 12                  # [sec]. duration recording audio.


def wrap_text(text):
    lines = []
    words = text.split()
    current_line = words[0]
    for word in words[1:]:
        if len(current_line) + len(word) + 1 <= 49:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return '\n'.join(lines)

def add_linebreaks(text):
    # Add double periods, exclamations, and question marks to avoid conflicting with sentence splits
    text = re.sub(r"\.", "..", text)
    text = re.sub(r"\!", "!!", text)
    text = re.sub(r"\?", "??", text)
    
    # Split the text by ". " and "? ", ignoring "!" since it can be part of a sentence
    sentences = re.split(r'\. |\? |\! ', text)
    new_sentences = []
    tempText = 0
    for sentence in sentences:
        # prevent last word duplicate stuff
        sentence = sentence.replace('..', '.')
        sentence = sentence.replace('!!', '!')
        sentence = sentence.replace('??', '?')

        words = sentence.split()    
        if len(words) < 5:
            tempText += len(words)
            
            if(tempText>4):
                if '.' in sentence:
                    sentence = sentence.replace('.', '.\n')
                if '?' in sentence:
                    sentence = sentence.replace('?', '?\n')
                if '!' in sentence:
                    sentence = sentence.replace('!', '!\n')
                tempText = 0
                new_sentences.append(sentence)

            else:
                new_sentences.append(sentence)

        else:
            if '.' in sentence:
                sentence = sentence.replace('.', '.\n')
            if '?' in sentence:
                sentence = sentence.replace('?', '?\n')
            if '!' in sentence:
                sentence = sentence.replace('!', '!\n')

            new_sentences.append(sentence)
            
    
    # Join the sentences back together
    new_text = ' '.join(new_sentences)

    # Remove double periods, exclamations, and question marks
    new_text = re.sub(r"\.\.", ".", new_text)
    new_text = re.sub(r"\!\!", "!", new_text)
    new_text = re.sub(r"\?\?", "?", new_text)


    return new_text





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
            
            # print("original:\n" + translated_result.text)
            
            new_translated_result = add_linebreaks(translated_result.text)

            # fix the Repeating words or text
            # Use regex to replace consecutive repeating words that occur more than three times with a single instance of that word
            pattern = re.compile(r'\b(\w+)\s+(\1\s+){3,}')
            new_translated_result = pattern.sub(r'\1 ', new_translated_result)

            # Use regex to replace consecutive repeating words that occur more than five times with three instances of that word
            pattern = re.compile(r'\b(\w+)\s+(\1\s+){4,}')
            new_translated_result = pattern.sub(r'\1 \1 \1 ', new_translated_result)


            # Use regex to replace consecutive repeating characters, except for 'ㅋ' that repeats more than 6 times, with a single instance
            # pattern = re.compile(r'(\w)\1{5,}')
            # new_translated_result = pattern.sub(r'\1', new_translated_result)

            new_translated_result = re.sub(r'(.)\1{5,}', r'\1'*6, new_translated_result)
    
            # Replace the 6 'ㅋ' characters with just one 'ㅋ'
            new_translated_result = re.sub(r'ㅋ{6}', 'ㅋㅋㅋㅋㅋㅋㅋ', new_translated_result)

            #Line breaks 
            new_translated_result = new_translated_result.replace("..", ".")
            
            # new_translated_result = add_linebreaks(new_translated_result)


            new_translated_result = new_translated_result.replace("\n\n", "\n")
            new_translated_result = new_translated_result.replace(".\n.", ".")
            new_translated_result = new_translated_result.replace(".\n.", ".")
            new_translated_result = new_translated_result.replace("..", ".")

            # print("Before wrap\n"+new_translated_result)

            # new_translated_result = wrap_text(new_translated_result)

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


