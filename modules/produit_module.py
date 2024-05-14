from injector import Binder, Module, singleton
from services.produit_service import ProduitService, ProduitServiceImpl


class ProduitModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ProduitService,
                    to=ProduitServiceImpl,
                    scope=singleton)
