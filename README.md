# pony_orm
Un repo donde hay un Pony orm galopando por acá o por alla. 

## Comentarios previos a las clases:

1. Qué pensaba yo que era programar durante mi vida acádemica y que pienso ahora qué es programar (por si me olvide: lo de siempre + saber de frameworks + testear). 
2. Usen la documentación oficial. Siempre va a estar ahí. 
3. Un buen equipo de desarrollo es previsible. Si digo "Voy a hacer A", entonces A se hace. Si se va a ir todo al caño, avisen con tiempo, es bueno saberlo para manejar las expectativas.
4. Participen en comunidades. Mirense videos de charlas en eventos. Cuando se acabe la pandemia, busquen ampliar sus circulos sociales. 
5. Lean libros. 


## Instalación

1. Descargar el repo.
2. Entrar a la carpeta descagada
3. Crear un entorno virtual con python3.
4. Levantar el entorno virtual
5. Instalar los requerimientos

```
$ git clone https://github.com/matiaslee/pony_orm.git
$ cd pony_orm/
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Explorando el archivo `entities.py`

En el archivo `entities.py` vamos a encontrar la como se crean "entidades" (clases de python que guardan datos en una base de dato) y y la configuración de la base de datos. 

Las entidades de ese archivo están basadas en la [sección primeros pasos de la documentación de Pony](https://docs.ponyorm.org/firststeps.html)

  - Cosas feas: La versión actual no soporta migraciones. :( 

## Jugando con Pony! 

Dentro del virtual env, levantemos python y juguemos con la entidad `Person`. 

```
(venv) $ python
Python 3.6.9 (default, Jul 17 2020, 12:50:27) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from entities import Person
>>> p = Person(name='Kate', age=33)
>>> p
Person[new:1]
>>> p.name
'Kate'
```
En otra consola, hagamos un `cat` al archivo `example.sqlite`

```
$ cat example.sqlite
```

Deberíamos ver la estructura de la base de datos peeeeero ningun dato, pues los datos que escribimos todavia no fuerom "commiteados".  Commitemoslos, en la consola de python: 

```
>>> from pony.orm import commit
>>> commit()
```

Si volvemos a ejecutar `cat example.sqlite` en la otra consola deberíamos ver que no está vacia. 

## Funciones que se conectan a la base de dato. 

Veamos el archivo `some_functions.py`. 

   - `load_more_data`: carga algunos datos usando el decorador/decorator `db_session`. 
   - `load_more_data_with_another_way_of_using_db_session` usa el with statement (con `db_session`) para cargar datos. Esto permite conexiones dentro de funciones. 

Corramos las funciones
```
>>> from some_functions import *
>>> load_more_data()
>>> load_more_data_with_another_way_of_using_db_session()

```
Veamos que tenemos datos datos para acceder:
```
>>> Person.select().show()
id|name  |age|nickname
--+------+---+--------
1 |Kate  |33 |        
2 |John  |20 |        
3 |Mary  |22 |        
4 |Bob   |30 |        
5 |Juan  |20 |        
6 |Maria |22 |        
7 |Bobito|30 |        
>>> 

```

## Queries 

Las queryes se construyen usando `generadores`.  Por ejemplo 

```
>>> select(p for p in Person if p.age > 20)
<pony.orm.core.Query at 0x105e74d10>
```

El resultado es un objeto `Query` que nos dice mucho. Podermos usar el método `show` para ver mejor esto:

```
>>> select(p for p in Person if p.age > 20).show()
id|name  |age|nickname
--+------+---+--------
2 |Mary  |22 |
3 |Bob   |30 |
5 |Maria |22 |
6 |Bobito|30 | 
```

Podemos ver que query de sql se realiza si activamos el modo debug: 

```
>>> from pony.orm import set_sql_debug
>>> set_sql_debug(True)

>>> select(p for p in Person if p.age > 20).show()
SELECT "p"."id", "p"."name", "p"."age", "p"."nickname"
FROM "Person" "p"
WHERE "p"."age" > 20

id|name  |age|nickname
--+------+---+--------
2 |Mary  |22 |        
3 |Bob   |30 |        
5 |Maria |22 |        
6 |Bobito|30 |        

>>> set_sql_debug(False)
>>>
```

Dada una consulta, podemos devolver una lista con
  - todos los objetos, 
  - solo los primeros N objetos, 
  - pero no podemos tomar los últimos N objetos

Por ejemplo: 

```
>>> select(p for p in Person if p.age > 20)[:]
[Person[2], Person[3], Person[5], Person[6]]
>>> select(p for p in Person if p.age > 20)[:3]
[Person[2], Person[3], Person[5]]
>>> select(p for p in Person if p.age > 20)[-2:]
Traceback (most recent call last):
... 
TypeError: Parameter 'start' of slice object cannot be negative
```

En vez de construir una lista con entidades se puede construir una lista con atributos de las entidads:

```
>>> select(p.name for p in Person if p.age != 30)[:]
['John', 'Mary', 'Juan', 'Maria']
```

Se pueden devolver tb listas mas complejas

```
>>> from pony.orm import count
>>> select((p, count(p.cars)) for p in Person)[:3]
[(Person[1], 0), (Person[2], 0), (Person[3], 1),]
```

##  Manipulando entidades:

Obtener un objeto directamente por su id: 

```
>>> Person[1]   # Tenemos el objeto
Person[1]
>>> Person[1].name  # Lo podemos acceder directamente
'John'
>>> Person[100]  # el id no existe, error. 
Traceback (most recent call last):
...
pony.orm.core.ObjectNotFound: Person[100]
```

Con el método `get` sobre una entidad podemos buscar por atributo. Si existe más de una entidad que satisface el criterio habrá un error. Si no existe estidad la función no devulve nada:

```
>>> Person.get(name='Mary')  # Solo existe una Maria
Person[2]
>>> Person.get(age=30)  # Hay más de una persona con 30 años. 
Traceback (most recent call last):
...
pony.orm.core.MultipleObjectsFoundError: Multiple objects were found. Use Person.select(...) to retrieve them

>>> Person.get(name='Chun')  # Chun no existis. 
>>>
```

Los entidades pueden ser asignadas a variables, manipuladas modificadas y luego guardadas en la base de datos.

```
>>> mary = Person.get(name='Mary')
>>> mary.age
22
>>> mary.age = 100
>>> commit()
```

(También expresiones lambdas) 


##  Relaciones

```
class Alumno(db.Entity):
    nota_evaluacion = Set('NotaEvaluacion')

class NotaEvaluacion(db.Entity):
    alumno = Required(Alumno)
    nota = Required(int)
```

 - Declaración explicita: ambos objetos tiene que establecer la relación
 - Tres tipos de relación one-to-one, one-to-many y many-to-many. 

### One-to-one

Ejemplos: 

- "Una persana puede tener un pasaporte y ningun pasaporte es compartido por dos personas"


```

class Person(db.Entity):
    passport = Optional("Passport") # "puede tener pasaporte" es optativo. 
    ...

class Passport(db.Entity):
    person = Required("Person") # Un pasaporte no puede existir sin una persona
    ...

```
 
- "Toda persona tiene un DNI y ningún DNI es compartido por dos personas"


```

class Person(db.Entity):
    passport = Required("Passport") # "puede tener pasaporte" es optativo. 
    ...


class Dni(db.Entity):
    person = Required("Person") # Un pasaporte no puede existir sin una persona
    ...

```
 
 

```
class Order(db.Entity):
    items = Set("OrderItem")

class OrderItem(db.Entity):
    order = Optional(Order) 
 
```

### one-to-many

El ejemplo que vimos: "Los alumnos tienen notas"

```
class Alumno(db.Entity):
    nota_evaluacion = Set('NotaEvaluacion')

class NotaEvaluacion(db.Entity):
    alumno = Required(Alumno)
    nota = Required(int)
```


### many-to-many

```
class Materia(db.Entity):
    nombre = Required(str)
    profesores = Set("Profesor")
  

class Profesor(db.Entity):
    nombre = Required(str)
    materias = Set(Materia)
```

### Jugando con las relaciones! 

La última relacion está en el archivo relations.py. Carguemolo.

Vamos a crear un profesor y una materia con ese profesor. 

```
>>> from relations import *
>>> matias = Profesor(nombre='Matias')
>>> matias.materias.select().show()
id|nombre
--+------

>>> ingenieria = Materia(nombre="Ingenieria", profesores=[matias])
>>> matias.materias.select().show()
id|nombre
--+------
2 |Ingenieria 
```

Vamos a crear ahora a una profesora  y agregarla como docente de la materia que creamos. 

```
>>> laura = Profesor(nombre='Laura')
>>> ingenieria.profesores.select().show()
id|nombre
--+------
1 |Matias

>>> ingenieria.profesores.add(laura)
>>> ingenieria.profesores.select().show()
id|nombre
--+------
1 |Matias
2 |Laura 
```

Como el primer profesor estaba flojo de papeles, lo sacaron de la materia. 

```
>>> ingenieria.profesores.remove(matias)
>>> ingenieria.profesores.select().show()

id|nombre
--+------
2 |Laura 
>>> commit()
```

La función `show`, te muestra las relaciones "to-one":

```
>>> Car.select().show()
id|make   |model         |owner    
--+-------+--------------+---------
1 |Toyota |Prius         |Person[4]
2 |Ferrari|Prius Otra vez|Person[7]

```

Pero no te muestra las relaciones "to many": 

```
>>> Person.select().show()
id|name  |age|nickname
--+------+---+--------
1 |Kate  |33 |        
2 |John  |20 |        
3 |Mary  |22 |        
4 |Bob   |30 |        
5 |Juan  |20 |        
6 |Maria |22 |        
7 |Bobito|30 |        
```

Podemos hacer queries de objetos en función de atributos de low objetos a los que se relaciona. Por ejemplo, podemos seleccionar los autos con dueños mayores a 25 años:

```
>>> select(car for car in Car if car.owner.age > 25).show()
id|make   |model         |owner    
--+-------+--------------+---------
1 |Toyota |Prius         |Person[4]
2 |Ferrari|Prius Otra vez|Person[7]

```

O seleccionar directamente objectos de la relacion, por ejemplo, los dueños de autos mayores a 30:

```
select(car.owner for car in Car if car.owner.age > 30).show()
```



Fin! 

## Agregaciones!

Se pueden realizar otras operaciones como contar, sumar, sacar el máximo, mínimo, promedio y agrupar en funcion de condiciones para despues volver a operar. Vean esta [sección](https://docs.ponyorm.org/aggregations.html) de la documentación. 

