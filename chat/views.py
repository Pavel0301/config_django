from django.shortcuts import render




# Create your views here.
"""
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'chat/rooms.html', context={'rooms': rooms})

def room(request, slug):
    room_name = Room.objects.get(slug=slug).name
    messages = Message.objects.filter(room=Room.objects.get(slug=slug))

    context = {
        'slug': slug,
        'room_name': room_name,
        'messages': messages,
    }
    return render(request, 'chat/room.html', context=context)

"""