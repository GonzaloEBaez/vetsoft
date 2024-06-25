import re  # Importa el módulo de expresiones regulares
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError, models


class CityEnum(models.TextChoices):
    """
     Enumeracion de la Ciudad
    """
    LA_PLATA = 'La Plata', 
    BERISSO = 'Berisso',
    ENSENADA = 'Ensenada',

    

def validate_client(data):
    """
    Esta función valida los datos del cliente.
    """
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    city = data.get("city", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', name):
        errors["name"] = "El nombre debe contener solo letras y espacios"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif not phone.isdigit():
        errors["phone"] = "El teléfono solo debe contener números"
    elif not phone.startswith("54"):
        errors["phone"] = "El telefono debe comenzar con 54"
            

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif not re.match(r"^[a-zA-Z0-9._%+-]+@vetsoft\.com$", email):
        errors["email"] = "El email debe tener un formato válido y ser de la forma nombre@vesoft.com"
    
    
    if city == "" or city is None:
        errors["city"] = "Por favor ingrese una ciudad"
    elif city not in dict(CityEnum.choices):
        errors["city"] = "Por favor ingrese una ciudad valida"

    return errors

class Client(models.Model):
    """
    Modelo que representa a un cliente en el sistema.
    """
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    city = models.CharField(max_length=35, choices=CityEnum.choices)

    def __str__(self):
        """
        Devuelve la representación de cadena de cliente.
        """
        return self.name

    @classmethod
    def save_client(cls, client_data):
        """
        Guarda un cliente en la base de datos.

        Args:
            client_data (dict): Datos del cliente.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.
      
        Esta función guarda el cliente. 
        """
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            city=client_data.get("city"),
        )

        return True, None

      
    def update_client(self, client_data):
        """
        Actualiza los datos de un cliente existente.

        Args:
            client_data (dict): Datos actualizados del cliente.

        Esta función actualiza el cliente. 
        """
    
        
        errors = validate_client(client_data)
   
        if len(errors) > 0:
            return False, errors
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.city = client_data.get("city", "") or self.city

        try:
            self.save()
            return True, None
        except (IntegrityError, ValidationError) as e:
            return False, {"error": str(e)}


def validate_provider(data):
    """
    Valida los datos del proveedor.

    Args:
        data (dict): Datos del proveedor.

    Returns:
        dict: Diccionario de errores encontrados.

    Esta función valida los datos del proovedor.
    """
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
    """
    Modelo que representa a un cliente en el sistema.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)

    def __str__(self):
        """
        Devuelve la representación de cadena de proovedor.
        """
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        """
        Guarda un proveedor en la base de datos.

        Args:
            provider_data (dict): Datos del proveedor.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.

        Esta función guarda el proveedor en la base de datos.
        """
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
        """
        Actualiza los datos de un proveedor existente.

        Args:
            provider_data (dict): Datos actualizados del proveedor.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.
        Esta función actualiza el proveedor.
        """
        errors = validate_provider(provider_data)

        if len(errors) > 0:
            return False, errors

        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.address = provider_data.get("address", "") or self.address
        

        try:
            self.save()
            return True, None
        except Exception as e:
            return False, e



        self.save()
        return True, None


def validate_product(data):
    """
    Valida los datos del producto.
    Args:
        data (dict): Datos del producto.

    Returns:
        dict: Diccionario de errores encontrados.
    Esta función valida los datos del producto.
    """
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
    """
    Modelo que representa a un producto en el sistema.
    """
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
            """
            Devuelve la representación de cadena de producto.
            """
            return self.name

    @classmethod
    def save_product(cls, product_data):
        """
        Guarda un producto en la base de datos.

        Args:
            product_data (dict): Datos del producto.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.
        Esta función guarda el producto en la base de datos.
        """
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
        """
        Actualiza los datos de un producto existente.
        Esta función actualiza el producto.
        Args:
            product_data (dict): Datos actualizados del producto.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.
        """
        errors = validate_product(product_data)
        if len(errors.keys()) > 0:
            return False, errors

        self.name = product_data.get("name", "") or self.name
        self.product_type = product_data.get("product_type", "") or self.product_type
        self.price = product_data.get("price", "") or self.price

        self.save()
        return True, None

def validate_pet(data):
    """
    Valida los datos de la mascota.

    Args:
        data (dict): Datos de la mascota.

    Returns:
        dict: Diccionario de errores encontrados.
    Esta función valida los datos de mascota.
    """
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
    """
    Modelo que representa a una mascota en el sistema.
    """
    name = models.CharField(max_length=40)
    breed = models.CharField(max_length=40)
    birthday = models.DateField()
    weight = models.FloatField()

    def __str__(self):
            """
            Devuelve la representación de cadena de mascota.
            """
            return self.name

    @classmethod
    def save_pet(cls, pet_data):
        """
        Guarda una mascota en la base de datos.

        Args:
            pet_data (dict): Datos de la mascota.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.
        Esta función guarda la mascota en la base de datos.
        """
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
        """
        Actualiza los datos de una mascota existente.

        Args:
            pet_data (dict): Datos actualizados de la mascota.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.
        Esta función actualiza los datos de mascota.
        """
        errors = validate_pet(pet_data)
        if len(errors.keys()) > 0:
            return False, errors

        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday
        self.weight = pet_data.get("weight", "") or self.weight

        self.save()
        return True, None

def validate_veterinary(data):
    """
    Valida los datos del veterinario.

    Args:
        data (dict): Datos del veterinario.

    Returns:
        dict: Diccionario de errores encontrados.
    Esta función valida los datos del veterinario.
    """
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', name):
        errors["name"] = "El nombre debe contener solo letras y espacios"    

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"
    
    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif not phone.isdigit():
        errors["phone"] = "El teléfono solo debe contener números enteros enteros"

    return errors

class Veterinary(models.Model):
    """
    Modelo que representa a un veterinario en el sistema.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    
    def __str__(self):
        """
        Devuelve la representación de cadena de veterinario.
        """
        return self.name

    @classmethod
    def save_veterinary(cls, veterinary_data):
        """
        Guarda un veterinario en la base de datos.

        Args:
            veterinary_data (dict): Datos del veterinario.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.
        Esta función guarda los datos de veterinario.
        """
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
        """
        Actualiza los datos de un veterinario existente.

        Args:
            veterinary_data (dict): Datos actualizados del veterinario.
        Esta función actualiza los datos de veterinario.
        """
 
        errors = validate_veterinary(veterinary_data)


        if len(errors) > 0:
            return False, errors
        self.name = veterinary_data.get("name", "") or self.name
        self.email = veterinary_data.get("email", "") or self.email
        self.phone = veterinary_data.get("phone", "") or self.phone


        try:
            self.save()
            return True, None
        except (IntegrityError, ValidationError) as e:
            return False, {"error": str(e)}
        
        






        



















































































































def validate_medicine(data):
    """
    Valida los datos del medicamento.

    Args:
        data (dict): Datos del medicamento.

    Returns:
        dict: Diccionario de errores encontrados.
    Esta  función valida los datos de medicina.
    """
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
    """
    Modelo que representa una medicina en el sistema.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    dose = models.IntegerField()

    def __str__(self):
        """
        Devuelve la representación de cadena de medicina.
        """
        return self.name

    @classmethod
    def save_medicine(cls, medicine_data):
        """
        Guarda un medicamento en la base de datos.

        Args:
            medicine_data (dict): Datos del medicamento.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.
        Esta función guarda los datos de medicina.
        """
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
        """
        Actualiza los datos de un medicamento existente.

        Args:
            medicine_data (dict): Datos actualizados del medicamento.

        Returns:
            tuple: (bool, dict or None) Éxito de la operación y errores encontrados, si los hay.
        Esta función actualiza los datos de medicina.
        """
        errors = validate_medicine(medicine_data)

        if len(errors) > 0:
            return False, errors
    
        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose
       

        try:
            self.save()
            return True, None
        except Exception as e:
            return False, {"errors": str(e)}

        self.save()
        return True, None
      
