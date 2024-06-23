# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.transport import transport
from .layers.generic import mapper
from django.core.paginator import Paginator
from django.shortcuts import render


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
    search_msg = request.POST.get('query', '')
    #agregar un if para que filtre cuando no hay busqueda
    if not search_msg:
        mappedImages, favourite_list = getAllImagesAndFavouriteList("space")
    else:
        mappedImages, favourite_list = getAllImagesAndFavouriteList(search_msg)
    
    paginator=Paginator(mappedImages, 8)
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    
        
    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    return render(request, 'searchResults.html', {'images': page_obj, 'favourite_list': favourite_list} )


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