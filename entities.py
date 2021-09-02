from pony.orm import Database, Required, Optional, Set

# Creamos una entidad Database
# Las entidades serán "creadas" y manipuladas por este objeto.
# (La magia de usar frameworks, uno no sabe bien que pasa...)

db = Database()

class Person(db.Entity):
    name = Required(str, unique=True)
    age = Required(int)
    nickname = Optional(str)
    cars = Set('Car') # 'Car' es el nombre de una clase que se va a definir abajo, por eso es un string.


class Car(db.Entity):
    make = Required(str)
    model = Required(str)
    owner = Required(Person)


# Configuramos la base de datos. 
# Más info: https://docs.ponyorm.org/database.html

db.bind('sqlite', 'example.sqlite', create_db=True)  # Conectamos el objeto `db` con la base de dato.
db.generate_mapping(create_tables=True)  # Generamos las base de datos.

