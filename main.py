from controlers import *


def main():
    while True:
        list_all_tables()

        choix_action = input("(C)réer / (A)fficher / (M)odifier / (S)upprimer : ").upper()

        if choix_action == "M":
            model_choice = input(
                "Quel tableau souhaitez-vous modifier ? (P)lante / (F)amille / (S)ous-classe / (I)ndication / Partie (U)tilisée "
            ).upper()

            # Liste des modeles disponibles à la modification
            models = {"P": Plante, "F": Famille, "S": SousClasse, "I": IndicationPlante}

            # Sélection du modèle
            model_class = models[model_choice]

            # Requête les entrées du modèle et affiche la liste précédée de l'id
            object_list = model_class.select()
            for obj in object_list:
                print(obj.id, obj)

            # Choix de l'id de l'objet à modifier
            obj_id = input("Entrez l'id de la ligne à modifier: ")

            # Sélection de l'objet à modifier
            obj = model_class.get(model_class.id == obj_id)

            # Affichage des champs modifiables (voir les méthodes `get_updatable_fields` dans models.py)
            updatable_fields = model_class.get_updatable_fields()
            field = input(
                "Quel champ souhaitez-vous modifier ? {} ".format(
                    " / ".join(["({}) {}".format(i, field) for i, field in enumerate(updatable_fields, 1)])
                )
            )

            # Saisie de la nouvelle valeur
            new_val = input("Nouvelle valeur de {} : ".format(field))

            # 👇 Ici affecte la nouvelle valeur au champ sélectionné sur l'objet, puis on sauvegarde
            setattr(obj, field, new_val)
            obj.save()

        elif choix_action == "A":
            choix_tableau = input(
                "Quel tableau souhaitez-vous afficher ? (P)lante / (F)amille / (S)ous-classe / "
                "(I)ndication / Partie (U)tilisée"
            ).upper()
            if choix_tableau == "P":
                table = Plante.select()
                for row in table:
                    print(row.id, row.name, row.price, row.id_indication, row.id_famille, row.id_used_part)
            elif choix_tableau == "F":
                table = Famille.select()
                for row in table:
                    print(row.id, row.name, row.name_french, row.id_sous_classe)
            elif choix_tableau == "S":
                table = SousClasse.select()
                for row in table:
                    print(row.id, row.name, row.name_french)
            elif choix_tableau == "I":
                table = IndicationPlante.select()
                for row in table:
                    print(row.id, row.name)
            elif choix_tableau == "U":
                table = PartieUtilisee.select()
                for row in table:
                    print(row.id, row.name)
            else:
                print("Commande non reconnue. Recommencez.")
        result = average_indication_price()
        for average_price, indication in result.tuples():
            print(indication, average_price)

        result2 = count_plants_by_family()
        for plant_count, famille in result2.tuples():
            print(famille, plant_count)

        result3 = minmax_price_by_sous_classe()
        for minprice, maxprice, sous_classe in result3.tuples():
            print(sous_classe, minprice, maxprice)

            update_table("P", "P", 9, 10)


if __name__ == "__main__":
    main()
