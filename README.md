# Clone X - Backend

API em Django REST Framework para um microclonador de posts com curtidas, retweets, comentários e perfis de usuário. Integra com um frontend em React/Vite e suporta autenticação baseada em sessão (cookies), CSRF, CORS e upload de imagens.

## Tecnologias
- Django 4 + Django REST Framework
- Autenticação por sessão + CSRF
- CORS configurado para frontend (Vercel e localhost)
- Upload e serviço de arquivos de mídia

## Estrutura
- `accounts/`: autenticação, perfis, follow/unfollow, endpoints públicos de usuário
- `posts/`: posts, likes, retweets, comentários, feed
- `backend/settings.py`: variáveis de ambiente, CORS/CSRF, tempo de sessão, mídia

## Requisitos
- Python 3.10+
- pip

## Como executar (dev)
1. Criar e ativar venv
   - Windows PowerShell: `python -m venv .venv` e `./.venv/Scripts/Activate.ps1`
2. Instalar dependências
   - `pip install -r requirements.txt`
3. Variáveis de ambiente (arquivo `.env` na pasta `backend`)
   - `SECRET_KEY=...`
   - `DEBUG=true`
   - `ALLOWED_HOSTS=*`
   - `FRONTEND_ORIGIN=https://clone-x-frontend-sigma.vercel.app`
   - `FRONTEND_DEV_ORIGIN=http://localhost:5173` (opcional, para desenvolvimento local)
   - `IDLE_TIMEOUT_SECONDS=1800`
   - `SESSION_COOKIE_AGE=1800`
4. Migrar banco
   - `python manage.py migrate`
5. Criar superusuário
   - `python manage.py createsuperuser`
6. Rodar servidor
   - `python manage.py runserver`

Com `DEBUG=true`, os arquivos em `MEDIA_ROOT` são servidos em `MEDIA_URL`.

## Endpoints principais
- `POST /api/auth/register/` — cadastro
- `POST /api/auth/login/` — login
- `POST /api/auth/logout/` — logout
- `GET /api/auth/profile/` — perfil autenticado
- `PATCH /api/auth/profile/` — atualizar perfil (suporta `multipart/form-data` para avatar)
- `GET /api/auth/users/` — lista de usuários
- `GET /api/auth/users/{id}/` — perfil público
- `POST/DELETE /api/auth/follow/{id}/` — seguir/desseguir

- `GET /api/posts/posts/` — lista de posts
- `GET /api/posts/posts/feed/` — feed
- `POST /api/posts/posts/` — criar post (suporta imagem)
- `GET /api/posts/posts/{id}/` — detalhe
- `POST /api/posts/posts/{id}/like/` e `DELETE /api/posts/posts/{id}/unlike/`
- `POST /api/posts/posts/{id}/retweet/` e `DELETE /api/posts/posts/{id}/unretweet/`
- `GET/POST /api/posts/posts/{id}/comments/`
- `DELETE /api/posts/comments/{comment_id}/`

## Observações de integração
- O frontend deve enviar `credentials: include` em todas as requisições.
- Antes de métodos não-GET, o frontend obtém o token CSRF em `/api/auth/csrf/` e envia `X-CSRFToken`.
- Em desenvolvimento com Vite (`localhost:5173`), mantenha `FRONTEND_DEV_ORIGIN` setado e adicionado em `CORS_ALLOWED_ORIGINS` e `CSRF_TRUSTED_ORIGINS`.

## Produção
- Ajuste `DEBUG=false` e configure serviço de mídia (Nginx/S3) conforme a plataforma.
- Use um banco robusto (PostgreSQL) e revisão de `CONN_MAX_AGE`.

## Licença
Uso educacional.