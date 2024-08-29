from ninja import ModelSchema, Schema
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
    nom: Optional[str] = None
    description: Optional[str] = None
    prix: Optional[float] = None
    stock: Optional[int] = None

    class Meta:
        model = Produit
        exclude = ['id']
        optional_fields = ['nom', 'description', 'prix', 'stock']


class AuthResponse(Schema):
    message: str
    userId: Optional[int] = None
    error: Optional[str] = None
