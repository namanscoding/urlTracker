CREATE_URLS_TABLE   = """CREATE TABLE IF NOT EXISTS urls(url text PRIMARY KEY, prevhash text, prevcontent text, timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW());"""
INSERT_URL          = "INSERT INTO urls (url, prevhash, prevcontent ,timestamp) VALUES (%s, %s, %s, NOW());"
FETCH_ALL           = "Select * from urls;"
UPDATE_HASH_TIME    = "UPDATE urls  SET prevhash=%s,prevcontent=%s, timestamp = %s WHERE  url=%s;  "
DELETE_URL          = 'DELETE FROM urls WHERE url = %s;'
CHECK_IF_EXISTS     = "SELECT * FROM urls WHERE url = '%s' ;"
