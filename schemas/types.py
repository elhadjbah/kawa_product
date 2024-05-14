from ninja import ModelSchema
from products.models import Produit


class ProduitSchema(ModelSchema):
    class Meta:
        model = Produit
        fields = '__all__'


class ProduitCreate(ModelSchema):
    class Meta:
        model = Produit
        exclude = ['id']
