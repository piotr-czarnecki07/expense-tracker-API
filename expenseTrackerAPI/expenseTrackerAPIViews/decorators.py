from functools import wraps
import json

def get_data(view):
    @wraps(view)
    def wrapper(request):
        if '_content' in request.data:
            request.data = json.loads(request.data['_content'])

        return view(request)

    return wrapper
