from pony.orm import db_session, select, count

from entities import Car, Person

#
# The db_session() decorator performs the following actions on exiting function:
#
#  - Performs rollback of transaction if the function raises an exception
#  - Commits transaction if data was changed and no exceptions occurred
#  - Returns the database connection to the connection pool
#  - Clears the database session cache
#

@db_session
def load_more_data():
    people = [
        ('John',20),
        ('Mary',22),
        ('Bob', 30),
    ]
    for name, age in people:
        person = Person(name=name, age=age)

    Car(make='Toyota', model='Prius', owner=person)


def load_more_data_with_another_way_of_using_db_session():
    people = [
        ('Juan',20),
        ('Maria',22),
        ('Bobito', 30),
    ]

    # Esta forma permite tener commits dentro de la misma función. 
    with db_session: 
        for name, age in people:
            person = Person(name=name, age=age)

        Car(make='Ferrari', model='Prius Otra vez', owner=person)
