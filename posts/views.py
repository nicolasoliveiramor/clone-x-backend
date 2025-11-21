from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like, Retweet
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Count, Exists, OuterRef, Value, BooleanField
from .permissions import IsAuthorOrReadOnly
from accounts.models import Follow

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author')\
        .annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
            retweets_count=Count('retweets', distinct=True),
        )\
        .prefetch_related('comments')\
        .order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    ordering_fields = ['created_at', 'likes_count', 'comments_count', 'retweets_count']
    ordering = ['-created_at']
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['content', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = Post.objects.select_related('author').prefetch_related('comments')
        qs = qs.annotate(
            likes_count=Count('likes', distinct=True), 
            comments_count=Count('comments', distinct=True),
            retweets_count=Count('retweets', distinct=True),
        )
        user = getattr(self, 'request', None).user if hasattr(self, 'request') else None
        if user and user.is_authenticated:
            qs = qs.annotate(
                liked_by_me=Exists(
                    Like.objects.filter(post=OuterRef('pk'), user=user)
                ),
                retweeted_by_me=Exists(
                    Retweet.objects.filter(post=OuterRef('pk'), user=user)
                ),
            )
        else:
            qs = qs.annotate(
                liked_by_me=Value(False, output_field=BooleanField()),
                retweeted_by_me=Value(False, output_field=BooleanField()),
            )
        return qs.order_by('-created_at')

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def retweet(self, request, pk=None):
        post = self.get_object()
        retweet, created = Retweet.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({'message': 'Retweet realizado'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Você já retweetou este post'}, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def unretweet(self, request, pk=None):
        post = self.get_object()
        deleted, _ = Retweet.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response({'message': 'Retweet removido'}, status=status.HTTP_200_OK)
        return Response({'message': 'Você não tinha retweetado este post'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({'message': 'Post curtido'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Você já curtiu este post'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response({'message': 'Curtida removida'}, status=status.HTTP_200_OK)
        return Response({'message': 'Você não tinha curtido este post'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def comments(self, request, pk=None):
        post = self.get_object()
        if request.method == 'GET':
            qs = Comment.objects.filter(post=post).select_related('author').order_by('-created_at')
            serializer = CommentSerializer(qs, many=True, context={'request': request})
            return Response(serializer.data)
        # POST: criar comentário deste post
        content = request.data.get('content', '').strip()
        if not content:
            return Response({'content': ['Este campo é obrigatório.']}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(author=request.user, post=post, content=content)
        return Response(CommentSerializer(comment, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def feed(self, request):
        # Feed público: todos os posts, com anotações
        qs = Post.objects.select_related('author').prefetch_related('comments')
        qs = qs.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
            retweets_count=Count('retweets', distinct=True),
        )

        user = request.user
        if user.is_authenticated:
            qs = qs.annotate(
                liked_by_me=Exists(Like.objects.filter(post=OuterRef('pk'), user=user)),
                retweeted_by_me=Exists(Retweet.objects.filter(post=OuterRef('pk'), user=user)),
            )
        else:
            qs = qs.annotate(
                liked_by_me=Value(False, output_field=BooleanField()),
                retweeted_by_me=Value(False, output_field=BooleanField()),
            )

        qs = qs.order_by('-created_at')

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = PostSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get('post')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs