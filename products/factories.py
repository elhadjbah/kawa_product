import factory
import faker_commerce
from products.models import Produit

factory.faker.Faker.add_provider(faker_commerce.Provider)


class ProduitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Produit

    nom = factory.faker.Faker('uuid4')
    description = factory.faker.Faker('sentence', nb_words=25)
    prix = factory.faker.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    stock = factory.faker.Faker('random_int', min=0, max=150)
