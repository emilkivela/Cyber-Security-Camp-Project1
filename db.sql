BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "pages_account" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "balance" integer NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "pages_transaction" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "message" text NOT NULL, "amount" integer NOT NULL, "time" datetime NOT NULL, "source_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "target_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Users" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "username" text NOT NULL, "password" text NOT NULL);
COMMIT;
