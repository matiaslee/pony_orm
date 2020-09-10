from pony.orm import Database, Required, Optional, Set

# Creamos una entidad Database
# Las entidades serán "creadas" y manipuladas por este objeto.
# (La magia de usar frameworks, uno no sabe bien que pasa...)

db = Database()

class Person(db.Entity):
    name = Required(str, unique=True)
    age = Required(int)
    nickname = Optional(str)
    cars = Set('Car') # Es un string xq no está declarado. Se declara recién en la siguiente clase.


class Car(db.Entity):
    make = Required(str)
    model = Required(str)
    owner = Required(Person)

#
# 1 - Conectamos el objeto `db` con la base de dato. 
# 2 - Generamos las base de datos
# Más info: https://docs.ponyorm.org/database.html
#

db.bind('sqlite', 'example.sqlite', create_db=True)  # 1
db.generate_mapping(create_tables=True)  # 2
