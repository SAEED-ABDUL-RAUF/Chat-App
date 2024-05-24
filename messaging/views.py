from django.shortcuts import render, get_object_or_404


from .models import GroupMessage, Group

# Create your views here.
def home(request):
    groups = Group.objects.all()
    context = {'groups':groups}
    return render(request, 'messaging/home.html', context)


def groupView(request, group_name):
    # group = get_object_or_404(Group, name=group_name)
    group = Group.objects.get(slug=group_name)
    context = {'group':group}
    return render(request, 'messaging/group.html', context)