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
    address = data.get("address", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"
    
    if address == "":
        errors["address"] = "Por favor, ingrese una direccion"

    return errors


class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)

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
            address=provider_data.get("address"),
        )

        return True, None

    def update_provider(self, provider_data):
        errors = validate_provider(provider_data)

        if len(errors) > 0:
            return False, errors

        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.address = provider_data.get("address", "") or self.address

        self.save()
        return True, None



def validate_product(data):
    errors = {}

    name = data.get("name", "")
    product_type = data.get("product_type", "")
    price = data.get("price", "")

    if name == "":
        errors["name"] = "Por favor ingrese su nombre"

    if product_type == "":
        errors["product_type"] = "Por favor ingrese un tipo de producto"

    if price == "":
        errors["price"] = "Por favor ingrese un precio"
    else:
        try:
            float_price = float(price)
            if float_price <= 0:
                errors["price"] = "El precio debe ser mayor que cero"
        except ValueError:
            errors["price"] = "El precio debe ser un número válido"
    
    return errors



class Product(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
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


        errors = validate_product(product_data)
        if len(errors.keys()) > 0:
            return False, errors

        self.name = product_data.get("name", "") or self.name
        self.product_type = product_data.get("product_type", "") or self.product_type
        self.price = product_data.get("price", "") or self.price

        self.save()
        return True, None

def validate_pet(data):
    errors = {}

    name = data.get("name", "")
    breed = data.get("breed", "")
    birthday = data.get("birthday", "")
    weight = data.get("weight", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if breed == "":
        errors["breed"] = "Por favor ingrese una raza"
    
    if birthday == "":
        errors["birthday"] = "Por favor ingrese una fecha de nacimiento"
    else:
        try:
            birth = datetime.strptime(birthday, "%Y-%m-%d").date()
            if birth >= datetime.now().date():
                errors["birthday"] = "La fecha de nacimiento debe ser menor a la fecha actual"
        except ValueError:
            errors["birthday"] = "Formato de fecha inválido. Por favor ingrese la fecha en el formato correcto (YYYY-MM-DD)"

    if weight == "":
        errors["weight"] = "Por favor ingrese un peso"
    else:
        try:
            float_weight = float(weight)
            if float_weight <= 0:
                errors["weight"] = "El peso debe ser mayor a cero"
        except ValueError:
            errors["weight"] = "El peso debe ser un número válido"

    return errors


class Pet(models.Model):
    name = models.CharField(max_length=40)
    breed = models.CharField(max_length=40)
    birthday = models.DateField()
    weight = models.FloatField()

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
            weight=pet_data.get("weight"),
        )

        return True, None
    
    def update_pet(self, pet_data):
        errors = validate_pet(pet_data)
        if len(errors.keys()) > 0:
            print("Retorno false")
            return False, errors

        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday
        self.weight = pet_data.get("weight", "") or self.weight

        errors = validate_pet(pet_data)
    
        if len(errors.keys()) > 0:
            return False, errors
        
        self.save()
        return True, None

def validate_veterinary(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")


    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

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

        if len(errors.keys()) > 0:
            return False, errors


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


def validate_medicine(data):
    errors = {}

    name = data.get("name", "")
    description = data.get("description", "")
    dose = data.get("dose", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if description == "":
        errors["description"] = "Por favor ingrese una descripción"
    if dose == "":
        errors["dose"] = "Por favor ingrese una dosis"
    else:
        try:
            int_dose = int(dose)
            if int_dose < 1 or int_dose > 10:
                errors["dose"] = "La dosis debe estar en un rango de 1 a 10"
        except ValueError:
            errors["dose"] = "La dosis debe ser un número entero válido"
    return errors

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    dose = models.IntegerField()

    def __str__(self):
        return self.name

    @classmethod
    def save_medicine(cls, medicine_data):
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        )

        return True, None
    def update_medicine(self, medicine_data):
        errors = validate_medicine(medicine_data)

        if len(errors) > 0:
            return False, errors
    
        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose


        self.save()
        return True, None
    