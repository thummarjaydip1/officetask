from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class MyMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        print("Middleware Request:", request.path)

    def process_response(self,request,response):
        print("Middleware Response")
        return response
    
class CheckMiddleWare(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        print("process view call")
        if request.path == "/test/":
            return HttpResponse("block by middleware")
        
class TemplateMiddleWare(MiddlewareMixin):
    def process_template_response(self,request,response):
        print("template are called")
        if hasattr(response,'context_data') and response.context_data is not None:
            response.context_data['msg'] = "Template in middlware data passed"
        return response
    
class ExceptionMiddleWare(MiddlewareMixin):
    def process_exception(self,request,exception):
        print("Exception handling")
        return HttpResponse("Somthing is wrong")