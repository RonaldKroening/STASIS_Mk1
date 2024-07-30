import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import requests

def get_data(request, tckr):
    
    print("requesting ",request, " with "+tckr)
    return None
def your_view(request):
    print("reqreq views.py ",request)
    market_data = [
        {"Metric": "Market Cap", "Value": "0.0"},
        {"Metric": "P/E Ratio", "Value": "0.0"},
    ]

    dropdown_options = [
        {"label": "Option 1 Label", "value": "option1"},
        {"label": "Option 2 Label", "value": "option2"},
        # Add more dropdown options as needed
    ]

    context = {
        'market_data': market_data,
        'dropdown_options': dropdown_options,
        # Include other context data as needed
    }
    print("rendering in views.py from stasisproject")

    return render(request, 'stasisproject/stasisapp/templates/index.html', context)



def external_api(request):
    try:
        response = requests.get(request)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'API request failed'}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
