## Accounts Endpoints

Base URL
- `http://localhost:8000/api/auth/`

Endpoints
- `POST /api/auth/register/` — cria usuário
- `POST /api/auth/login/` — autentica e cria sessão
- `POST /api/auth/logout/` — encerra sessão (requer autenticado)
- `GET /api/auth/profile/` — retorna perfil do usuário logado
- `PUT /api/auth/profile/` — atualiza perfil do usuário logado
- `GET /api/auth/check-auth/` — valida autenticação e retorna dados do usuário
- `POST /api/auth/follow/{user_id}/` — seguir usuário
- `DELETE /api/auth/follow/{user_id}/` — deixar de seguir usuário
- `GET /api/auth/{user_id}/followers/` — lista seguidores
- `GET /api/auth/{user_id}/following/` — lista seguindo

Exemplos rápidos (Windows cmd)

Registrar:
```bash
curl -H "Content-Type: application/json" -d "{\"email\":\"user@example.com\",\"username\":\"user1\",\"first_name\":\"Nome\",\"last_name\":\"Sobrenome\",\"password\":\"SenhaSegura123\",\"password_confirm\":\"SenhaSegura123\"}" http://localhost:8000/api/auth/register/
```

Login:
```bash
curl -H "Content-Type: application/json" -d "{\"email_or_username\":\"user1\",\"password\":\"SenhaSegura123\"}" http://localhost:8000/api/auth/login/
```

Perfil (GET):
```bash
curl -u email:senha http://localhost:8000/api/auth/profile/
```

Atualizar perfil (PUT):
```bash
curl -u email:senha -X PUT -H "Content-Type: application/json" -d "{\"bio\":\"Minha bio atualizada\"}" http://localhost:8000/api/auth/profile/
```

Seguir:
```bash
curl -u email:senha -X POST http://localhost:8000/api/auth/follow/2/
```

Deixar de seguir:
```bash
curl -u email:senha -X DELETE http://localhost:8000/api/auth/follow/2/
```

Seguidores:
```bash
curl -u email:senha http://localhost:8000/api/auth/2/followers/
```

Seguindo:
```bash
curl -u email:senha http://localhost:8000/api/auth/2/following/
```

## Notas

Payloads esperados
- Registro: `email`, `username`, `first_name`, `last_name`, `password`, `password_confirm`
- Login: `email_or_username`, `password`

Status esperados
- Registro: `201 Created` ao sucesso; `400 Bad Request` validações
- Login: `200 OK` ao sucesso; `400 Bad Request` credenciais inválidas
- Perfil: `200 OK`; `PUT` retorna `200 OK` com dados atualizados
- Follow/Unfollow: `201 Created` ao seguir; `200 OK` já seguindo/removido; `404 Not Found` se não existia
- Logout: `200 OK` ao sucesso

Sessão vs Basic Auth
- Sessão: no login, salve cookies e use nos próximos requests
```bash
curl -H "Content-Type: application/json" -c cookies.txt -d "{\"email_or_username\":\"user1\",\"password\":\"SenhaSegura123\"}" http://localhost:8000/api/auth/login/
```
- Em seguida, use:
```bash
curl -b cookies.txt http://localhost:8000/api/auth/profile/
```
- Alternativa: use Basic Auth (`-u email:senha`) em endpoints protegidos.

Dica de shell
- Windows cmd: escape aspas do JSON como nos exemplos acima.
- PowerShell/Git Bash: pode usar aspas simples no JSON, por exemplo:
```bash
curl -H "Content-Type: application/json" -d '{"email_or_username":"user1","password":"SenhaSegura123"}' http://localhost:8000/api/auth/login/
```

Logout:
```bash
curl -u email:senha -X POST http://localhost:8000/api/auth/logout/
```