# CONTRIBUTING

## PR / Issue 작성 방법
추가 예정 (TODO: Issue template도 찾아보기)

## 개발 환경 설정 방법

1. Python 3.11 설치
2. PyQT6 설치
3. 프로젝트 파일 열기

또는 로컬에 Poetry가 설치되어 있을 시, (poetry로 의존성 관리 예정)
    
 ```bash
 poetry install
 ```

## 배포 실행 파일 생성 방법

실행 파일 아이콘 :
- MacOS 용 : [rickTcal.icns](images/static/rickTcal.icns)
- Windows 용 : [rickTcal.ico](images/static/rickTcal.ico)

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
 - 실행 파일 생성
```bash
# 프로젝트 루트에서,

$ pyinstaller main.spec
```
 - 빌드 설정 초기화 및 새로운 실행 파일 생성(웬만하면 실행하지 말 것.)
```bash
# 프로젝트 루트에서,

# MacOS 환경
$ pyinstaller --onefile --windowed --icon=src/static/rickTcal.icns src/main.py

# Windows 환경
$ pyinstaller --onefile --windowed --icon=src/static/rickTcal.ico src/main.py
```