from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    email = Column(String)
    password = Column(String)
    balance = Column(Integer)
    adminrights = Column(Integer)

    def __init__(self, username, email, password, balance, adminrights):
        self.username = username
        self.email = email
        self.password = password
        self.balance = balance
        self.adminrights = adminrights

# Define a function to add a user
def add_user(username, email, password, balance, adminrights):
    engine = create_engine("sqlite:///users.db", echo=True)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    person = User(username, email, password, balance, adminrights)
    session.add(person)
    session.commit()

def user_exists(username):
	engine = create_engine("sqlite:///users.db", echo=True)
	Base.metadata.create_all(bind=engine)
	
	Session = sessionmaker(bind=engine)
	session = Session()
    # Query the database to check if a user with the given email exists
	results = session.query(User).filter(User.username == username).first()
	# If a user with the same email is found, return True; otherwise, return False
	return results is not None

def check_password(username, password):
    # Create an SQLAlchemy engine and session
    engine = create_engine("sqlite:///users.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query the database for the user by username
    user = session.query(User).filter(User.username == username).first()

    # Check if the user exists and the provided password matches
    print(user.username, username)
    print(user.password, password)
    if user.password == password:
        return True
    else:
        return False

def get_balance(username):
    # Create an SQLAlchemy engine and session
    engine = create_engine("sqlite:///users.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query the database for the user by username
    user = session.query(User).filter(User.username == username).first()

    # Check if the user exists and the provided password matches
    return user.balance