import os
from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils import timezone
from playwright.sync_api import Browser, expect, sync_playwright

from app.models import Client, Provider

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    """
    Clase base para pruebas funcionales utilizando Playwright.
    """
    @classmethod
    def setUpClass(cls):
        """
        Esta función prepara el entorno necesario para la ejecución de un conjunto de pruebas dentro de una clase de pruebas.
        """
        super().setUpClass()
        cls.browser: Browser = playwright.chromium.launch(
            headless=headless, slow_mo=int(slow_mo),
        )

    @classmethod
    def tearDownClass(cls):
        """
        Esta función limpia y libera los recursos compartidos después de que todas las pruebas en la clase hayan sido ejecutadas.
        """
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        """
        Esta función prepara el entorno necesario antes de ejecutar cada prueba individual.
        """
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        """
        Esta función limpia y libera los recursos después de que cada prueba individual haya sido ejecutada.
        """
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    """
    Pruebas funcionales para la página de inicio.
    """
    def test_should_have_navbar_with_links(self):
        """
        Esta función verifica que una página web tenga una barra de navegación (navbar) con enlaces (links) a otras páginas o secciones del sitio.
        """
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
        """
        Esta función verifica que una página de inicio tenga tarjetas (cards) con enlaces (links) a otras partes del sitio.
        """
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    """
    Pruebas funcionales para la vista de repositorio de clientes.
    """

    def test_should_show_message_if_table_is_empty(self):
        """
        Esta función verifica que un mensaje se muestre correctamente cuando una tabla está vacía en una aplicación web.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        """
        Esta función verifica que los datos de los clientes se muestren correctamente en una determinada página de la aplicación web.
        """
        Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone="54221555232",
            email="brujita75@vetsoft.com",

        )

        Client.objects.create(
            name="Guido Carrillo",
            city="Berisso",
            phone="54221232555",
            email="goleador@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        expect(self.page.get_by_text("La Plata")).to_be_visible()

        expect(self.page.get_by_text("54221555232")).to_be_visible()
        
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("Berisso")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        """
        Esta función verifica que la página de la lista de clientes incluya una acción para agregar un nuevo cliente.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False,
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        """
        Esta función verifica que la página de detalle de cliente incluya una acción para editar el cliente.
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )

    def test_should_show_client_delete_action(self):
        """
        Esta función verifica que la página de detalle de cliente incluya una acción para eliminar el cliente.
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente",
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        """
        Esta función verifica que un cliente pueda ser eliminado correctamente a través de una solicitud POST al servidor.
        """
        Client.objects.create(
            name="Juan Sebastian Veron",
            city="La Plata",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastian Veron")).to_be_visible()

        def is_delete_response(response):
            """
            Esta función verifica si una respuesta HTTP es una respuesta de eliminación (código de estado 204 No Content).
            """
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastian Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    """
    Pruebas funcionales para crear y editar un cliente.
    """
    def test_should_be_able_to_create_a_new_client(self):
        """
        Esta función verifica que se pueda crear un nuevo cliente correctamente a través de una solicitud POST al servidor.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastian Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")


        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastian Veron")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()
        expect(self.page.get_by_text("La Plata")).to_be_visible()


    def test_should_view_errors_if_form_is_invalid(self):
        """
        Esta función  verifica que se muestren los errores de validación en el 
        formulario si se envían datos inválidos al intentar crear un nuevo cliente.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastian Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Ciudad").select_option("La Plata")


        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("El email debe ser de la forma @vetsoft.com"),
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        """
        Esta función verifica que se pueda editar un cliente existente correctamente a través de una solicitud POST al servidor.
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("54221232555")
        self.page.get_by_label("Email").fill("goleador@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("Berisso")


        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("La Plata")).not_to_be_visible()
        expect(self.page.get_by_text("54221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("Berisso")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )


    def test_should_view_errors_if_name_is_invalid(self):
        """
        Esta función verifica que muestre un mesnaje de error para un nombre invalido.
        """
        
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("manu22")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("El nombre debe contener solo letras y espacios")).to_be_visible()
        

    def test_should_show_message_if_city_is_not_selected(self):
        """
        Esta función verifica que se muestre un mensaje de error cuando se intenta 
        crear un cliente sin seleccionar ciudad
        """
        self.page.get_by_label("Nombre").fill("Angel")
        self.page.get_by_label("Teléfono").fill("542226836789")
        self.page.get_by_label("Email").fill("fideo@vetsoft.com")
        # no selecciono una ciudad
        self.page.get_by_role("button", name="Guardar").click()

        # Verifica si se muestra el mensaje de error esperado
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()


class MedicineCreateEditTestCase(PlaywrightTestCase):
    """
    Pruebas para crear y editar medicamentos.
    """
    def test_should_show_error_for_dose_greater_than_10(self):
        """
        Esta función verifica que se muestre un mensaje de error cuando se intenta 
        crear o editar un medicamento con una dosis mayor que 10.
        """
        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("prueba")
        self.page.get_by_label("Descripcion").fill("arbol")
        self.page.get_by_label("Dosis").fill("11")  # Introduce una dosis mayor
        self.page.get_by_role("button", name="Guardar").click()

        # Verifica si se muestra el mensaje de error esperado
        expect(self.page.get_by_text("La dosis debe estar en un rango de 1 a 10")).to_be_visible()

    def test_should_show_error_for_dose_less_than_1(self):
        """
        Esta función verifica que se muestre un mensaje de error cuando se intenta crear o 
        editar un medicamento con una dosis menor que 1.
        """
        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("prueba")
        self.page.get_by_label("Descripcion").fill("arbol")
        self.page.get_by_label("Dosis").fill("-1")  # Introduce una dosis menor
        self.page.get_by_role("button", name="Guardar").click()

        # Verifica si se muestra el mensaje de error esperado
        expect(self.page.get_by_text("La dosis debe estar en un rango de 1 a 10")).to_be_visible()

class ProvidersRepoTestCase(PlaywrightTestCase):
    """
    Pruebas para verificar el comportamiento del repositorio de proveedores.
    """
    def test_should_show_message_if_table_is_empty(self):
        """
        Esta función verifica que se muestre un mensaje adecuado si una tabla en la interfaz de usuario está vacía.
        """
        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).to_be_visible()

    def test_should_show_providers_data(self):
        """
        Esta función verifica que se muestren los datos de los proveedores en la interfaz de usuario.
        """
        Provider.objects.create(
            name="Juan Roman Riquelme",
            email="senor10@hotmail.com",
            address="13 y 44",
        )

    def test_should_show_add_provider_action(self):
        """
        Esta función verifica que en la interfaz de usuario se muestre una acción para agregar un nuevo proveedor.
        """
        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo Proveedor", exact=False,
        )
        expect(add_provider_action).to_have_attribute("href", reverse("provider_form"))

    #Agrego e2e que utilicen el atributo address
    def test_should_view_errors_if_form_is_invalid(self):
        """
        Esta función verifica que se muestren los errores de validación en un 
        formulario si se envían datos inválidos al servidor. 
        """
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
            self.page.get_by_text("Por favor ingrese un email valido"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor, ingrese una direccion"),
        ).to_be_visible()

    def test_should_be_able_to_edit_a_provider(self):
        """
        Esta función verifica que se pueda editar un proveedor existente correctamente 
        a través de una solicitud POST al servidor.
        """
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
            "href", reverse("provider_edit", kwargs={"id": provider.id}),
        )
        
  
class PetFormCreateValidationTestCase(PlaywrightTestCase):
    """
    Pruebas para validar la creación de una mascota en el formulario.
    """
    def test_should_show_error_for_future_birth_date(self):
        """
        Esta función verifica que se muestre un mensaje de error cuando se intenta 
        ingresar una fecha de nacimiento en el futuro al crear o editar un cliente.
        """
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
        """
        Esta función verifica que se muestre un mensaje de error cuando se intenta ingresar una fecha de nacimiento 
        que corresponde al día actual (o una fecha anterior al día actual) al crear o editar un cliente.
        """
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
        

    def test_should_be_able_to_create_a_new_pet_goto(self):
        """
        Verifica si el test me permite crear una nueva masota.
        """
  
        self.page.goto(f"{self.live_server_url}{reverse('pet_form')}")


    # Pruebas para peso de la mascota
    def test_should_be_able_to_create_a_new_pet(self):
        """
        Esta función verifica que se pueda crear una nueva mascota correctamente 
        a través de una solicitud POST al servidor. 
        """
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
        """
        Esta función verifica que se muestren errores cuando se intenta 
        enviar un formulario con un peso de mascota menor que cero.
        """
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
            self.page.get_by_text("El peso debe ser mayor a cero"),
        ).to_be_visible()

# Pruebas de unidad para verificar la creación exitosa de un nuevo producto

class ProductCreatePriceGreaterThanZeroTestCase(PlaywrightTestCase):
    """
    Pruebas para verificar la creación de un nuevo producto con un precio mayor que cero.
    """
    def test_should_be_able_to_create_a_new_product(self):
        """
        Esta función verifica que se pueda crear un nuevo producto correctamente 
        a través de una solicitud POST al servidor.
        """
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
        """
        Esta función verifica que se muestren errores cuando se intenta enviar 
        un formulario con un precio de producto menor que cero.
        """
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
        expect(self.page.get_by_text("Por favor ingrese un tipo")).not_to_be_visible()

# Verificar que el mensaje de error "El precio debe ser mayor que cero" sea visible
        expect(self.page.get_by_text("El precio debe ser mayor que cero")).to_be_visible()
