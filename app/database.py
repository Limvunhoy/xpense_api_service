from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///xpense.db"
CONNECT_ARGS = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=CONNECT_ARGS)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session(): 
    """Dependency function to provide database session."""
    with Session(engine) as session: 
        yield session