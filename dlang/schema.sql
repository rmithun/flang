DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comments TEXT NOT NULL,
    is_foul BOOLEAN DEFAULT TRUE,
    moderated BOOLEAN DEFAULT FALSE
);