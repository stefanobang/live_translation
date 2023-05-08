<h1 align="center">Live Translator!!</h1>
It is a system speech transcription and translation application using whisper AI model.
It can be used to translate live stream and videos!

Whisper AI 모델을 이용한 시스템 음성 번역 애플리케이션입니다. 라이브 스트림과 비디오를 번역하는데 사용할 수 있습니다!


## Preview
<summary>Preview</summary>
    <p align="center">
        <img src="https://github.com/stefanobang/live_translation/blob/master/assets/Example1.png" width="500" height="500"> 
        <img src="https://github.com/stefanobang/live_translation/blob/master/assets/Example2.png" width="800" height="400">
        <img src="https://github.com/stefanobang/live_translation/blob/master/assets/Example3.png" width="800" height="400">
    </p>

## Pre-requirments
 [Whisper](https://github.com/openai/whisper) is required to be installed 
 ```bash
    pip install -U openai-whisper
```
    
It also requires the command-line tool [`ffmpeg`](https://ffmpeg.org/) to be installed on your system, which is available from most package managers:
```bash
# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg
# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

- Whisper uses vram/gpu to process the audio, so it is recommended to have a CUDA compatible GPU. 
- For each model requirement you can check directly at the [whisper repository](https://github.com/openai/whisper) 
- Must have at least Python 3.9. This project best work for any 3.9 version. 
- Python version above 3.10.9 might not work. 

## Requirments
- By running the setup.exe will install all the requirments (if I am correct)
- If you don`t want to use setup.exe

```bash
    pip install -r requirements.txt
```


## Compatibility
This project should be compatible with Windows only(tested on 10 & 11). 
Will add MacOs and Linux suppot in the near future.


## Installation
1. Donwlaod the Git Files
2. Run setup.exe (automatically install the libaries and will close when finished)
3. Run liveTranslation.exe !



## Running the app
Simply run the liveTranslation.exe file

## Future Development and Updates
- Add better translation model for Korean Translation
- Reduce the transcription time
- Improve the GUI
- Add more better UI that can provide better UX. 

## License
This project is licensed under the MIT License 