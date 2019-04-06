import db_connection

def contents_insert(db,cursor,index_n,transactions):
    print(transactions)
    for i in range(len(transactions)):
        sql = "INSERT INTO CONTENTS (index_n, user_id, title, main) VALUES ('"+ str(index_n) +"','"+ transactions[i]['user_id'] +"','"+ transactions[i]['contents_title'] +"','"+ transactions[i]['contents_main'] +"')"
        cursor.execute(sql)
    db.commit()
    
def view_insert(db,cursor,index_n,timestamp,proof,previous_hash,merkle_root):
    print(index_n,timestamp,proof,previous_hash,merkle_root)
    print(type(merkle_root))
    sql = "INSERT INTO VIEW (index_n,time_stamp,proof,previous_hash,merkle_root_hash) VALUES ('"+str(index_n)+"','"+str(timestamp)+"','"+str(proof)+"','"+previous_hash+"','"+merkle_root+"')"
    cursor.execute(sql)
    db.commit()