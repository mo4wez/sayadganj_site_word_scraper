from peewee import Model, SqliteDatabase, CharField, PrimaryKeyField


db = SqliteDatabase()
class WordBook(Model):
    _id = PrimaryKeyField()
    full_word = CharField()
    full_word_with_symbols = CharField()
    definition = CharField()

    class Meta:
        database = db