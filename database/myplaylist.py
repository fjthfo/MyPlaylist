import pymysql
import pprint
import time as t
from tabulate import tabulate
import pandas as pd
tabulate.WIDE_CHARS_MODE = False

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


def SongList():  # * 1번
    print('-------------------------------------------- 노래목록 --------------------------------------------')
    cursor.execute("SELECT track_name, artist_name, track_id FROM song")
    row = cursor.fetchall()
    # print(tabulate(row, headers=['노래', '가수', '장르'],
    #       tablefmt='plain', stralign='left', showindex=True))
    count = 50
    song_page(row, count)
    while True:
        select = input('이전페이지[<] | 다음페이지 [>] | 뒤로가기[b] | 추가할 노래번호 입력\n')
        if select == '>':
            count += 50
            song_page(row, count)
        elif select == '<':
            count -= 50
            song_page(row, count)
        elif select == 'b':
            break
        else:
            add_song(row, int(select))
    menu()


def song_page(row, count):
    num = count-50
    for i, j, k in row[num:count]:
        num += 1
        print('%d\t%-65s%s' % (num, i, j))


def search_song():  # * 2번
    print('----------------노래검색페이지----------------')
    word = input("가수 또는 노래 검색 : ")
    cursor.execute(
        "SELECT DISTINCT * FROM (SELECT a.track_name, a.artist_name, a.track_id, GROUP_CONCAT(' ',b.genre) AS genres FROM song a LEFT JOIN genres b ON a.track_id = b.track_id GROUP BY a.track_id) AS a WHERE a.track_name LIKE '%%%s%%' OR a.artist_name LIKE '%%%s%%' ORDER BY a.artist_name" % (word, word))
    row = cursor.fetchall()
    a = 0
    print('%-20s\t%-50s%-30s\t%s' % ('번호', '제목', '가수', '장르'))
    for i, j, k, r in row:
        a += 1
        print('%d\t%-65s%-25s\t%s' % (a, i, j, r))
    add_song(row)


def edit_playlist():  # *  3번
    print('----------------플레이리스트 수정----------------')
    while True:
        row = show_myplaylist(Uid)
        select = int(input('선택한 번호의 노래 제거 | 뒤로가기(-1) | 플레이리스트삭제(-2) \n'))
        if select == -1:
            menu()
            break
        elif select == -2:
            answer = input('정말로 제거하시겠습니까? [Y/N]')
            if answer == 'y' or answer == 'Y':
                cursor.execute(
                    "DELETE FROM playlist WHERE user_id = '%s' " % (Uid))
                cnxn.commit()
                break
        else:
            cursor.execute(
                "DELETE FROM track where user_id='%s' and track_id='%s'" % (Uid, row[select-1][2]))
            cnxn.commit()
            print('%s - %s (이)가 제거되었습니다' %
                  (row[select-1][0], row[select-1][1]))
            break


def show_playlist():  # *  4번
    print('# 플레이리스트 목록')
    cursor.execute(
        "select a.title, a.user_id, round(avg(b.reco_num),1) FROM playlist a LEFT JOIN recommend b ON a.playlist_id = b.playlist_id group by a.playlist_id, a.title, a.user_id")
    row = cursor.fetchall()

    cursor.execute(
        "select playlist_id FROM playlist")
    pidrow = cursor.fetchall()
    print(row)

    print(tabulate(row, headers=['제목', '작성자', '평점'],
          tablefmt='pretty', stralign='left', showindex=True))

    # print('\t%-10s\t%-10s\t%s' % ('제목', '작성자', '별점'))
    # a = 0
    # for i, j, k, r in row:
    #     a += 1
    #     print('%d\t%-10s\t%-10s\t%s' % (a, j, k, r))

    select = int(input('조회하고 싶은 플레이리스트의 번호를 입력: '))
    Pid = pidrow[select][0]
    show_myplaylist(row[select][1])

    cursor.execute(
        "SELECT user_id, body FROM comment where playlist_id = '%s'" % (Pid))
    row2 = cursor.fetchall()
    if len(row2) > 0:
        for i in range(len(row2)):
            print(' ㄴ %s : %s' % (row2[i][0], row2[i][1]))

    choice = int(input('댓글달기 [1] | 별점매기기[2] | 즐겨찾기 추가[3] | 뒤로가기 [-1]\n'))
    if choice == 1:
        add_comment(Pid)
    elif choice == 2:
        recommend(Pid)
    elif choice == 3:
        add_bookmark(Pid, row)
    elif choice == -1:
        menu()


def add_bookmark(Pid, row):
    cursor.execute(
        "INSERT INTO `bookmark` (`playlist_id`, `user_id`) VALUES ('%s', '%s')" % (Pid, Uid))
    cnxn.commit()
    print(row)
    print('추가되었습니다')


def show_bookmark():
    print('#즐겨찾기목록')
    cursor.execute(
        "SELECT distinct b.bookmark_id, a.user_id, a.title FROM playlist a INNER JOIN bookmark b ON a.playlist_id = b.playlist_id")
    row = cursor.fetchall()
    print(tabulate(row, headers=['번호', '작성자', '제목'],
          tablefmt='pretty', stralign='left', showindex=False))


# def logout():  # *8번
#     choice = input('로그아웃 하시겠습니까? [Y/N]')
#     if choice == 'Y' or choice == 'y':
#         login_num = 0


def recommend(Pid):
    num = int(input('1~10까지의 숫자를 입력해주세요 : '))
    if num >= 1 and num <= 10:
        try:
            cursor.execute(
                "INSERT INTO `recommend` (`playlist_id`, `user_id`, `reco_num`) VALUES ('%s', '%s', '%s')" % (Pid, Uid, num))
            cnxn.commit()
        except pymysql.err.IntegrityError:
            print('이미 등록한 평점입니다.')
    else:
        print('잘못된 입력입니다')


def add_comment(Pid):
    body = input("댓글을 입력해주세요 : ")
    cursor.execute("INSERT INTO `comment` (`playlist_id`, `user_id`, `body`) VALUES ('%s', '%s', '%s')" % (
        Pid, Uid, body))
    cnxn.commit()
    print('댓글등록완료')


def add_song(row, select):
    # select = int(input('추가할 노래번호 선택:'))

    cursor.execute(
        "SELECT `title` FROM playlist WHERE user_id = '%s'" % (Uid))
    namerow = cursor.fetchall()
    if len(namerow) < 1:
        title = input('플레이리스트의 이름을 입력하세요: ')
        cursor.execute("INSERT INTO `Playlist` (`user_id`, `title`) VALUES ('%s', '%s')" % (
            Uid, title))
        cnxn.commit()

    if len(row) < 1:
        print('존재하지 않는 번호입니다.다시 입력해주세요')
    else:
        print(Uid, row[select-1][2])
        cursor.execute(
            "INSERT INTO `Track` (`user_id`, `track_id`) VALUES ('%s', '%s')" % (Uid, row[select-1][2]))
        cnxn.commit()
        print('%s - %s (이)가 추가되었습니다' %
              (row[select-1][0], row[select-1][1]))


def show_myplaylist(Uid):
    cursor.execute(
        "SELECT `playlist_id`, `title` FROM playlist WHERE user_id = '%s'" % (Uid))
    row = cursor.fetchall()
    print('---------------------------------------')
    print('플레이리스트 제목:', row[0][1])
    print('---------------------------------------')
    cursor.execute(
        "SELECT DISTINCT `track_name`, `artist_name`, `genres` FROM (SELECT a.track_name, a.artist_name, a.track_id, GROUP_CONCAT(b.genre) AS genres FROM song a INNER JOIN genres b ON a.track_id = b.track_id GROUP BY a.track_id) c where track_id IN( SELECT track_id from track where user_id = '%s')" % (Uid))
    row = cursor.fetchall()

    print(tabulate(row, headers=['노래', '가수', '장르'],
          tablefmt='plain', stralign='left', showindex=True))
    # return row


def menu():
    print('----------------메뉴----------------')
    print('1.노래 목록\t\t2.노래 검색')
    print('3.내 플레이리스트 수정\t4.플레이리스트 목록조회')
    print('5.즐겨찾기 목록')
    print('9.종료')
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
        SongList()
        t.sleep(1)
    elif menu_num == 2:
        search_song()
        t.sleep(1)
    elif menu_num == 3:
        edit_playlist()
    elif menu_num == 4:
        show_playlist()
    elif menu_num == 5:
        show_bookmark()
    elif menu_num == 9:
        print("Bye")
        break
