from django.db import models
from datetime import datetime


def validate_client(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

        self.save()

def validate_provider(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
        )

        return True, None

    def update_provider(self, provider_data):
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email

        self.save()


def validate_product(data):
    errors = {}

    name = data.get("name", "")
    product_type = data.get("product_type", "")
    price = data.get("price", "")

    if name == "":
        errors["name"] = "Por favor ingrese su nombre"

    if product_type == "":
        errors["type"] = "Por favor ingrese un tipo de producto"

    if price == "":
        errors["price"] = "Por favor ingrese un precio válido"

    return errors


class Product(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=15)
    price = models.CharField(max_length=15)
    
    def __str__(self):
            return self.name

    @classmethod
    def save_product(cls, product_data):
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors

        Product.objects.create(
            name=product_data.get("name"),
            product_type=product_data.get("product_type"),
            price=product_data.get("price"),
        )
    
        return True, "Producto creado exitosamente"

    def update_product(self, product_data):
        self.name = product_data.get("name", "") or self.name
        self.product_type = product_data.get("product_type", "") or self.product_type
        self.price = product_data.get("price", "") or self.price

        self.save()

def validate_pet(data):
    errors = {}

    name = data.get("name", "")
    breed = data.get("breed", "")
    birthday = data.get("birthday", "")
    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if breed == "":
        errors["breed"] = "Por favor ingrese una raza"
    
    if birthday == "":
        errors["birthday"] = "Por favor ingrese una fecha de nacimiento"
        
    return errors


class Pet(models.Model):
    name = models.CharField(max_length=40)
    breed = models.CharField(max_length=40)
    birthday = models.CharField(max_length=40,default='')
    
    def __str__(self):
            return self.name

    @classmethod
    def save_pet(cls, pet_data):
        errors = validate_pet(pet_data)
    
        if len(errors.keys()) > 0:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
        )

        return True, None
    
    def update_pet(self, pet_data):
        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday


        self.save()

def validate_veterinary(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"
    
    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    return errors


class Veterinary(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    
    def __str__(self):
        return self.name

    @classmethod
    def save_veterinary(cls, veterinary_data):
        errors = validate_veterinary(veterinary_data)
        Veterinary.objects.create(
            name=veterinary_data.get("name"),
            email=veterinary_data.get("email"),
            phone=veterinary_data.get("phone"),
        )

        return True, None

    def update_veterinary(self, veterinary_data):
        self.name = veterinary_data.get("name", "") or self.name
        self.email = veterinary_data.get("email", "") or self.email
        self.phone = veterinary_data.get("phone", "") or self.phone

        self.save()
 

def validate_medicine(medicine_data):
    errors = {}
    name = medicine_data.get("name")
    description = medicine_data.get("description")
    dose = medicine_data.get("dose")

    if not name:
        errors["name"] = "El nombre es obligatorio."

    if not description:
        errors["description"] = "La descripción es obligatoria."

    try:
        dose = float(dose)
        if dose <= 0:
            errors["dose"] = "La dosis debe ser mayor a 0."
    except ValueError:
        errors["dose"] = "La dosis debe ser un número válido."

    return errors
    
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    dose = models.FloatField()

    def __str__(self):
        return self.name
    

    @classmethod
    def save_medicine(cls, medicine_data):
        errors = validate_medicine(medicine_data)

        if errors:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        )

        return True, "Medicamento creado exitosamente"
    
    def update_medicine(self, medicine_data):
        name = medicine_data.get("name", "")
        description = medicine_data.get("description", "")
        dose = medicine_data.get("dose", "")

        errors = validate_medicine(medicine_data)

        if errors:
            return False, errors  # Devolver False y errores si hay problemas de validación

        # Aplicar los cambios al objeto Medicine
        self.name = name
        self.description = description
        self.dose = dose

        self.save()  # Guardar los cambios en la base de datos

        return True, "Medicamento actualizado exitosamente"