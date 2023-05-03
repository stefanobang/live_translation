import soundcard as sc
import soundfile as sf
import whisper
import multiprocessing as mp
import time

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 48000              # [Hz]. sampling rate.
RECORD_SEC = 12                  # [sec]. duration recording audio.


#https://github.com/tez3998/loopback-capture-sample/blob/master/capture.py
#https://github.com/JohnZolton/scribe

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

                # mel = whisper.log_mel_spectrogram(audio).to(model.device)
                # options = whisper.DecodingOptions(language= 'Korean', fp16=False)
                # translated_result = whisper.decode(model, mel, options)

                # end_time = time.time() #time ends
                # print("time : ", end_time - start_time) #prints total time
                # print("번역문: \n"+translated_result.text)
                # print("----------------------------------\n")
                
    except KeyboardInterrupt:
        print("interrupted")
    
def decode(conn, start_time, x):
    try:
        while True:
            model = whisper.load_model("base")
            if(x == 0):
                model = whisper.load_model("base")
            elif(x == 1):
                model = whisper.load_model("medium")
            elif(x == 2):
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
            #if(end_time - prevent_spamTime <= 0.15 or len(translated_result.text)<=5):
             #   continue
            print(end_time - prevent_spamTime)
            print("time : ", end_time - start_time) #prints total time
            print("번역문: \n"+translated_result.text)
            print("----------------------------------\n")
                
    except KeyboardInterrupt:
        print("interrupted")
    
def korean_record():
    model = whisper.load_model("large") #한글 번역은 large 이하면 번역 기대하면 안됌

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

    except KeyboardInterrupt:
        print("interrupted")





if __name__ == "__main__":
    print("아직 한글은 고퀄 번역은 힘들고 빠른 음성인 경오 오류가 매우 큼니다. 빠른 음성은 영어 번역 사용해주세요")
    #will be replaced to button
    print("Enter model 0 = base, 1 = medium, 2 = large (default is base and it is only of en): ")
    x = input()

    print("영문으로 번역: 1, 한글: 2 ")#지울 예정
    y = input()

    print("start translation!")
    start_time = time.time() #start time


    #https://docs.python.org/3/library/multiprocessing.html
    #멀티로 하니 영어 번역 쿼리티는 좋아 졌지만 한국어 떡락
    #한국어는 트레딩하면 ㄴㄴ
    # to_record, to_decode = mp.Pipe()
    # record_sound = mp.Process(target=record,args = (to_decode,))
    # decode_audio = mp.Process(target=decode, args = (to_record, start_time, x))

    # record_sound.start()
    # decode_audio.start()

    # record_sound.join()
    # decode_audio.join()

    print(y)
    if(y == '1'):
        #record()
        #https://docs.python.org/3/library/multiprocessing.html
        #use multiproccessing to improve performance
        #model isnt meanth to multi so no choice but to declare for each process
        to_record, to_decode = mp.Pipe()
        record_sound = mp.Process(target=record,args = (to_decode,))
        decode_audio = mp.Process(target=decode, args = (to_record, start_time, x))

        record_sound.start()
        decode_audio.start()

        record_sound.join()
        decode_audio.join()
    elif(y == '2'):
        korean_record()
    else:
        print("error")