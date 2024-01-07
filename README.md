# 개요
## 주제
MyPlayList는 사용자들이 자신만의 플레이리스트를 공유할 수 있는 서비스이다.
## 기능
1. 음원 데이터를 통한 노래 검색 기능 
2. 플레이리스트 생성 기능
3. 플레이리스트에 평점을 등록하는 기능
4. 플레이리스트 즐겨찾기 기능
5. 플레이리스트 곡 목록 수정 및 삭제 기능
## 개발환경
- 호스트 언어 : Python
- DB : mysql
- OS : macOS Sonoma 14.2

# 요구사항 명세서
1. 사용자가 플레이리스트를 등록하려면 회원가입을 해야한다
2. 회원가입 정보에는 아이디, 비밀번호, 나이, 성별을 입력해야한다
3. 플레이리스트는 1개 이상의 노래를 포함해야 한다
4. 회원은 여러 노래를 등록할 수 있고, 하나의 노래는 여러 회원들로부터 등록될 수 있다
5. 플레이리스트와 회원은 회원아이디로 식별한다
6. 노래는 제목, 아티스트, 앨범명을 갖는다
7. 회원이 등록한 플레이리스트는 플레이리스트 아이디, 제목, 평점을 갖는다
8. 플레이리스트의 초기 평점 값은 0이며 한 명당 한 번의 입력이 가능하다
9. 회원은 플레이리스트에 한 번만 평점을 입력할 수 있다
10. 회원은 여러개의 플레이리스트를 즐겨찾기에 등록할 수 있다
11. 회원은 여러 플레이리스트에 여러개의 댓글을 작성할 수 있다

# ERD
<img width="834" alt="image" src="https://github.com/fjthfo/Myplaylist/assets/41682265/506fcc09-fb38-4781-ba56-bf5fe79cc9fa">

<img width="748" alt="image" src="https://github.com/fjthfo/Myplaylist/assets/41682265/26bb8630-d060-4091-bb60-96d7b1c9232f">


# 릴레이션 스키마 정보
<img width="815" alt="image" src="https://github.com/fjthfo/Myplaylist/assets/41682265/96104bce-32e5-4ba8-b8b7-09ce21aaf4f1">

<img width="815" alt="image" src="https://github.com/fjthfo/Myplaylist/assets/41682265/a1350c72-fae0-40be-a871-ef97474b16d9">


# 릴레이션 인스턴스 정보
<img width="516" alt="image" src="https://github.com/fjthfo/Myplaylist/assets/41682265/f023ad87-063b-40ca-b614-f45854b2c3c8">

<img width="697" alt="image" src="https://github.com/fjthfo/Myplaylist/assets/41682265/ef0a39cd-bea4-4912-a9de-4b4996c34962">

# 흐름도
<img width="714" alt="image" src="https://github.com/fjthfo/Myplaylist/assets/41682265/ed0f52f1-1eeb-4a25-810d-1707499f90ce">


# 서비스 시연

![1번동영상](https://github.com/fjthfo/Myplaylist/assets/41682265/7f418c14-810f-47cd-a438-7fe13788ed1e)

![2번](https://github.com/fjthfo/Myplaylist/assets/41682265/a4aed893-898f-4b37-8db6-4cc3d9774961)

![3번](https://github.com/fjthfo/Myplaylist/assets/41682265/cc42b2d4-ce16-476f-8b19-e0dcae20ea3d)

![4번](https://github.com/fjthfo/Myplaylist/assets/41682265/183eec3b-55d3-4b01-926c-ff39a74e2407)





