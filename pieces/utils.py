from pieces.models import UserQueue


def reorder_queue():
    for index, user_queue in enumerate(UserQueue.objects.all().order_by('position')):
        user_queue.position = index + 1
        user_queue.save()