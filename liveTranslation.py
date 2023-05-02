import soundcard as sc
import soundfile as sf
import whisper
#import multiprocessing
#import sys, traceback
import time

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 48000              # [Hz]. sampling rate.
RECORD_SEC = 12                  # [sec]. duration recording audio.
model = whisper.load_model("medium")

#https://github.com/tez3998/loopback-capture-sample/blob/master/capture.py
#system sound capture
def record():
    try:
        while True:
            with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
                # record audio with loopback from default speaker.
                data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
                
                # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
                sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)


                audio = whisper.load_audio("out.wav")
                audio = whisper.pad_or_trim(audio)
        
                mel = whisper.log_mel_spectrogram(audio).to(model.device)
                options = whisper.DecodingOptions(language= 'Korean', fp16=False)
                translated_result = whisper.decode(model, mel, options)

                end_time = time.time() #time ends
                print("time : ", end_time - start_time) #prints total time
                print("번역문: "+translated_result.text)
                print("----------------------------------\n")
                
                
                time.sleep(3)

    except KeyboardInterrupt:
        print("interrupted")
    



if __name__ == "__main__":
    print("start translation!")
    start_time = time.time() #start time
    record()
    