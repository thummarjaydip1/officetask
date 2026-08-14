from django.http import JsonResponse

# fuction base middleware
def set_request_data(get_response):
    def wrapper(request):
        print("middleware function run")
        response = get_response(request)
        return response
    return wrapper


def check_even(get_respocse):
    print("check even middleware")
    def wrapper(request):
        print("start check")
        number = request.POST.get("number")
        if number and int(number) % 2:
            return JsonResponse({"message" : 'failed from the middleware'})
        response = get_respocse(request)
        print("end check")
        return response
    return wrapper

class SetRequestData:
    def __init__(self, get_response):
        print("initialization call")
        self.get_response = get_response

    def __call__(self, request):
        print(f"post data = {request.POST}")
        data = request.POST.get("number")
        print(data)
        print("start of request data")
        response = self.get_response(request)
        print("end of request data")
        return response