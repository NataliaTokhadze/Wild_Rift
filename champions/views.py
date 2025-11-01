from django.http import JsonResponse
from champions.models import Champion
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


@csrf_exempt
def search_champions(request):
    query = request.GET.get("q", "")
    champions = Champion.objects.filter(name__icontains=query)[:10]  # максимум 10 результатов
    results = []

    for champ in champions:
        results.append({
            "id": champ.id,
            "name": champ.name,
            "role": champ.role,
            "strong_against": [c.name for c in champ.strong_against.all()],
            "weak_against": [c.name for c in champ.weak_against.all()],
        })

    return JsonResponse(results, safe=False)

def champion_search_page(request):
    return render(request, "champions/search.html")
