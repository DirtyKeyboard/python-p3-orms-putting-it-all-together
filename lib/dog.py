import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS dogs(
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
        )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
        DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)

    def save(self):
        sql = """
        INSERT INTO dogs(name, breed)
        VALUES (?, ?)
        """
        if self.id == None:
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        try:
            dog = cls(row[1], row[2])
            dog.id = row[0]
            return dog
        except:
            return None
    
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    
    @classmethod
    def find_by_name(cls, name):
        sql ="SELECT * FROM dogs WHERE name = ? LIMIT 1"
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ? LIMIT 1"
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed): 
        current = CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,)).fetchone()
        #conv = [cls.new_from_db(row) for row in current]
        if (current == None):
            newDog = Dog(name, breed)
            newDog.save()
            return newDog
        else:
            return [cls.new_from_db(row) for row in current]

    def update(self):
        # UPDATE table_name
        # SET column1 = value1, column2 = value2, ...
        # WHERE condition;
        sql = """
        UPDATE dogs
        SET name = ?, breed = ?
        WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))