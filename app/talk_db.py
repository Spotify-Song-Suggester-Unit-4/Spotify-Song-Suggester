import sqlite3
import re

def retrieve_recs(input_id):
    conn = sqlite3.connect('kn5_ids.sqlite3')
    curs = conn.cursor()
    
    select_rec_ids = '''
        SELECT kn5_ids
        FROM song_results
        WHERE id =  \'{}\'
    '''.format(input_id)
    
    q_result = curs.execute(select_rec_ids).fetchall()
    conn.close()

    result_str = re.sub('[\[\]\' ]', '', q_result[0][0])
    result_list = result_str.split(',')

    return result_list