from .models import Cart


def cart_count(request):
    if request.user.is_authenticated:
        # Filter the cart items for the logged-in user only
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        # If the user is not authenticated, set cart_count to 0 or handle as needed
        cart_count = 0

    return {'cart_count': cart_count}
