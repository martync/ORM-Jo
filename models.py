from peewee import *

db = SqliteDatabase("herboristerie.db")


class BaseModel(Model):
    name = CharField()

    def __str__(self):
        return self.name

    class Meta:
        database = db


class PartieUtilisee(BaseModel):
    @staticmethod
    def get_updatable_fields():
        return ["name"]

    def update_table(field, instance_id, update):
        if field == "N":
            PartieUtilisee.update(name=update).where(PartieUtilisee.id == instance_id).execute()
            return True
        else:
            return False

    class Meta:
        table_name = "partie_utilisée_plantes"


class IndicationPlante(BaseModel):
    @staticmethod
    def get_updatable_fields():
        return ["name"]

    def update_table(field, instance_id, update):
        if field == "N":
            IndicationPlante.update(name=update).where(IndicationPlante.id == instance_id).execute()
            return True
        else:
            return False

    class Meta:
        table_name = "indications_plantes"


class SousClasse(BaseModel):
    name_french = CharField()

    @staticmethod
    def get_updatable_fields():
        return ["name", "name_french"]

    class Meta:
        table_name = "sous_classes"


class Famille(BaseModel):
    sous_classe = ForeignKeyField(SousClasse, column_name="id_sous_classe")
    name_french = CharField()

    @staticmethod
    def get_updatable_fields():
        return ["name", "name_french"]

    class Meta:
        table_name = "familles_plantes"


class Plante(BaseModel):
    price = DecimalField(30, 2)
    famille = ForeignKeyField(Famille, column_name="id_famille")
    id_indication = ForeignKeyField(IndicationPlante, column_name="id_indication")
    id_used_part = ForeignKeyField(PartieUtilisee, column_name="id_used_part")

    @staticmethod
    def get_updatable_fields():
        # Permettre la mise à jour de champs ForeignKey est un peu plus
        # velu (si on veut proposer quelque chose de user-friendly).
        # Cependant, on peut le permettre, à condition que l'utilisateur saisisse l'id
        # de l'objet en relation.
        return ["name", "price"]

    class Meta:
        table_name = "plante"


db.create_tables([Plante, Famille, SousClasse, IndicationPlante, PartieUtilisee])


partie_utilisee = PartieUtilisee.create(name="Feuille")
indication = IndicationPlante.create(name="Digestion")
sousclasse = SousClasse.create(name="Subclassae", name_french="Subclassae")
famille = Famille.create(sous_classe=sousclasse, name="Famillace", name_french="Famillace")
plante = Plante.create(name="Menthe", price=9, famille=famille, id_indication=indication, id_used_part=partie_utilisee)
plante = Plante.create(name="Laurier", price=8, famille=famille, id_indication=indication, id_used_part=partie_utilisee)
