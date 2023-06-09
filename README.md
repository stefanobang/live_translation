<h1 align="center">Live Translator!!</h1>
It is a system speech transcription and translation application using whisper AI model.
It can be used to translate live stream and videos!

Whisper AI 모델을 이용한 시스템 음성 번역 애플리케이션입니다. 라이브 스트림과 비디오를 번역하는데 사용할 수 있습니다!


## Preview
<summary>Preview</summary>
    <p align="center">
        <img src="https://github.com/stefanobang/live_translation/blob/master/assets/Example1.png" width="500" height="500"> 
        <img src="https://github.com/stefanobang/live_translation/blob/master/assets/Example4.png" width="400" height="400"> 
        <img src="https://github.com/stefanobang/live_translation/blob/master/assets/Example5.png" width="400" height="400"> 
        <img src="https://github.com/stefanobang/live_translation/blob/master/assets/Example2.png" width="800" height="400">
        <img src="https://github.com/stefanobang/live_translation/blob/master/assets/Example3.png" width="800" height="400">
    </p>

## System Requirments

|  Size  | Parameters |  Multilingual model | Required VRAM | Relative speed |
|:------:|:----------:|:------------------:|:-------------:|:--------------:|
|  base  |    74 M    |       `base`       |     ~1 GB     |      ~16x      |
| medium |   769 M    |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |      `large`       |    ~10 GB     |       1x       |

- For Korean transaltion it utilize 'large' Multilingual model so having at least 10GB of VRAM is recommended
- 한국어 번역에는 'large' 다국어 모델을 사용하므로 최소 10GB의 VRAM을 권장합니다.

## Pre-requirements (사전준비)    
- Requires the command-line tool [`ffmpeg`](https://ffmpeg.org/) to be installed on your system, which is available from most package managers:
```bash
# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg
# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```
Englsih:
- Whisper uses vram/gpu to process the audio, so it is recommended to have a CUDA compatible GPU(NVIDA). 
- For each model requirement you can check directly at the [whisper repository](https://github.com/openai/whisper) 
- Must have at least Python 3.9. This project best work for any 3.9 version. 
- Python version above 3.9.9 might not work. 
- For Korean tranlsation you will need malgun.ttf font 
- Must install tkinter for the usage of overlay

Korean:
- 명령줄 도구 ['ffmpeg'](https://ffmpeg.org/) 를 시스템에 설치해야 합니다. (위에 설치 예시 및 링크 있습니다)
- Whisper는 vram/gpu를 사용하여 오디오를 처리하므로 CUDA 호환성 있는 GPU를 사용하는 것이 좋습니다. 
- 각 모델 요구 사항은 [whisper repository](https://github.com/openai/whisper)에서 직접 확인할 수 있습니다
- Python 3.9 이상이어야 합니다. 이 프로젝트는 모든 3.9 버전에 가장 적합합니다.
- 3.9.9 이상의 Python 버전은 작동하지 않을 수 있습니다.
- 한국어 번역을 위해서는 malgun.ttf (맑은 고딕) 폰트가 필요합니다.
- 오버레이를 사용하려면 tkinter를 설치해야 합니다



## Requirements (필수 파일 설치)
- By running the setup.exe will install all the requirments (if I am correct)
- If you don`t want to use setup.exe

```bash
    pip install -r requirements.txt
```
- setup.exe 파일 실행하면 
- setup.exe 외에 위에 있는 pip으로 설치 가능합니다

## Compatibility (호환성)
English:
- This project should be compatible with Windows only(tested on 10 & 11). 
- Will add MacOs and Linux suppot in the near future.
- Please note that this project works best on NIVIDA GPU with CUDA
- Does work on AMD GPU, but can`t expect the same level performance as NVIDA GPU

Korean:
- 이 프로젝트는 Windows 환경에서만 실행이 가능합니다(10 및 11에서 테스트됨)
- 추후 업데이트에서 MacOs 및 Linux 지원을 추가할 예정입니다.
- 이 프로젝트는 CUDA가 있는 NIVIDA GPU에서 가장 잘 작동합니다
- AMD GPU에서 작동하지만 NVIDA GPU와 같은 수준의 성능은 기대할 수 없습니다

## Installation (설치)
English:
1. Donwload the Git Files (zip recommended)
2. Run 'setup.exe' (automatically install the libaries and will close when finished)
3. Run 'liveTranslation.exe' !

한글:
1. Git 파일 다운로드 (zip으로 추천)
2. 'setup.exe'를 실행합니다(라이브러리를 자동으로 설치하고 완료되면 닫힙니다)
3. 'liveTranslation.exe'을 실행합니다!

## Usage (실행)
English:
1. Simply run the liveTranslation.exe file
2. Choose the langauge for translation (Choose 'base' or 'medium' or 'large' model then press the button)
- Please note that bigger the model the output is better!
- Output time varies depending on computer performance
3. For overlay, you must initate the translate first and then press the overlay button.
- If you close the process for the tranlstor, the overlay will not print the tranlated text

한글:
1. liveTranslation.exe 실행하면 됩니다
2. 번역할 언어 선택 ('base' or 'medium' or 'large' 모델 선택 후 버튼 누르기)
- 모델이 클수록 출력이 우수하다는 점에 유의하시기 바랍니다!
- 컴퓨터 성능에 따라 출력시간은 다릅니다
3. 번역 오버레이의 경우 번역 버튼을 먼저 실행한 뒤 오버레이 버튼을 눌러야 합니다.
- 번역기 프로세스를 닫으면 오버레이가 번역된 텍스트를 인쇄하지 않습니다

## Future Development and Updates (추후 업데이트)
- Add better translation model for Korean Translation
- Reduce the transcription time
- Improve the GUI
- Add more better UI that can provide better UX. 

## License
This project is licensed under the MIT License 

## TERMS OF SERVICE (서비스/사용자 약관)
All Rights Reserved
Copyright (c)\
THE AUTHOR(@stefanobang) IS NOT A LAW FIRM AND DOES NOT PROVIDE LEGAL SERVICES.

THE AUTHOR MAKES NO WARRANTIES REGARDING THE INFORMATION PROVIDED, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM ITS USE. 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
THE USER IS FULLY RESPONSIBLE FOR USING THIS SOFTWARE.


작성자는 제공된 정보에 대해 어떠한 보증도 하지 않으며, 제공된 정보의 사용으로 인한 손해에 대한 책임도 지지 않습니다.
소프트웨어는 명시적 또는 묵시적으로 어떠한 종류의 보증도 없이 "있는 그대로" 제공됩니다.
어떠한 경우에도 저작자 또는 저작권 소유자는  소프트웨어의 사용 또는 기타 거래로 인해 발생하는 불법 행위 또는 기타 행위, 계약의 행위에 관계없이 모든 청구, 손해 또는 기타 책임에 대해 책임을 지지 않습니다. 이 소프트웨어를 사용시 모든 책임은 사용자한테 있습니다.

