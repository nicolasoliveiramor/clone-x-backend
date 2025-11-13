import time
from django.conf import settings
from django.contrib.auth import logout

class IdleLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Só considera sessões autenticadas
        if request.user.is_authenticated:
            now = int(time.time())
            last = request.session.get("last_activity", now)
            timeout = getattr(settings, "IDLE_TIMEOUT_SECONDS", 3600)  # 1h por padrão

            # Se exceder o tempo de inatividade, desloga
            if now - last > timeout:
                logout(request)
                # Limpamos o last_activity para evitar reaproveitar valor antigo
                request.session.pop("last_activity", None)
            else:
                # Atualiza o timestamp a cada requisição
                request.session["last_activity"] = now

        response = self.get_response(request)
        return response