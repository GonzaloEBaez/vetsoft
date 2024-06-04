from django.test import TestCase
from app.models import Client,Pet,validate_pet,Provider, Product,Medicine
from django.utils import timezone

class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": "221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

class MedicineModelTest(TestCase):
    
    def test_can_create_medicine_with_valid_dose(self):
        success, errors = Medicine.save_medicine(
            {
                "name": "Ibuprofeno",
                "description": "Medicamento antiinflamatorio",
                "dose": 1,
            }
        )
        self.assertTrue(success)

        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

    def test_cannot_create_medicine_with_invalid_dose(self):
        success, errors = Medicine.save_medicine(
            {
                "name": "Ibuprofeno",
                "description": "Medicamento antiinflamatorio",
                "dose": 11,
            }
        )
        self.assertFalse(success)
        self.assertIn("dose", errors)

        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 0)

    def test_update_medicine_with_invalid_dose(self):
        Medicine.save_medicine(
            {
                "name": "Paracetamol",
                "description": "Medicamento para el dolor",
                "dose": 5,
            }
        )
        medicine = Medicine.objects.get(pk=1)

        self.assertEqual(medicine.dose, 5)

        success, errors = medicine.update_medicine({"dose": 11})

        self.assertFalse(success)
        self.assertIn("dose", errors)
        medicine_updated = Medicine.objects.get(pk=1)

        self.assertEqual(medicine_updated.dose, 5)

class  ProviderModelTest(TestCase):
    def test_can_create_and_get_provider(self):
        Provider.save_provider(
            {
                "name": "Juan Roman Riquelme",
                "email": "senor10@gmail.com",
                "address": "13 y 44",
            }
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Juan Roman Riquelme")
        self.assertEqual(providers[0].address, "13 y 44")
        self.assertEqual(providers[0].email, "senor10@gmail.com")

    #Agrego test unitario especifico de la issue de provider
    def test_provider_address(self):
        addres = "calle 13 y 44"
        Provider.save_provider(
            {
                "name": "Juan Roman Riquelme",
                "email": "senor10@gmail.com",
                "address": addres, #guardo proveedor con direccion especifica
            }
        )
        provider = Provider.objects.get(address=addres) #recupero proveedor segun la direccion (supongo que no van a haber dos proveedores con esa direccion)
        self.assertEqual(provider.address, addres) #verifica que la direccion recuperada coincida con la especifica

class PetModelTest(TestCase):
    def test_validate_pet_birthday(self):
        # Probamos la validación de fecha de nacimiento para una mascota
        valid_data = {
            "name": "Frida",
            "breed": "negrita",
            "birthday": "2013-01-01",  # Fecha de nacimiento válida
            "weight": "22",
        }
        self.assertEqual(validate_pet(valid_data), {})  # La validación debería pasar sin errores
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        invalid_data = {
            "name": "Frida",
            "breed": "negrita",
            "birthday": future_date.strftime("%Y-%m-%d"),  # Fecha de nacimiento en el futuro
            "weight": "22",
        }
        expected_error = {"birthday": "La fecha de nacimiento debe ser menor a la fecha actual"}
        self.assertEqual(validate_pet(invalid_data), expected_error)  # La validación debería dar error



    # Validacion de peso mascota

    def test_create_pet_with_valid_weight(self):
        success, message_or_errors = Pet.save_pet({
            "name": "Frida",
            "breed": "negrita",
            "birthday": "2017-01-01",
            "weight": "4" # Peso válido
        })

        self.assertTrue(success)
        self.assertEqual(message_or_errors, None)

    def test_create_pet_with_invalid_weight_negative(self):
        success, message_or_errors = Pet.save_pet({
            "name": "Frida",
            "breed": "negrita",
            "birthday": "2017-01-01",
            "weight": "-1" # Peso inválido
        })

        self.assertFalse(success)
        self.assertIn("weight", message_or_errors)
        self.assertEqual(message_or_errors["weight"], "El peso debe ser mayor a cero")

class ProductModelTest(TestCase):
    def test_create_product_with_valid_price(self):
        success, message_or_errors = Product.save_product({
            "name": "Test Product",
            "product_type": "Test Type",
            "price": "100"
        })

        self.assertTrue(success)
        self.assertEqual(message_or_errors, "Producto creado exitosamente")

    def test_create_product_with_invalid_price_zero(self):
        success, message_or_errors = Product.save_product({
            "name": "Test Product",
            "product_type": "Test Type",
           "price": "0"
         })

        self.assertFalse(success)
        self.assertIn("price", message_or_errors)
        self.assertEqual(message_or_errors["price"], "El precio debe ser mayor que cero")

    def test_create_product_with_invalid_price_negative(self):
        success, message_or_errors = Product.save_product({
            "name": "Test Product",
          "product_type": "Test Type",
           "price": "-10"
        })

        self.assertFalse(success)
        self.assertIn("price", message_or_errors)
        self.assertEqual(message_or_errors["price"], "El precio debe ser mayor que cero")

