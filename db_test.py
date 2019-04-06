import db_connection

def contents_insert(cursor,index_n,u_id,title,main):
    sql = "INSERT INTO CONTENTS (index_n, user_id, title, main) VALUE ("+ str(index_n) +","+ u_id +","+ title +","+ main +")"
    cursor.execute(sql)
    

cursor = db_connection.db_init()
sql ="SELECT * FROM CONTENTS"
n = cursor.execute(sql)
result = cursor.fetchall()
print(result)