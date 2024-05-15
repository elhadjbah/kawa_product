from ninja import ModelSchema
from products.models import Produit
from typing import Optional


class ProduitSchema(ModelSchema):
    class Meta:
        model = Produit
        fields = '__all__'


class ProduitCreate(ModelSchema):
    class Meta:
        model = Produit
        exclude = ['id']


class ProduitUpdate(ModelSchema):
    nom: Optional[str]
    description: Optional[str]
    prix: Optional[float]
    stock: Optional[int]

    class Meta:
        model = Produit
        exclude = ['id']
        # optional_fields = ['nom', 'description', 'prix', 'stock']
