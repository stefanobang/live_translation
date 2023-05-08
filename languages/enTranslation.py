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




name = "English Translation"
system("title "+name)

value_str = sys.argv[1]
inputType = int(value_str)

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
    try:
        while True:
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

            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            # options = whisper.DecodingOptions(language= 'Korean', fp16=False)
            options = whisper.DecodingOptions(language= 'en', fp16=False)
            translated_result = whisper.decode(model, mel, options)

            # #to prevent spamming random text every 5 seconds
            # if(len(translated_result.text) <= 10):
            #     continue

            end_time = time.time() #time ends
            #prevent spamming short text or short decode time
            if(end_time - prevent_spamTime <= 0.15 or len(translated_result.text)<=5):
                continue

            new_translated_result = re.sub(r"\.", ".\n", translated_result.text)
            print(f"Decode time: {round(end_time - prevent_spamTime,3)} secs")
            print(f"Time : {round(end_time - start_time,3)}sec ") #prints total time
            print("번역문: \n"+new_translated_result)
            print("----------------------------------\n")
                
    except KeyboardInterrupt:
        print("interrupted")


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