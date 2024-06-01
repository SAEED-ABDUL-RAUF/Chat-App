from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import GroupMessage, Group, Membership

User = get_user_model()
# Create your views here.
@login_required
def home(request):
    query = request.GET['q']
    groups = Group.objects.filter(name__icontains=query)
    user_groups = Membership.objects.filter(user=request.user).values_list('group_id', flat=True)
    context = {'groups':groups, 'user_groups':user_groups}
    return render(request, 'messaging/home.html', context)

@login_required
def groupChatPage(request, group_name):
    # group = get_object_or_404(Group, name=group_name)
    group = Group.objects.get(slug=group_name)
    messages = GroupMessage.objects.filter(group=group)
    members = group.members.all()
    online_users = group.online.all()
    context = {
        'group':group, 
        'members':members, 
        'messages':messages,
        'online_users':online_users
    }
    return render(request, 'messaging/group_page.html', context)

@login_required
def joinGroup(request, pk):
    if request.method == 'POST':
        group = Group.objects.get(id=pk)
        group.members.add(request.user)
        return redirect('group-page', group.slug)
    return redirect('home')



@login_required
def groupList(request):
    user = User.objects.get(id=request.user.id)
    groups = Group.objects.filter(members=user)
    context = {'groups':groups}
    return render(request, 'messaging/group_list.html', context)