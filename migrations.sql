BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> f632b07fe41b

CREATE TABLE users (
    id SERIAL NOT NULL, 
    username VARCHAR NOT NULL, 
    email VARCHAR NOT NULL, 
    hashed_password VARCHAR NOT NULL, 
    is_active BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    token_version INTEGER NOT NULL, 
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE UNIQUE INDEX ix_users_username ON users (username);

CREATE TABLE categories (
    name VARCHAR(100) NOT NULL, 
    description VARCHAR(500), 
    icon_url VARCHAR(255), 
    is_active BOOLEAN NOT NULL, 
    category_id VARCHAR(36) NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    user_id INTEGER NOT NULL, 
    PRIMARY KEY (category_id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE UNIQUE INDEX ix_categories_category_id ON categories (category_id);

CREATE INDEX ix_categories_is_active ON categories (is_active);

CREATE INDEX ix_categories_name ON categories (name);

CREATE TABLE wallets (
    wallet_id VARCHAR(36) NOT NULL, 
    wallet_number VARCHAR NOT NULL, 
    wallet_name VARCHAR NOT NULL, 
    currency VARCHAR(3) NOT NULL, 
    wallet_type VARCHAR NOT NULL, 
    wallet_logo VARCHAR, 
    is_active BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    user_id INTEGER NOT NULL, 
    PRIMARY KEY (wallet_id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE INDEX ix_wallets_is_active ON wallets (is_active);

CREATE UNIQUE INDEX ix_wallets_wallet_id ON wallets (wallet_id);

CREATE UNIQUE INDEX ix_wallets_wallet_number ON wallets (wallet_number);

CREATE TABLE transactions (
    amount FLOAT NOT NULL, 
    currency VARCHAR(3) NOT NULL, 
    note VARCHAR(500), 
    transaction_date TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    is_active BOOLEAN NOT NULL, 
    transaction_id VARCHAR(36) NOT NULL, 
    transaction_no VARCHAR(12) NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    wallet_id VARCHAR NOT NULL, 
    category_id VARCHAR, 
    user_id INTEGER NOT NULL, 
    PRIMARY KEY (transaction_id), 
    FOREIGN KEY(category_id) REFERENCES categories (category_id), 
    FOREIGN KEY(user_id) REFERENCES users (id), 
    FOREIGN KEY(wallet_id) REFERENCES wallets (wallet_id)
);

CREATE INDEX ix_transactions_is_active ON transactions (is_active);

CREATE UNIQUE INDEX ix_transactions_transaction_id ON transactions (transaction_id);

CREATE UNIQUE INDEX ix_transactions_transaction_no ON transactions (transaction_no);

INSERT INTO alembic_version (version_num) VALUES ('f632b07fe41b') RETURNING alembic_version.version_num;

COMMIT;

