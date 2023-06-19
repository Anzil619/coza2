

from .models import Wishlist


def wishlist_counter(request):
    wishlist_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                wishlist_count = Wishlist.objects.all().filter(user=request.user).count()

        except Wishlist.DoesNotExist:
            wishlist_counter = 0
    return dict(wishlist_count=wishlist_count)


