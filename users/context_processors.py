from .models import Add_Cart

def cart_count(request):
    if request.user.is_authenticated:
        return {
            "cart_count": Add_Cart.objects.filter(user=request.user).count()
        }
    return {"cart_count": 0}
