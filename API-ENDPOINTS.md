# Clone X - API Endpoints

Base URL
- `http://localhost:8000/`

Autenticação
- Endpoints protegidos exigem usuário autenticado.
- Exemplos abaixo usam Basic Auth (`-u email:senha`).

Serializers
- `PostSerializer` retorna:
  - `id`, `author`, `author_username`, `content`, `image`
  - `created_at`, `updated_at`
  - `likes_count`, `comments_count`, `retweets_count`
  - `liked_by_me`, `retweeted_by_me`

Paginação
- Resposta padrão DRF:
  - `count`, `next`, `previous`, `results: [...]`

Ordenação e Busca
- `ordering`: `created_at`, `likes_count`, `comments_count`, `retweets_count`
- `search`: por `content` e `author__username`

## Posts

Listar posts
- `GET /api/posts/posts/`
- Parâmetros:
  - `ordering`: `-created_at` | `-likes_count` | `-comments_count` | `-retweets_count`
  - `search`: termo de busca

Exemplo:

- `curl -u email:senha http://localhost:8000/api/posts/posts/?ordering=-created_at`


Detalhe do post
- `GET /api/posts/posts/{id}/`

Exemplo:

- `curl -u email:senha http://localhost:8000/api/posts/posts/1/`


Criar post
- `POST /api/posts/posts/`
- Body (JSON): `{"content":"texto","image":null}`

Exemplo GIT Bash:
- `curl -u email:senha -H "Content-Type: application/json" -d "{"content":"Olá mundo"}" http://localhost:8000/api/posts/posts/`

Exemplo Windows cmd:
- `curl -u email:senha -H "Content-Type: application/json" -d "{\"content\":\"Olá mundo\"}" http://localhost:8000/api/posts/posts/`


Atualizar post (autor)
- `PATCH /api/posts/posts/{id}/`
- Body (JSON): campos a alterar


Excluir post (autor)
- `DELETE /api/posts/posts/{id}/`

## Interações

Curtir
- `POST /api/posts/posts/{id}/like/`

Exemplo:

- `curl -u email:senha -X POST http://localhost:8000/api/posts/posts/1/like/`


Remover curtida
- `DELETE /api/posts/posts/{id}/unlike/`

Exemplo:

- `curl -u email:senha -X DELETE http://localhost:8000/api/posts/posts/1/unlike/`



Retweet
- `POST /api/posts/posts/{id}/retweet/`

Exemplo:

- `curl -u email:senha -X POST http://localhost:8000/api/posts/posts/1/retweet/`


Remover retweet
- `DELETE /api/posts/posts/{id}/unretweet/`

Exemplo:

- `curl -u email:senha -X DELETE http://localhost:8000/api/posts/posts/1/unretweet/`


Comentários
- `GET /api/posts/posts/{id}/comments/` (lista)
- `POST /api/posts/posts/{id}/comments/` (criar)
- Body (JSON): `{"content":"comentário"}`

Exemplo criação GIT bash:

- `curl -u email:senha -H "Content-Type: application/json" -d "{"content":"Show!"}" http://localhost:8000/api/posts/posts/1/comments/`

Exemplo criação Windows cmd:

- `curl -u email:senha -H "Content-Type: application/json" -d "{\"content\":\"Show!\"}" http://localhost:8000/api/posts/posts/1/comments/`

## Feed

Feed dos seguidos
- `GET /api/posts/posts/feed/`
- Retorna posts de usuários seguidos com contadores e flags.

Exemplo:

- `curl -u email:senha http://localhost:8000/api/posts/posts/feed/`

## Exemplos de Ordenação e Busca

Mais comentados:

- `curl -u email:senha http://localhost:8000/api/posts/posts/?ordering=-comments_count`


Mais retweetados:

- `curl -u email:senha http://localhost:8000/api/posts/posts/?ordering=-retweets_count`


Busca por texto:

- `curl -u email:senha http://localhost:8000/api/posts/posts/?search=feliz&ordering=-created_at`


## Observações

- Contadores e flags são otimizados via anotações de banco (`Count`, `Exists`) sem N+1.
- Para endpoints de conta e perfil, consulte os endpoints expostos pelo app `accounts` na sua configuração atual.