from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import CityEnum, Client, Medicine, Pet, Product, Provider, Veterinary


def home(request):
    """
    Renderiza la página de inicio.
    """
    return render(request, "home.html")


def clients_repository(request):
    """
    Renderiza la lista de clientes.
    """
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})

def clients_form(request, id=None):
    """
    Renderiza el formulario de clientes y maneja la creación o actualización de clientes.
    """
    ciudades = CityEnum.choices
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = False

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            update_result = client.update_client(request.POST)
            if update_result is not None:
                saved, errors = update_result
            else:
                saved = True

        if saved:
            """print("Saved successfully! Redirecting to clients_repo...")"""
            return redirect(reverse("clients_repo"))
        else:
            """print("Error saving client! Errors:", errors"""
            return render(request, "clients/form.html", {"errors": errors, "client": request.POST, "ciudades": ciudades})

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client, "ciudades": ciudades})


def clients_delete(request):
    """
    Elimina un cliente.
    """
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))

# Proveedor
def provider_repository(request):
    """
    Renderiza la lista de proveedores.
    """
    providers = Provider.objects.all()
    return render(request, "providers/repository.html", {"providers": providers})


def provider_form(request, id=None):
    """
    Renderiza el formulario de proveedores y maneja la creación o actualización de proveedores.
    """
    if request.method == "POST":
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            saved, errors = provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("provider_repo"))

        return render(
            request, "providers/form.html", {"errors": errors, "provider": request.POST},
        )

    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "providers/form.html", {"provider": provider})


def provider_delete(request):
    """
    Elimina un proveedor.
    """
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()

    return redirect(reverse("provider_repo"))


# Producto
def product_repository(request):
    """
    Renderiza la lista de productos.
    """
    products = Product.objects.all()
    return render(request, "products/repository.html", {"products": products})


def product_form(request, id=None):
    """
    Renderiza el formulario de productos y maneja la creación o actualización de productos.
    """
    if request.method == "POST":
        product_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if product_id == "":
            saved, errors = Product.save_product(request.POST)
        else:
            product = get_object_or_404(Product, pk=product_id)
            saved, errors = product.update_product(request.POST)

        if saved:
            return redirect(reverse("product_repo"))

        return render(
            request, "products/form.html", {"errors": errors, "product": request.POST},
        )

    product = None
    if id is not None:
        product = get_object_or_404(Product, pk=id)

    return render(request, "products/form.html", {"product": product})


def product_delete(request):
    """
    Elimina un producto.
    """
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()

    return redirect(reverse("product_repo"))

# Mascota
def pet_repository(request):
    """
    Renderiza la lista de mascotas.
    """
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})

def pet_form(request, id=None):
    """
    Renderiza el formulario de mascotas y maneja la creación o actualización de mascotas.
    """
    if request.method == "POST":
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = False

        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            update_result = pet.update_pet(request.POST)
            if update_result is not None:
                saved, errors = update_result
            else:
                saved = True

        if saved:
            return redirect(reverse("pet_repo"))

        return render(
            request, "pets/form.html", {"errors": errors, "pet": request.POST},
        )

    pet = None
    if id is not None:
        pet = get_object_or_404(Pet, pk=id)

    return render(request, "pets/form.html", {"pet": pet})


def pet_delete(request):
    """
    Elimina una mascota.
    """
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()

    return redirect(reverse("pet_repo"))

# Veterinario

def veterinary_repository(request):
    """
    Renderiza la lista de veterinarios.
    """
    veterinaries = Veterinary.objects.all()
    return render(request, "veterinaries/repository.html", {"veterinaries": veterinaries})


def veterinary_form(request, id=None):
    """
    Renderiza el formulario de veterinarios y maneja la creación o actualización de veterinarios.
    """
    if request.method == "POST":
        veterinary_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if veterinary_id == "":
            saved, errors = Veterinary.save_veterinary(request.POST)
        else:
            veterinary = get_object_or_404(Veterinary, pk=veterinary_id)
            saved, errors =  veterinary.update_veterinary(request.POST)
          
           

        if saved:
            return redirect(reverse("veterinary_repo"))

        return render(
            request, "veterinaries/form.html", {"errors": errors, "veterinary": request.POST},
        )

    veterinary = None
    if id is not None:
        veterinary = get_object_or_404(Veterinary, pk=id)

    return render(request, "veterinaries/form.html", {"veterinary": veterinary})


def veterinary_delete(request):
    """
    Elimina un veterinario.
    """
    veterinary_id = request.POST.get("veterinary_id")
    veterinary = get_object_or_404(Veterinary, pk=int(veterinary_id))
    veterinary.delete()

    return redirect(reverse("veterinary_repo"))

# Funciones para Medicamentos
def medicine_repository(request):
    """
    Renderiza la lista de medicamentos.
    """
    medicines = Medicine.objects.all()
    return render(request, "medicines/repository.html", {"medicines": medicines})

def medicine_form(request, id=None):
    """
    Renderiza el formulario de medicamentos y maneja la creación o actualización de medicamentos.
    """
    medicine = None  # Asignar un valor predeterminado a la variable medicine
    if request.method == "POST":
        medicine_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if medicine_id == "":
            saved, errors = Medicine.save_medicine(request.POST)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            saved, errors = medicine.update_medicine(request.POST)

        if saved:
            return redirect(reverse("medicine_repo"))

        return render(
            request, "medicines/form.html", {"errors": errors, "medicine": request.POST},
        )

    medicine = None
    if id is not None:
        medicine = get_object_or_404(Medicine, pk=id)

    return render(request, "medicines/form.html", {"medicine": medicine})

def medicine_delete(request):
    """
    Elimina un medicamento.
    """
    medicine_id = request.POST.get("medicine_id")
    medicine = get_object_or_404(Medicine, pk=int(medicine_id))
    medicine.delete()

    return redirect(reverse("medicine_repo"))