from .models import Follow


def is_following(request, author) -> bool:
    """Checks if this author is in the user's subscriptions"""
    if Follow.objects.filter(user=request.user, author=author):
        return True
    return False


def is_empty(page) -> bool:
    """Checks if the subscription feed is empty for user"""
    if len(page.object_list) == 0:
        return True
    return False
