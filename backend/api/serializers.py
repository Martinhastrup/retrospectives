from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team, Retrospective, RetrospectiveItem, ActionItem

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'userfullname', 'role']
        read_only_fields = ['id']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'userfullname', 'role', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'userfullname', 'role']


class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members', 'created_at']
        read_only_fields = ['id', 'created_at']


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description']


class RetrospectiveItemSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = RetrospectiveItem
        fields = ['id', 'retrospective', 'category', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class ActionItemSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    
    class Meta:
        model = ActionItem
        fields = [
            'id', 'retrospective', 'title', 'description', 'assigned_to',
            'status', 'priority', 'due_date', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at']


class RetrospectiveSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    items = RetrospectiveItemSerializer(many=True, read_only=True)
    action_items = ActionItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Retrospective
        fields = [
            'id', 'title', 'description', 'team', 'created_by', 'status',
            'created_at', 'completed_at', 'items', 'action_items'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']


class RetrospectiveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retrospective
        fields = ['title', 'description', 'team']  # Added 'team' field back 