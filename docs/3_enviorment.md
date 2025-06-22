# 3. Environment (환경)

## 목차

- [3.1 Operating Environment (운영 환경)](#31-operating-environment-운영-환경)
    - [3.1.1 Hardware Environment (하드웨어 환경)](#311-hardware-environment-하드웨어-환경)
    - [3.1.2 Software Environment (소프트웨어 환경)](#312-software-environment-소프트웨어-환경)
        - [3.1.2.1 OS Environment (운영체제 환경)](#3121-os-environment-운영체제-환경)
        - [3.1.2.2 OS 외 Software 환경](#3122-os-외-software-환경)
- [3.2 Product Installation and Configuration (제품 설치 및 설정)](#32-product-installation-and-configuration-제품-설치-및-설정)
    - [3.2.1 전제 조건](#321-전제-조건)
    - [3.2.2 설치 단계](#322-설치-단계)
- [3.3 Distribution Environment (배포 환경)](#33-distribution-environment-배포-환경)
    - [3.3.1 Master Configuration (마스터 구성)](#331-master-configuration-마스터-구성)
    - [3.3.2 Distribution Method (배포 방법)](#332-distribution-method-배포-방법)
    - [3.3.3 Patch/Update Method (패치와 업데이트 방법)](#333-patchupdate-method-패치와-업데이트-방법)
- [3.4 Development Environment (개발 환경)](#34-development-environment-개발-환경)
    - [3.4.1 Hardware Environment (하드웨어 환경)](#341-hardware-environment-하드웨어-환경)
    - [3.4.2 Software Environment (소프트웨어 환경)](#342-software-environment-소프트웨어-환경)
- [3.5 Test Environment (테스트 환경)](#35-test-environment-테스트-환경)
    - [3.5.1 Hardware Environment (하드웨어 환경)](#351-hardware-environment-하드웨어-환경)
    - [3.5.2 Software Environment (소프트웨어 환경)](#352-software-environment-소프트웨어-환경)
- [3.6 Configuration Management (형상관리)](#36-configuration-management-형상관리)
    - [3.6.1 Location of Outputs (산출물 위치)](#361-location-of-outputs-산출물-위치)
        - [3.6.1.1 Location of Source Code (소스코드 위치)](#3611-location-of-source-code-소스코드-위치)
        - [3.6.1.2 Location of Documents (문서 위치)](#3612-location-of-documents-문서-위치)
    - [3.6.2 Build Environment (빌드 환경)](#362-build-environment-빌드-환경)
    - [3.6.3 Bugtrack System (버그트래킹)](#363-bugtrack-system-버그트래킹)
    - [3.6.4 Other Environment (기타 환경)](#364-other-environment-기타-환경)

## 3.1 Operating Environment (운영 환경)

### 3.1.1 Hardware Environment (하드웨어 환경)

- **CPU**: 멀티코어 프로세서 (예: Intel Xeon 또는 AMD EPYC 계열)
- **RAM**: 8GB 이상 (서비스 규모 및 동시 접속자 수에 따라 유동적으로 조정)
- **저장 공간**: 100GB 이상 (고성능 SSD 권장)
- **네트워크**: 1Gbps 이상의 네트워크 인터페이스

### 3.1.2 Software Environment (소프트웨어 환경)

#### 3.1.2.1 OS Environment (운영체제 환경)

- **Linux**: Ubuntu 22.04 LTS 또는 CentOS 7/8 (서버 운영 환경)
- **Windows Server**: 2019/2022 (선택 사항, 개발 및 테스트 환경)

#### 3.1.2.2 OS 외 Software 환경

- **Python**: 3.x (Django 및 관련 라이브러리 실행 환경)
- **Django**: 5.2.3 (웹 프레임워크)
- **Django REST Framework**: 3.16.0 (RESTful API 구축)
- **drf-spectacular**: 0.28.0 (OpenAPI 3.0 스키마 자동 생성)
- **PyYAML**: 6.0.2 (YAML 파싱 및 생성)
- **기타 라이브러리**:
    - asgiref==3.8.1
    - attrs==25.3.0
    - inflection==0.5.1
    - jsonschema==4.24.0
    - jsonschema-specifications==2025.4.1
    - referencing==0.36.2
    - rpds-py==0.25.1
    - sqlparse==0.5.3
    - typing_extensions==4.14.0
    - uritemplate==4.2.0

---

## 3.2 Product Installation and Configuration (제품 설치 및 설정)

본 섹션에서는 제품을 설치하고 설정하는 방법에 대한 자세한 지침을 제공합니다.

### 3.2.1 전제 조건

제품을 설치하기 전에 다음 소프트웨어가 시스템에 설치되어 있는지 확인하십시오.

* **Git**: 소스 코드 저장소를 클론하는 데 필요합니다.
* **Python 3.x**: Django 및 관련 라이브러리를 실행하는 데 필요합니다. (권장 버전: 3.9 이상)
* **pip**: Python 패키지 관리자입니다. Python 설치 시 함께 설치됩니다.

### 3.2.2 설치 단계

다음 단계에 따라 제품을 설치하고 설정합니다.

1. **저장소 클론**:
   Git을 사용하여 프로젝트 저장소를 로컬 시스템에 복제합니다.

   ```bash
   git clone [프로젝트 저장소 URL]
   cd tpjt-django-timesale-api
   ```

2. **가상 환경 설정**:
   프로젝트 의존성을 격리하기 위해 Python 가상 환경을 생성하고 활성화합니다.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 또는 Windows: .\venv\Scripts\activate
   ```

3. **의존성 설치**:
   `requirements.txt` 파일에 명시된 모든 Python 패키지를 설치합니다.

   ```bash
   pip install -r requirements.txt
   ```

4. **데이터베이스 마이그레이션**:
   Django 모델을 기반으로 데이터베이스 스키마를 생성하고 초기 데이터를 마이그레이션합니다.

   ```bash
   python src/manage.py migrate
   ```

5. **관리자 계정 생성 (선택 사항)**:
   Django 관리자 페이지에 접근하기 위한 슈퍼유저 계정을 생성합니다.

   ```bash
   python src/manage.py createsuperuser
   ```

6. **환경 변수 설정**:
   프로젝트의 설정 파일은 `src/config/settings/base.py`에 정의되어 있으며, 민감한 정보(예: `SECRET_KEY`, 데이터베이스 자격 증명)는 환경 변수를 통해 관리하는 것이 좋습니다. `.env` 파일을 생성하여 환경 변수를 설정할 수
   있습니다.

   프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가합니다. (예시)

   ```
   SECRET_KEY='your_secret_key_here'
   DEBUG=True
   DATABASE_URL='sqlite:///db.sqlite3'
   ```

   **참고**: 실제 운영 환경에서는 `DEBUG`를 `False`로 설정하고, 강력한 `SECRET_KEY`를 사용하며, 적절한 데이터베이스 URL을 구성해야 합니다.

7. **개발 서버 실행**:
   설치가 완료되면 Django 개발 서버를 실행하여 제품이 올바르게 작동하는지 확인할 수 있습니다.

   ```bash
   python src/manage.py runserver
   ```

   서버가 성공적으로 시작되면 웹 브라우저에서 `http://127.0.0.1:8000/`에 접속하여 API 엔드포인트에 접근할 수 있습니다.

---

## 3.3 Distribution Environment (배포 환경)

### 3.3.1 Master Configuration (마스터 구성)

본 프로젝트의 산출물 마스터를 어떤 형태로 구성할 것인지를 기술한다.  
외적인 구성 형태 및 마스터 내부 구성 형태를 미리 고려한다.

- 예: CD 한 장 또는 두 장 구성 여부 등

### 3.3.2 Distribution Method (배포 방법)

본 프로젝트의 산출물 마스터를 어떤 방법으로 배포할 것인지를 기술한다.

- 예: CD 제공, 웹 다운로드 등

### 3.3.3 Patch/Update Method (패치와 업데이트 방법)

배포 이후, 제품 패치와 데이터나 구성 파일 업데이트 등의 업데이트 방법 및 환경을 기술한다.

---

## 3.4 Development Environment (개발 환경)

본 프로젝트의 산출물을 개발하기 위한 하드웨어 환경 정보와 소프트웨어 환경 정보를 기술한다.

### 3.4.1 Hardware Environment (하드웨어 환경)

### 3.4.2 Software Environment (소프트웨어 환경)

---

## 3.5 Test Environment (테스트 환경)

### 3.5.1 Hardware Environment (하드웨어 환경)

### 3.5.2 Software Environment (소프트웨어 환경)

---

## 3.6 Configuration Management (형상관리)

### 3.6.1 Location of Outputs (산출물 위치)

#### 3.6.1.1 Location of Source Code (소스코드 위치)

#### 3.6.1.2 Location of Documents (문서 위치)

### 3.6.2 Build Environment (빌드 환경)

### 3.6.3 Bugtrack System (버그트래킹)

### 3.6.4 Other Environment (기타 환경)
