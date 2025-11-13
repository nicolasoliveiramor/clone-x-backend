from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    liked_by_me = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    retweeted_by_me = serializers.SerializerMethodField()
    author_profile_picture = serializers.SerializerMethodField()
    retweets_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'author_username',
            'content', 'image',
            'created_at', 'updated_at',
            'likes_count', 'comments_count',
            'retweeted_by_me', 'liked_by_me', 'retweets_count',
            'author_profile_picture',
        )
        read_only_fields = ('author', 'created_at', 'updated_at')

    def get_likes_count(self, obj):
        return getattr(obj, 'likes_count', obj.likes.count())

    def get_comments_count(self, obj):
        return getattr(obj, 'comments_count', obj.comments.count())

    def get_liked_by_me(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            annotated = getattr(obj, 'liked_by_me', None)
            if annotated is not None:
                return bool(annotated)
            return obj.likes.filter(user=user).exists()
        return False

    def get_retweets_count(self, obj):
        return getattr(obj, 'retweets_count', obj.retweets.count())

    def get_retweeted_by_me(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            annotated = getattr(obj, 'retweeted_by_me', None)
            if annotated is not None:
                return bool(annotated)
            return obj.retweets.filter(user=user).exists()
        return False

    def get_author_profile_picture(self, obj):
        pic = getattr(obj.author, 'profile_picture', None)
        if pic:
            try:
                return pic.url
            except Exception:
                return None
        return None

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'author_username', 'author_profile_picture', 'post', 'content', 'created_at')
        read_only_fields = ('author', 'created_at')

    def get_author_profile_picture(self, obj):
        pic = getattr(obj.author, 'profile_picture', None)
        if pic:
            try:
                return pic.url
            except Exception:
                return None
        return None
