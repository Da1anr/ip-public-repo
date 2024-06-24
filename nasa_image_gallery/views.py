# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.transport import transport
from .layers.generic import mapper
from googletrans import Translator


# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(query):

    images = transport.getAllImages(query) #en formato json
    mappedImages = [] #lista de objetos de nasacards
    for image in images:
        mappedImages.append(mapper.fromRequestIntoNASACard(image))
    favourite_list = []

    return mappedImages, favourite_list

# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló es opcional de favoritos; caso contrario, será un listado vacío [].
    predeterminado="space"

    mappedImages, favourite_list = getAllImagesAndFavouriteList(predeterminado)
    return render(request, 'home.html', {'images': mappedImages, 'favourite_list': favourite_list} )

    
# función utilizada en el buscador..
def search(request):
    translator = Translator()
    search_msg = request.POST.get('query', '')
    #agregar un if para que filtre cuando no hay busqueda
    if search_msg:
        try:
            translated_search_msg = translator.translate(search_msg, src = "es", dest='en').text # Momentaneamente el source en español, traducción al inglés.
        except Exception as e:
            print(f"Error translating search query: {e}") 
            translated_search_msg = search_msg    # Si no puede traducir, lo devuelve al mensaje original.
        mappedImages, favourite_list = getAllImagesAndFavouriteList(translated_search_msg)
    else:
        mappedImages, favourite_list = getAllImagesAndFavouriteList("space")

    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    return render(request, 'searchResults.html', {'images': mappedImages, 'favourite_list': favourite_list} )


# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    pass


@login_required
def deleteFavourite(request):
    pass


@login_required
def exit(request):
    pass