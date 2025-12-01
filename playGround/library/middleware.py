import time
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import time as tm
from django.shortcuts import redirect

BLOCK_IPs = ['',]
EXCEPT_URLs = ['/login/', '/admin/', '/register/', '/quotes/', '/logout/'] # Url's "públicas"

# Middleware personalizado para medir el tiempo de ejecución de una vista
class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()

        response = self.get_response(request)

        duration = time.time() - start

        print(f'tiempo de respuesta de la solicitud: {duration:.2f} seg')

        return response
    
# Middlewara para bloquear ip:
class BlockIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        print(f'Ip detectada: {ip}')

        if ip in BLOCK_IPs:
            return HttpResponseForbidden('Tu ip esta bloqueada')
        
        return self.get_response(request)
    
# Middleware para procesar solicitudes únicamente en un cierto rango horario:
class OfficeHoursOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        current_time = timezone.now().time()
        
        start_time = tm(6, 0)   # 06:00
        end_time = tm(20, 0)    # 20:00

        if  current_time < start_time or current_time > end_time:
            print(f"No se puede completar la solicitud en este horario: {current_time}")
            return HttpResponseForbidden('No se puede procesar la solicitud en el horario actual') 
        else:
            print(f"Se puede completar la solicitud en este horario: {current_time}")
        
        return self.get_response(request)
    
# Middleware para requerir login para acceder a una view:
class RequiredLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in EXCEPT_URLs):
            print('User not auth, redirigiendo...')
            return redirect('/admin/')
            

        return self.get_response(request)