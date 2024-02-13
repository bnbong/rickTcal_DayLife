# CONTRIBUTING

## PR / Issue 작성 방법
추가 예정

## 개발 환경 설정 방법

1. Python 3.11 설치
2. PyQT6 설치
3. PyQT Designer 설치
4. PyQT Designer 실행
5. 프로젝트 파일 열기

또는 로컬에 Poetry가 설치되어 있을 시, (poetry로 의존성 관리 예정)
    
 ```bash
 poetry install
 ```

## 배포 실행 파일 생성 방법

실행 파일 아이콘 :
- MacOS 용 : [rickTcal.icns](./src/static/rickTcal.icns)
- Windows 용 : [rickTcal.ico](./src/static/rickTcal.ico)

### 0. pyinstaller 설치
```bash
# 로컬에 pyinstaller 개별 설치
$ pip install pyinstaller
```

```bash
# 또는 로컬에 개발 환경 의존성 통합 설치
$ pip install -r requirements.txt
```


### 1. 명렁어 실행
 - 실행 파일 생성(MacOS 개발 환경에서)
```bash
# 프로젝트 루트에서,

$ pyinstaller --onefile --windowed --icon=src/static/rickTcal.icns src/main.py
```
 - 실행 파일 생성(Windows 개발 환경에서)
```bash
# 프로젝트 루트에서,

$ pyinstaller --onefile --windowed --icon=src/static/rickTcal.ico src/main.py
```