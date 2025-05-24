from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server_pi3.config.config import database_connection
from server_pi3.database.models import Base, Data
from server_pi3.dataclass.dataclass_models import MeasuredData
from server_pi3.my_logging.log_config import server_logger

engine = create_engine(
    database_connection,
    connect_args={'check_same_thread': False}
)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    # Create the database tables if they don't exist
    Base.metadata.create_all(bind=engine)


def store_data(data: MeasuredData):
    # Create a new session
    session = Session()

    try:
        # Create a new my_data object
        new_data = Data(
            client=data.client,
            time=data.time,
            temperature=data.temperature,
            humidity=data.humidity,
            pressure=data.pressure,
            brightness=data.brightness
        )
        session.add(new_data)

        # Commit the transaction
        session.commit()
    except Exception as e:
        # rollback the transaction in case of error
        session.rollback()
        server_logger.error(f"Error occurred while storing data: {e}")
    finally:
        # Close the session
        session.close()


def get_data(start_time, end_time):
    # Create a new session
    session = Session()

    try:
        # Query the my_data from the database
        data = (session.
                query(Data)
                .filter(Data.date.between(start_time, end_time))
                .all()
                )
    except Exception as e:
        server_logger.error(f"Error occurred while retrieving data: {e}")
        data = []
    finally:
        # Close the session
        session.close()

    return data