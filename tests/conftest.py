import pytest
from app import create_app
from app import db as _db

@pytest.fixture(scope='session')
def app():
    """Session-wide test `Flask` application."""
    app = create_app('testing')
    return app

@pytest.fixture(scope='session')
def db(app):
    """Session-wide test database."""
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    """Creates a new database session for each test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
