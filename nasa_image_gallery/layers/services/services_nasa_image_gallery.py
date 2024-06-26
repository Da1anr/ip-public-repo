# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user

#se borró la funcion getAllImages(): ya que estaba definida en transport.py

def getImagesBySearchInputLike(input):
    return 

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request del template en una NASACard.
    fav.user = '' # le seteamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.


# usados en el template 'favourites.html'
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositorio TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            nasa_card = '' # transformamos cada favorito en una NASACard, y lo almacenamos en nasa_card.
            mapped_favourites.append(nasa_card)

        return mapped_favourites


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.