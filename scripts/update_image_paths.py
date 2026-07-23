#!/usr/bin/env python3
import os
import json
import pymysql
import sys

# Load data
with open('/tmp/photos.json') as f:
    photos_data = json.load(f)
with open('/tmp/spots.json') as f:
    spots_data = json.load(f)

qg_id_to_name = {s['id']: s['name'] for s in spots_data}

# Connect to MySQL (internal docker network)
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = int(os.environ.get('DB_PORT', '3306'))
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'your_password')
DB_NAME = os.environ.get('DB_NAME', 'getaway_plan')

conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8mb4')
cur = conn.cursor()

cur.execute('SELECT sn.id, sn.author, s.name FROM social_notes sn JOIN spots s ON sn.spot_id = s.id')
notes = cur.fetchall()
note_map = {}
for nid, author, spot_name in notes:
    note_map.setdefault(f'{spot_name}|{author}', []).append(nid)

updated = 0
for spot_qg_id, spot_data in photos_data.items():
    spot_name = qg_id_to_name.get(spot_qg_id, spot_qg_id)
    for group in spot_data.get('groups', []):
        photos = group.get('photos', [])
        if not photos:
            continue
        author = group.get('author', '')
        note_ids = note_map.get(f'{spot_name}|{author}', [])
        for nid in note_ids:
            cur.execute('SELECT id, sort_order, local_path FROM social_images WHERE note_id=%s ORDER BY sort_order', (nid,))
            for img_id, so, ex in cur.fetchall():
                if so < len(photos) and not ex:
                    cur.execute('UPDATE social_images SET local_path=%s WHERE id=%s', (photos[so], img_id))
                    updated += 1

conn.commit()
cur.close()
conn.close()
print(f'Success: {updated} images updated')
