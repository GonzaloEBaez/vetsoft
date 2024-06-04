import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser
from datetime import datetime
from django.utils import timezone
from django.urls import reverse

from app.models import Client, Provider


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.chromium.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Inicio")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Inicio")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))



        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self):
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

    def test_should_show_client_delete_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente"
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )


class MedicineCreateEditTestCase(PlaywrightTestCase):
    def test_should_show_error_for_dose_greater_than_10(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("prueba")
        self.page.get_by_label("Descripcion").fill("arbol")
        self.page.get_by_label("Dosis").fill("11")  # Introduce una dosis mayor
        self.page.get_by_role("button", name="Guardar").click()

        # Verifica si se muestra el mensaje de error esperado
        expect(self.page.get_by_text("La dosis debe estar en un rango de 1 a 10")).to_be_visible()

    def test_should_show_error_for_dose_less_than_1(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("prueba")
        self.page.get_by_label("Descripcion").fill("arbol")
        self.page.get_by_label("Dosis").fill("-1")  # Introduce una dosis menor
        self.page.get_by_role("button", name="Guardar").click()

        # Verifica si se muestra el mensaje de error esperado
        expect(self.page.get_by_text("La dosis debe estar en un rango de 1 a 10")).to_be_visible()

class ProvidersRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).to_be_visible()

    def test_should_show_providers_data(self):
        Provider.objects.create(
            name="Juan Roman Riquelme",
            email="senor10@hotmail.com",
            address="13 y 44",
        )

    def test_should_show_add_provider_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo Proveedor", exact=False
        )
        expect(add_provider_action).to_have_attribute("href", reverse("provider_form"))

    #Agrego e2e que utilicen el atributo address
    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('provider_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor, ingrese una direccion")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Roman Riquelme")
        self.page.get_by_label("Email").fill("senor10@gmail.com")
        self.page.get_by_label("Direccion").fill("")
        
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor, ingrese una direccion")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_provider(self):
        provider = Provider.objects.create(
            name="Juan Roman Riquelme",
            email="senor10@hotmail.com",
            address="13 y 44",
        )

        path = reverse("provider_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Martin Palermo")
        self.page.get_by_label("Email").fill("titan@gmail.com")
        self.page.get_by_label("Direccion").fill("124 y 60")
        

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Roman Riquelme")).not_to_be_visible()
        expect(self.page.get_by_text("senor10@hotmail.com")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()

        expect(self.page.get_by_text("Martin Palermo")).to_be_visible()
        expect(self.page.get_by_text("titan@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("124 y 60")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("provider_edit", kwargs={"id": provider.id})
        )
        
  
class PetFormCreateValidationTestCase(PlaywrightTestCase):
    def test_should_show_error_for_future_birth_date(self):
        self.page.goto(f"{self.live_server_url}{reverse('pet_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        # Introduce una fecha de nacimiento no valida
        future_date = datetime.now().date() + timezone.timedelta(days=7)  # Ejemplo: 7 días en el futuro
        future_date_str = future_date.strftime("%Y-%m-%d")  # Formatea la fecha como cadena

        self.page.get_by_label("Nombre").fill("Frida")
        self.page.get_by_label("Raza").fill("negrita")
        self.page.get_by_label("Fecha de nacimiento").fill(future_date_str)  # Introduce la fecha en el campo
        self.page.get_by_label("Peso").fill("4")
        self.page.get_by_role("button", name="Guardar").click()

        # Verifica si se muestra el mensaje de error esperado
        expect(self.page.get_by_text("La fecha de nacimiento debe ser menor a la fecha actual")).to_be_visible()

    def test_should_show_error_for_present_birth_date(self):
        self.page.goto(f"{self.live_server_url}{reverse('pet_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        # Introduce una fecha de nacimiento no valida
        future_date = datetime.now().date()  # Dia actual
        future_date_str = future_date.strftime("%Y-%m-%d")  # Formatea la fecha como cadena

        self.page.get_by_label("Nombre").fill("Frida")
        self.page.get_by_label("Raza").fill("negrita")
        self.page.get_by_label("Fecha de nacimiento").fill(future_date_str)  # Introduce la fecha en el campo
        self.page.get_by_label("Peso").fill("4")

        self.page.get_by_role("button", name="Guardar").click()

        # Verifica si se muestra el mensaje de error esperado
        expect(self.page.get_by_text("La fecha de nacimiento debe ser menor a la fecha actual")).to_be_visible()     

    

    # Pruebas para peso de la mascota
    def test_should_be_able_to_create_a_new_pet(self):
        self.page.goto(f"{self.live_server_url}{reverse('pet_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        # Completar el formulario para crear una nueva mascota con valores específicos
        self.page.get_by_label("Nombre").fill("Frida")
        self.page.get_by_label("Raza").fill("negrita")
        self.page.get_by_label("Fecha de nacimiento").fill("2017-01-11")
        self.page.get_by_label("Peso").fill("10")

        self.page.get_by_role("button", name="Guardar").click()

        # Verificar que los detalles de la mascota recién creado sean visibles en la página
        expect(self.page.get_by_text("Frida")).to_be_visible()
        expect(self.page.get_by_text("negrita")).to_be_visible()
        expect(self.page.get_by_text("Jan. 11, 2017")).to_be_visible()
        expect(self.page.get_by_text("10")).to_be_visible()

        # Prueba para verificar si se muestran errores cuando el formulario es inválido con un peso menor que cero
    def test_should_view_errors_if_form_is_invalid_with_weight_less_than_zero(self): 
        self.page.goto(f"{self.live_server_url}{reverse('pet_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        # Verificar que se muestren mensajes de error para ingresar nombre, raza, fecha de nacimiento y peso
        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una raza")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un peso")).to_be_visible()

        # Completar el formulario con un peso negativo y enviarlo
        self.page.get_by_label("Nombre").fill("Frida")
        self.page.get_by_label("Raza").fill("negrita")
        self.page.get_by_label("Fecha de nacimiento").fill("2017-01-11")
        self.page.get_by_label("Peso").fill("-10")

        self.page.get_by_role("button", name="Guardar").click()

        # Verificar que el mensaje de error "El peso debe ser mayor que cero" sea visible
        expect(
            self.page.get_by_text("El peso debe ser mayor a cero")
        ).to_be_visible()

# Pruebas de unidad para verificar la creación exitosa de un nuevo producto

class ProductCreatePriceGreaterThanZeroTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_product(self):
        self.page.goto(f"{self.live_server_url}{reverse('product_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

# Completar el formulario para crear un nuevo producto con valores específicos
        self.page.get_by_label("Nombre").fill("Gentamicina")
        self.page.get_by_label("Tipo").fill("Antibiotico")
        self.page.get_by_label("Precio").fill("200")

        self.page.get_by_role("button", name="Guardar").click()

# Verificar que los detalles del producto recién creado sean visibles en la página
        expect(self.page.get_by_text("Gentamicina")).to_be_visible()
        expect(self.page.get_by_text("Antibiotico")).to_be_visible()
        expect(self.page.get_by_text("200")).to_be_visible()

# Prueba para verificar si se muestran errores cuando el formulario es inválido con un precio menor que cero
    def test_should_view_errors_if_form_is_invalid_with_price_less_than_zero(self):
        self.page.goto(f"{self.live_server_url}{reverse('product_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

# Verificar que se muestren mensajes de error para ingresar nombre, tipo y precio
        expect(self.page.get_by_text("Por favor ingrese su nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un tipo")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un precio")).to_be_visible()

# Completar el formulario con un precio negativo y enviarlo
        self.page.get_by_label("Nombre").fill("Gentamicina")
        self.page.get_by_label("Tipo").fill("Antibiótico")
        self.page.get_by_label("Precio").fill("-10")

        self.page.get_by_role("button", name="Guardar").click()

# Verificar que los mensajes de error para ingresar el nombre y el tipo no sean visibles
        expect(self.page.get_by_text("Por favor ingrese su nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un tipo")
        ).not_to_be_visible()

# Verificar que el mensaje de error "El precio debe ser mayor que cero" sea visible
        expect(
            self.page.get_by_text("El precio debe ser mayor que cero")
        ).to_be_visible()