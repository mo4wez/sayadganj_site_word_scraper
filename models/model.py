from peewee import Model, SqliteDatabase, CharField, PrimaryKeyField, ForeignKeyField


db = SqliteDatabase('word_book.db')

class WordBook(Model):
    full_word = CharField()
    full_word_with_symbols = CharField()
    definition = CharField()

    class Meta:
        database = db

# class SimilarWord(Model):
#     main_word = ForeignKeyField(model=WordBook, backref="similar_words", on_delete="CASCADE")
#     similar_title = CharField()

#     class Meta:
#         database = db


if not WordBook.table_exists():
    db.create_tables([WordBook])
