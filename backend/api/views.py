from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Team, Retrospective, RetrospectiveItem, ActionItem
from .serializers import (
    UserSerializer, UserCreateSerializer, TeamSerializer, TeamCreateSerializer,
    RetrospectiveSerializer, RetrospectiveCreateSerializer, RetrospectiveItemSerializer,
    ActionItemSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeamCreateSerializer
        return TeamSerializer
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            return Response({'message': 'Member added successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            return Response({'message': 'Member removed successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class RetrospectiveViewSet(viewsets.ModelViewSet):
    queryset = Retrospective.objects.all()
    serializer_class = RetrospectiveSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RetrospectiveCreateSerializer
        return RetrospectiveSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        retrospective = self.get_object()
        retrospective.status = 'completed'
        retrospective.save()
        return Response({'message': 'Retrospective completed'})
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        retrospective = self.get_object()
        retrospective.status = 'archived'
        retrospective.save()
        return Response({'message': 'Retrospective archived'})


class RetrospectiveItemViewSet(viewsets.ModelViewSet):
    queryset = RetrospectiveItem.objects.all()
    serializer_class = RetrospectiveItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ActionItemViewSet(viewsets.ModelViewSet):
    queryset = ActionItem.objects.all()
    serializer_class = ActionItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        action_item = self.get_object()
        action_item.status = 'completed'
        action_item.save()
        return Response({'message': 'Action item completed'})
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        action_item = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            action_item.assigned_to = user
            action_item.save()
            return Response({'message': 'Action item assigned successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            ) 