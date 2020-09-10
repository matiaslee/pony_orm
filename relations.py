from pony.orm import Database, Required, Optional, Set

db = Database()

class Materia(db.Entity):
    nombre = Required(str)
    profesores = Set("Profesor")
  

class Profesor(db.Entity):
    nombre = Required(str)
    materias = Set(Materia)

db.bind('sqlite', 'example_relations.sqlite', create_db=True)
db.generate_mapping(create_tables=True)  

