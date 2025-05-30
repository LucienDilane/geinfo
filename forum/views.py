# forum/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import Forum
from Etudiants.models import Etudiant  # Assurez-vous d'importer Etudiant


@csrf_exempt
def forums_list_api(request):
    """
    GET: Retourne la liste de tous les forums avec leurs informations essentielles.
    """
    if request.method == 'GET':
        forums = Forum.objects.all().order_by('-date_creation')
        data = []
        for forum in forums:
            data.append({
                'id': forum.id,
                'nom': forum.nom,
                'description': forum.description,
                'date_creation': forum.date_creation.isoformat(),
                'nombre_membres': forum.nombre_membres,  # Propriété calculée
                'is_general': forum.is_general,
                'createur_id': forum.createur.id if forum.createur else None,
                'createur_nom_complet': f"{forum.createur.prenom} {forum.createur.nom}" if forum.createur else "N/A",
            })
        return JsonResponse(data, safe=False)
    # Les autres méthodes (POST) sont ignorées ici car vous ne les gérez pas
    return JsonResponse({"error": "Méthode non autorisée pour cette API."}, status=405)


@csrf_exempt
def create_forum_api(request):
    """
    POST: Crée un nouveau forum.
    Je laisse cette fonction telle quelle (ou la version précédente)
    car elle est essentielle à la création de forums.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nom = data.get('nom')
            description = data.get('description')
            createur_id = data.get('createur_id')
            is_general = data.get('is_general', False)

            if not nom:
                return JsonResponse({"error": "Le nom du forum est requis."}, status=400)

            createur = None
            if createur_id:
                try:
                    createur = Etudiant.objects.get(id=createur_id)
                except Etudiant.DoesNotExist:
                    return JsonResponse({"error": "Créateur (étudiant) non trouvé."}, status=404)

            if is_general and Forum.objects.filter(is_general=True).exists():
                return JsonResponse(
                    {"error": "Un forum général existe déjà. Un seul forum peut être marqué comme général."},
                    status=409)

            forum = Forum.objects.create(
                nom=nom,
                description=description,
                createur=createur,
                is_general=is_general
            )
            return JsonResponse({
                "message": f"Forum '{forum.nom}' créé avec succès !",
                "forum_id": forum.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erreur serveur interne: {e}"}, status=500)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


@csrf_exempt
def forum_detail_update_delete_api(request, pk):
    """
    GET: Retourne les détails d'un forum spécifique, y compris ses membres.
    PUT/DELETE: Laissé tel quel pour la fonctionnalité existante si vous la gérez.
    """
    forum = get_object_or_404(Forum, pk=pk)

    if request.method == 'GET':
        data = {
            'id': forum.id,
            'nom': forum.nom,
            'description': forum.description,
            'date_creation': forum.date_creation.isoformat(),
            'nombre_membres': forum.nombre_membres,
            'is_general': forum.is_general,
            'createur_id': forum.createur.id if forum.createur else None,
            'createur_nom_complet': f"{forum.createur.prenom} {forum.createur.nom}" if forum.createur else "N/A",
            # Inclure la liste des membres pour la vue détaillée du forum
            'membres': [{
                'id': membre.id,
                'matricule': membre.matricule,
                'nom_complet': f"{membre.prenom} {membre.nom}"
            } for membre in forum.membres.all().order_by('nom', 'prenom')]  # Ordonner les membres
        }
        return JsonResponse(data)

    elif request.method == 'PUT':
        # Je laisse la logique PUT si vous la gériez déjà.
        # Sinon, vous pouvez simplement retourner une erreur 405 ou la commenter.
        try:
            data = json.loads(request.body)
            forum.nom = data.get('nom', forum.nom)
            forum.description = data.get('description', forum.description)
            is_general = data.get('is_general', forum.is_general)

            if is_general and not forum.is_general:
                if Forum.objects.filter(is_general=True).exclude(id=forum.id).exists():
                    return JsonResponse(
                        {"error": "Un autre forum est déjà marqué comme général. Un seul forum peut être général."},
                        status=409)

            forum.is_general = is_general

            createur_id = data.get('createur_id')
            if createur_id is not None:
                if createur_id:
                    try:
                        new_createur = Etudiant.objects.get(id=createur_id)
                        forum.createur = new_createur
                    except Etudiant.DoesNotExist:
                        return JsonResponse({"error": "Nouveau créateur (étudiant) non trouvé."}, status=404)
                else:
                    forum.createur = None

            forum.save()
            return JsonResponse({"message": f"Forum '{forum.nom}' mis à jour avec succès !"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erreur serveur interne: {e}"}, status=500)


    elif request.method == 'DELETE':
        # Je laisse la logique DELETE si vous la gériez déjà.
        # Sinon, vous pouvez simplement retourner une erreur 405 ou la commenter.
        forum_nom = forum.nom
        forum.delete()
        return JsonResponse({"message": f"Forum '{forum_nom}' supprimé avec succès !"}, status=204)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

# Je retire les API spécifiques d'ajout/suppression de membres ici
# car vous avez dit que vous gérez la création d'étudiants (qui inclura l'ajout au forum général via signal)
# et si vous voulez ajouter/retirer des membres manuellement, ce serait via l'interface d'admin ou un autre point.
# Si vous aviez des vues pour forum_members_api et forum_remove_member_api, vous pouvez les laisser
# mais elles ne seront pas utilisées par le JS fourni si je retire les boutons correspondants.