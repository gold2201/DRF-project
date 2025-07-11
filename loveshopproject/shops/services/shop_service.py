from rest_framework.generics import get_object_or_404

from shops.models import Shop


def purchase_product(shop, product):
    if shop.currency_amount >= product.product_price and product.product_amount > 0:
        shop.currency_amount -= product.product_price
        product.product_amount -= 1
        product.save()
        shop.save()
        return True, product.message_after_purchase
    else:
        return False, 'Not enough currency'

def check_shop_object(pk):
    shop = get_object_or_404(Shop, pk=pk)
    return shop