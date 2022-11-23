import pymysql
import pprint

cnxn = pymysql.connect(host='localhost', user='root', password='1234',
                       db='myplaylistdb', charset='utf8')  # 한글처리 (charset = 'utf8')

# STEP 3: Connection 으로부터 Cursor 생성
cursor = cnxn.cursor()

# STEP 4: SQL문 실행 및 Fetch
sql = "SELECT track_name, artist_name FROM Song"
cursor.execute(sql)

# 데이타 Fetch
# rows = cursor.fetchall()
# pprint.pprint(rows)     # 전체 rows

# STEP 5: DB 연결 종료
# cnxn.close()


def mainpage():
    print('1.로그인')
    print('2.회원가입')
    return int(input())


def signup():
    print('----------------회원가입페이지----------------')
    id = input("id : ")
    password = input("password : ")
    name = input("이름 : ")
    age = int(input("나이 : "))
    gender = input("성별 : ")

    cursor.execute("INSERT INTO `user` (`id`, `password`, `name`, `age`, `gender`) VALUES ('%s', '%s', '%s', '%d', '%s')" % (
        id, password, name, age, gender))
    cnxn.commit()


def login():
    print('----------------로그인페이지----------------')
    id = input("ID : ")
    password = input("password : ")
    cursor.execute(
        "SELECT id, password FROM user WHERE id = '%s' AND password = '%s'" % (id, password))
    row = cursor.fetchall()
    if len(row) == 0:
        print('존재하지 않는 아이디거나 비밀번호가 맞지 않습니다')
        return id, 0
    elif row[0][1] == password:
        print('%s님 환영합니다.' % (row[0][0]))
        return id, 1


def make_playlist():
    cursor.execute(
        "SELECT title FROM playlist WHERE user_id = '%s'" % (Uid))
    row = cursor.fetchall()
    print(row)

    title = input('플레이리스트의 이름을 입력하세요: ')
    description = input('플레이리스트 설명을 입력하세요: ')


def add_song(row):
    select = int(input('추가할 노래번호 선택:'))
    if len(row) < 1:
        print('존재하지 않는 번호입니다.다시 입력해주세요')
    else:
        cursor.execute(
            "INSERT INTO `playlist` (`User_Id`, `Song_track_id`) VALUES ('%s', '%s')" % (Uid, row[select-1][2]))
        cnxn.commit()
        print('%s - %s (이)가 추가되었습니다' % (row[select-1][0], row[select-1][1]))


def add_playlist():
    a = 0
    print('-------------------------------------------- 노래목록 --------------------------------------------')
    cursor.execute("SELECT track_name, artist_name, track_id FROM song")
    row = cursor.fetchall()
    for i, j, k in row[:500]:
        a += 1
        print('%d\t%-65s%s' % (a, i, j))
        # todo 페이지로 분할

    add_song(row)


def search_song():
    print('----------------노래검색페이지----------------')
    word = input("검색창 : ")
    cursor.execute(
        "SELECT DISTINCT * FROM (SELECT a.track_name, a.artist_name, a.track_id, GROUP_CONCAT(' ',b.genre) AS genres FROM song a LEFT JOIN genres b ON a.track_id = b.Song_track_id GROUP BY a.track_id) AS a WHERE a.track_name LIKE '%%%s%%' OR a.artist_name LIKE '%%%s%%' ORDER BY a.artist_name" % (word, word))
    row = cursor.fetchall()
    a = 0
    print('%-20s\t%-50s%-30s\t%s' % ('번호', '제목', '가수', '장르'))
    for i, j, k, r in row:
        a += 1
        print('%d\t%-65s%-25s\t%s' % (a, i, j, r))

    add_song(row)


def menu():
    print('----------------메뉴----------------')
    print('1.플레이리스트추가')
    print('2.노래검색')
    print('3.플레이리스트 등록')
    return int(input())


while True:
    mainpage_num = mainpage()
    if mainpage_num == 2:
        signup()
        Uid, login_num = login()
    elif mainpage_num == 1:
        Uid, login_num = login()
    else:
        print('잘못 입력하셨습니다')
    if login_num == 1:
        break

while True:
    menu_num = menu()
    if menu_num == 1:
        add_playlist()
    elif menu_num == 2:
        search_song()
    elif menu_num == 3:
        make_playlist()
    break