SELECT * FROM users WHERE updated_at = '1969-1-1';
UPDATE users
SET updated_at = '1969-1-1'
WHERE EXISTS (
  SELECT 1
  FROM users_metadata
  WHERE users_metadata.username = users.username
  AND users_metadata.commits = 0
);

SELECT * FROM users
WHERE NOT EXISTS (
  SELECT 1
  FROM users_metadata
  WHERE users_metadata.username = users.username
)
AND users.is_outlaw <> TRUE;

UPDATE users
SET updated_at = '1969-1-1'
WHERE NOT EXISTS (
  SELECT 1
  FROM users_metadata
  WHERE users_metadata.username = users.username
)
AND users.is_outlaw <> TRUE;


