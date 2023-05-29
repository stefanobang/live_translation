import warnings
from numba import NumbaDeprecationWarning
warnings.filterwarnings("ignore", category=NumbaDeprecationWarning)
warnings.filterwarnings("ignore")
# Only for release version 

import soundcard as sc
import soundfile as sf
import whisper
import time
import multiprocessing as mp
import sys 
import re
from os import system

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



name = "English Translation"
system("title "+name)

value_str = sys.argv[1]
inputType = int(value_str)

# 0.2.0 update
#_______________________________________________________________________________________________________________________ 
def remove_repetitive_words(text):
    words = text.split(", ")
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    return ", ".join(unique_words)

def replace_repeated_sentences(text):
    sentences = text.split("\n")
    unique_sentences = []
    for sentence in sentences:
        if sentence.strip() not in unique_sentences:
            unique_sentences.append(sentence.strip())
    return "\n".join(unique_sentences)

# if there are more than 100character is a line will 
# print the last word before 100character and print the next word in next line
def add_newline(text):
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) <= 100:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    return "\n".join(lines)
#_______________________________________________________________________________________________________________________ 

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



#system sound capture
def record(conn):
    OUTPUT_FILE_NAME = "out.wav"    # file name.
    SAMPLE_RATE = 96000              # [Hz]. sampling rate.
    RECORD_SEC = 12                  # [sec]. duration recording audio.

    try:
        while True:
            with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
                currentState = False
                conn.send(currentState)

                # record audio with loopback from default speaker.
                data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
                
                # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
                sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)


                currentState = True
                conn.send(currentState)

    except KeyboardInterrupt:
        print("interrupted")
    
def decode(conn, start_time, inputVer):
    
    while True:
        try:
            model = whisper.load_model("base")
            if(inputVer == 0):
                model = whisper.load_model("base")
            elif(inputVer == 1):
                model = whisper.load_model("medium")
            elif(inputVer == 2):
                model = whisper.load_model("large")

            while True:
                currentState = conn.recv()
                if currentState:
                    break
            prevent_spamTime = time.time() #start time
            audio = whisper.load_audio("out.wav")
            audio = whisper.pad_or_trim(audio)

            # ;anguage 를 고정하지 않고 녹음을 했을 때 나오는 '시청해주셔서 감사합니다' 는 
            # language code 가 ko가 아니라  nn 으로 잡히네요. 이걸로 if 문 걸어서 걸러버리면 되네요
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            options = whisper.DecodingOptions(language= 'en', fp16=False)
            translated_result = whisper.decode(model, mel, options)

            

            # print(translated_result)

            if translated_result.language_probs is not None:
                if translated_result.language_probs < 0.2:
                    continue
            
            if translated_result.language_probs is None and translated_result.no_speech_prob>0.4:
                # print("\n\n\n continued for none")
                continue


            end_time = time.time() #time ends

            #prevent spamming short text or short decode time
            if(end_time - prevent_spamTime <= 0.15 or len(translated_result.text)<=5):
                continue

            new_translated_result = add_linebreaks(translated_result.text)

            # fix the Repeating words or text
            # Use regex to replace consecutive repeating words that occur more than three times with a single instance of that word
            pattern = re.compile(r'\b(\w+)\s+(\1\s+){3,}')
            new_translated_result = pattern.sub(r'\1 ', new_translated_result)

            # Use regex to replace consecutive repeating words that occur more than five times with three instances of that word
            pattern = re.compile(r'\b(\w+)\s+(\1\s+){4,}')
            new_translated_result = pattern.sub(r'\1 \1 \1 ', new_translated_result)


            new_translated_result = re.sub(r'(.)\1{5,}', r'\1'*6, new_translated_result)
    

            #Line breaks 
            new_translated_result = new_translated_result.replace("..", ".")
            new_translated_result = new_translated_result.replace("\n\n", "\n")
            new_translated_result = new_translated_result.replace(".\n.", ".")
            new_translated_result = new_translated_result.replace(".\n.", ".")
            new_translated_result = new_translated_result.replace("..", ".")

            # prevent repeating sentences or words
            new_translated_result = replace_repeated_sentences(new_translated_result)
            new_translated_result = remove_repetitive_words(new_translated_result)
            # If more than 100 characters will print the rest in new line
            new_translated_result = add_newline(new_translated_result)
            
            

            print(f"Decode time: {round(end_time - prevent_spamTime,3)} secs")
            print(f"Time : {round(end_time - start_time,3)}sec ") #prints total time
            print("번역문: \n"+new_translated_result)
            print("----------------------------------\n")

            

            # Open the image
            image = Image.open("./overlay/textImage_700X600.png")

            # Create a drawing object
            draw = ImageDraw.Draw(image)

            # Define the font and font size
            font = ImageFont.truetype("arial.ttf", 15)

            # Define the text to overlay
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
                


if __name__ == "__main__":       
    inputVer = inputType #temp
    if(inputVer == 0):
        print("Current Model is 'Base' and recommended for 8GB VRAM or less.")
    elif(inputVer == 1):
        print("Current Model is 'Medium' and above 8GB VRAM.")
    elif(inputVer == 2):
        print("Current Model is 'Large' and above 10GB VRAM.")

    
    print("During first start, it will take some times to install the model.....")
    print("Start English Translation!")
    start_time = time.time() #start time

    to_record, to_decode = mp.Pipe()
    record_sound = mp.Process(target=record,args = (to_decode,))
    decode_audio = mp.Process(target=decode, args = (to_record, start_time, inputVer))

    record_sound.start()
    decode_audio.start()

    record_sound.join()
    decode_audio.join()