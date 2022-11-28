# cursor.execute(
#     "SELECT distinct a.user_id, a.title, b.playlist_id FROM playlist a INNER JOIN bookmark b ON a.playlist_id = b.playlist_id")
# row = cursor.fetchall()

#  print('%-10s\t%-20s%-30s' % ('번호', '작성자', '제목'))
#   a = 0
#    for i, j, k in row:
#         a += 1
#         print('%-10d\t%-20s%-30s' % (a, i, j))

#     select = int(input('조회하고 싶은 플레이리스트의 번호를 입력: '))
#     Pid = row[select-1][2]

#     cursor.execute(
#         "SELECT DISTINCT `track_name`, `artist_name`, `genres`, `track_id` FROM (SELECT a.track_name, a.artist_name, a.track_id, GROUP_CONCAT(b.genre) AS genres FROM song a INNER JOIN genres b ON a.track_id = b.track_id GROUP BY a.track_id) c where track_id IN( SELECT track_id from track where playlist_id = '%s')" % (Pid))
#     row = cursor.fetchall()
#     print(row)
#     print('%-20s\t%-50s%-30s\t%s' % ('번호', '제목', '가수', '장르'))
#     a = 0
#     for i, j, k, r in row:
#         a += 1
#         print('%d\t%-65s%-25s\t%s' % (a, i, j, k))

#     cursor.execute(
#         "SELECT user_id, body FROM comment where playlist_id = '%s'" % (Pid))
#     row2 = cursor.fetchall()
#     if len(row2) > 0:
#         for i in range(len(row2)):
#             print(' ㄴ %s : %s' % (row2[i][0], row2[i][1]))
