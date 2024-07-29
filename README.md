# Web Scraping - Proyecto Individual

Estructura de la base de datos MySQL

```sql
DROP DATABASE IF EXISTS quotes;
CREATE DATABASE quotes;
USE quotes;

CREATE TABLE authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    about TEXT,
    born DATE,
    birth_place VARCHAR(100),
    about_page_url VARCHAR(200)  -- Campo para almacenar la URL de la página "about"
);

CREATE TABLE quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE quote_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quote_id INT,
    tag_id INT,
    FOREIGN KEY (quote_id) REFERENCES quotes(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id),
    UNIQUE (quote_id, tag_id)  -- Asegura que no haya duplicados en la combinación de quote_id y tag_id
);

```

![Untitled]([https://prod-files-secure.s3.us-west-2.amazonaws.com/fd601164-f93c-4e8c-811f-4ddad4d5af3e/4e5f7b69-a94b-4f80-8300-447d28608f73/Untitled.png](https://beaded-sociology-706.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Ffd601164-f93c-4e8c-811f-4ddad4d5af3e%2F4e5f7b69-a94b-4f80-8300-447d28608f73%2FUntitled.png?table=block&id=0139a48f-dcc2-471e-8367-eeb9d1937db2&spaceId=fd601164-f93c-4e8c-811f-4ddad4d5af3e&width=2000&userId=&cache=v2)

### Librerías de Web Scraping, Beatiful Soup o Scrapy

En el archivo web_scraper.py estamos usando la librería Beautiful Soup para hacer web scraping. Cada librería tiene sus propias fortalezas:
**Beautiful Soup:**

- Es más fácil de aprender y usar para proyectos pequeños a medianos.
- Es excelente para analizar HTML y XML.
- Se integra bien con requests para hacer peticiones HTTP.
- Es ideal para scraping de pocas páginas o sitios web simples.

**Scrapy**:

- Es un framework más completo y potente para web scraping a gran escala.
- Tiene mejor rendimiento para proyectos grandes.
- Incluye características como manejo de sesiones, pipelines de datos, y exportación de datos.
- Es mejor para scraping de múltiples páginas o sitios web complejos.

En este caso, Beautiful Soup es una buena elección porque el sitio que estamos scrapeando es relativamente simple y no necesitamos las características avanzadas de Scrapy.

## Estructura del Proyecto

```markdown
django-web-scraping/
│
├── manage.py
├── xyz_quotes/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── quotes/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── quote_list.html
│   │   ├── author_detail.html
│   │   ├── tag_detail.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── styles.css
│   ├── management/
│       ├── __init__.py
│       ├── commands/
│           ├── __init__.py
│           ├── web_scraper.py
│           ├── data_import.py
│           ├── update_quotes.py
│
└── requirements.txt

```

# Documentación del Proyecto de Web Scraping con Django

## 1. Visión General del Proyecto

- Nombre del Proyecto: Web Scraping con Django
- Propósito: Extraer citas y información de autores de [quotes.toscrape.com](http://quotes.toscrape.com/) y presentarlas en una aplicación web
- Características Principales: Web scraping, almacenamiento de datos, presentación de datos, visualización de datos

## 2. Stack Tecnológico

- Backend: Django
- Base de Datos: MySQL
- Frontend: Plantillas de Django, HTML, CSS (Bootstrap).
- Extracción de Datos: Beautiful Soup, Requests
- Visualización de Datos: Matplotlib, Seaborn

## 3. Estructura del Proyecto

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/fd601164-f93c-4e8c-811f-4ddad4d5af3e/ee287479-46d0-491d-b6bf-747aadf49e73/Untitled.png)

## 4. Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Gestor de bases de datos (MySQL Workbench)
- Git (para clonar el repositorio)

### Configuración del entorno

1. Clonar el repositorio:
    
    ```
    git clone <https://github.com/AI-School-F5-P3/WebScraping_Angelmaria.git>
    cd WebScraping_Angelmaria
    ```
    
2. Crear y activar un entorno virtual:
    
    ```
    python -m venv env
    source env/bin/activate  # En Windows: env\\Scripts\\activate
    ```
    
3. Instalar las dependencias:
    
    ```
    pip install -r requirements.txt
    ```
    

### Pasos de instalación

1. Configurar la base de datos en `settings.py`
2. Aplicar las migraciones:
    
    ```
    python manage.py migrate
    ```
    
3. Crear un superusuario (solo si se quiere acceder a la zona admin):
    
    ```
    python manage.py createsuperuser
    ```
    

### Ejecución del proyecto localmente

1. Iniciar el servidor de desarrollo:
    
    ```
    python manage.py runserver
    ```
    
2. Acceder a la aplicación en `http://localhost:8000`
3. Acceder al panel de administración en `http://localhost:8000/admin`

### Configuración inicial

1. Ejecutar el archivo update_quotes.py que automatiza la actualización del “scraping” y ejecuta tanto el scraper inicial (web_scarper) como la importación de los datos iniciales (data_import):

```
python manage.py update_quotes
```

## 5. Componentes Principales

### 5.1 Web Scraper (web_scraper.py)

- Propósito: Extraer citas e información de autores de [quotes.toscrape.com](http://quotes.toscrape.com/)
- Funcionalidad:
    - Utiliza las bibliotecas `requests` para hacer peticiones HTTP y `BeautifulSoup` para analizar el HTML
    - Navega por múltiples páginas del sitio web (hasta 5 páginas por defecto)
    - Extrae citas, autores y etiquetas de cada página
    - Recopila información detallada del autor de sus páginas individuales
- Métodos clave:
    - `scrape_quotes()`: Método principal que coordina el proceso de scraping
    - `scrape_author_info(author_url)`: Extrae información detallada del autor
    - `convert_date(date_str)`: Convierte fechas al formato YYYY-MM-DD
- Manejo de errores:
    - Utiliza bloques try/except para manejar errores de red y HTTP
    - Registra advertencias para fechas no reconocidas o información faltante del autor

### 5.2 Importación de Datos (data_import.py)

- Propósito: Importar los datos extraídos a la base de datos de Django
- Funcionalidad:
    - Lee el archivo JSON generado por el web scraper
    - Crea o actualiza registros en la base de datos para autores, citas y etiquetas
- Proceso de importación:
    - Itera sobre los autores en el JSON, creando o actualizando registros de Author
    - Para cada cita, crea un registro de Quote y lo asocia con su autor
    - Crea registros de Tag y los asocia con las citas correspondientes a través de QuoteTag

### 5.3 Mecanismo de Actualización (update_quotes.py)

- Propósito: Automatizar la actualización periódica de la base de datos
- Funcionalidad:
    - Utiliza la biblioteca `schedule` para programar actualizaciones diarias
    - Ejecuta el web scraper y el proceso de importación de datos
- Métodos clave:
    - `schedule_jobs()`: Configura la tarea para ejecutarse diariamente a medianoche
    - `run_update()`: Ejecuta el proceso de actualización completo

### 5.4 Vistas y Plantillas

- quote_list.html: Muestra una lista paginada de citas con opciones de filtrado
- author_detail.html: Muestra información detallada sobre un autor y sus citas
- tag_detail.html: Muestra citas asociadas a una etiqueta específica
- about.html: Proporciona información sobre el proyecto
- base.html: Plantilla base que define la estructura común de las páginas

## 6. Modelos de Datos

### Modelo de Author

- Campos:
    - `name`: CharField, nombre del autor
    - `born`: DateField, fecha de nacimiento del autor
    - `birth_place`: CharField, lugar de nacimiento
    - `about`: TextField, biografía del autor
    - `about_page_url`: URLField, enlace a la página de información del autor

### Modelo de Quote

- Campos:
    - `text`: TextField, texto de la cita
    - `author`: ForeignKey a Author, establece la relación con el autor

### Modelo de Tag

- Campos:
    - `name`: CharField, nombre de la etiqueta

### Modelo de QuoteTag (Relación Many-to-Many)

- Campos:
    - `quote`: ForeignKey a Quote
    - `tag`: ForeignKey a Tag

### Relaciones entre modelos:

- Un Author puede tener múltiples Quotes (relación uno a muchos)
- Una Quote puede tener múltiples Tags, y un Tag puede estar asociado a múltiples Quotes (relación muchos a muchos a través de QuoteTag)

Estos modelos permiten una estructura de datos flexible y eficiente para almacenar y recuperar citas, autores y etiquetas, facilitando las operaciones de filtrado y búsqueda en la aplicación.

## 7. Vistas y URLs (endpoints)

1. Lista de citas (quote_list.html)
    - URL: `/`
    - Vista: `quote_list`
2. Detalle del autor (author_detail.html)
    - URL: `/author/<int:author_id>/`
    - Vista: `author_detail`
3. Detalle de la etiqueta (tag_detail.html)
    - URL: `/tag/<int:tag_id>/`
    - Vista: `tag_detail`
4. Página "Acerca de" (about.html)
    - URL: `/about/`
    - Vista: `about`
5. Plantilla base (base.html)
    - Esta es una plantilla base que es extendida por las otras plantillas (con los elementos comunes como la barra de navegación y la carga de los css y js).

Además, hay vistas adicionales para las visualizaciones de datos:

- URL: `/tag-distribution/`
Vista: `generate_tag_distribution_chart`
- URL: `/author-distribution/`
Vista: `generate_author_distribution_chart`
- URL: `/author-decade-distribution/`
Vista: `generate_author_decade_distribution_chart`

## 8. Visualización de Datos

- Gráfico de distribución de etiquetas

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/fd601164-f93c-4e8c-811f-4ddad4d5af3e/222e4d1d-1033-4aab-87e6-b82a377c898d/Untitled.png)

- Gráfico de distribución de autores

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/fd601164-f93c-4e8c-811f-4ddad4d5af3e/0766d446-5ee3-4acd-9a57-dd96cd64e805/Untitled.png)

- Gráfico de distribución de autores por década

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/fd601164-f93c-4e8c-811f-4ddad4d5af3e/0af025ad-e0b6-474c-8cd0-df68b8262b21/Untitled.png)

## 9. Test

### Estrategia de pruebas

El proyecto utiliza la biblioteca unittest de Python para realizar pruebas unitarias. Las pruebas se centran en el componente de web scraping, cubriendo diferentes aspectos como la extracción de datos, el manejo de diferentes formatos y el comportamiento en distintos escenarios.

### Tests implementados

1. `test_scrape_quotes_success`: Verifica la extracción correcta de citas, autores y etiquetas.
2. `test_scrape_author_info_success`: Comprueba la extracción de información del autor.
3. `test_convert_date`: Prueba la función de conversión de fechas.
4. `test_scrape_quotes_no_quotes`: Verifica el comportamiento cuando no hay citas para extraer.

### Ejecución de pruebas

Para ejecutar todas las pruebas:

```
python manage.py test
```

Para ejecutar un test específico:

```
python manage.py test quotes.tests.TestWebScraper.test_scrape_quotes_success
```

### Escribir nuevas pruebas

Al agregar nuevas funcionalidades, se deben escribir pruebas correspondientes. Seguir el patrón existente en el archivo de pruebas:

1. Importar las dependencias necesarias.
2. Crear una nueva función de prueba dentro de la clase `TestWebScraper`.
3. Usar mocks para simular respuestas HTTP si es necesario.
4. Verificar el comportamiento esperado usando aserciones.

## 10. Despliegue

### Despliegue con Docker

El proyecto está configurado para ser desplegado utilizando Docker y Docker Compose, lo que facilita la configuración del entorno y asegura la consistencia entre desarrollo y producción.

### Prerequisitos

- Docker
- Docker Compose

### Archivos de configuración

1. Dockerfile:

```
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

1. docker-compose.yml:

```yaml
version: '3.8'

services:
  web:
    build: .
    command: ["wait-for-it", "db:3306", "-t", "60", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3307:3306"

volumes:
  mysql_data:
```

### Proceso de despliegue

1. Asegúrate de tener un archivo `.env` en la raíz del proyecto con las variables de entorno necesarias:
    
    ```
    DB_NAME=nombre_de_tu_base_de_datos
    MYSQL_ROOT_PASSWORD=tu_contraseña_segura
    
    ```
    
2. Construye las imágenes de Docker:
    
    ```
    docker-compose build
    ```
    
3. Inicia los contenedores:
    
    ```
    docker-compose up -d
    ```
    
4. Ejecuta las migraciones de Django:
    
    ```
    docker-compose exec -it webscraping_angelmaria-web-1 /bin/bash 
    
    python manage.py migrate
    ```
    
5. Crea un superusuario (opcional):
    
    ```
    docker-compose exec web python manage.py createsuperuser
    ```
    
6. Accede a la aplicación en `http://localhost:8000`

### Notas importantes:

- El servicio web espera a que la base de datos esté lista antes de iniciar, gracias al script `wait-for-it.sh`.
- Los datos de MySQL se persisten en un volumen Docker (`mysql_data`).
- Para producción, considera cambiar el comando en el Dockerfile para usar Gunicorn en lugar del servidor de desarrollo de Django.

### Mantenimiento y actualizaciones

- Para aplicar cambios en el código, construye las imagenes si no existen o si han cambiado, inicia los contenedores y muestra los logs en la consola actual:
    
    ```
    docker-compose up --build
    ```
    
- Para ejecutar comandos de Django (como `collectstatic`), -crucial para el despliegue en producción- usa:
    
    ```
    docker-compose exec web python manage.py collectstatic
    ```
    

### Monitoreo

- Revisa los logs de los contenedores con:
    
    ```
    docker-compose logs
    
    ```
    
- Para un contenedor específico:
    
    ```
    docker-compose logs nombre-del-contenedor
    
    ```
    

Este enfoque de despliegue con Docker proporciona un entorno consistente y fácil de configurar, facilitando el desarrollo y el despliegue de la aplicación.

## 11. Mantenimiento y Actualizaciones

### Tareas programadas

- La actualización diaria de citas está configurada en `update_quotes.py`:
    
    ```python
    def schedule_jobs(self):
        # Schedule the job to run daily at midnight
        schedule.every().day.at("00:00").do(self.run_update)
    ```
    
- Considerar usar un sistema de tareas más robusto como Celery para producción

### Monitoreo y registro

- Configurar un sistema de logging para registrar errores y actividades importantes
- Utilizar herramientas de monitoreo como Sentry o New Relic para seguimiento en tiempo real

### Estrategia de respaldo

- Configurar copias de seguridad diarias de la base de datos
- Almacenar copias de seguridad en una ubicación segura y remota
- Probar regularmente la restauración de copias de seguridad

### Actualizaciones de dependencias

- Revisar y actualizar regularmente las dependencias del proyecto
- Probar exhaustivamente después de cada actualización

## 12. Solución de Problemas

### Problemas comunes y sus soluciones

- Error de conexión al scraper: Verificar la conectividad a internet y el estado del sitio web objetivo
- Errores de base de datos: Comprobar la conexión y los permisos de la base de datos
- Errores de importación de módulos: Verificar que todas las dependencias estén instaladas correctamente

### Consejos de depuración

- Utilizar logging extensivo para rastrear el flujo de ejecución
- Usar herramientas de depuración de Django como Django Debug Toolbar
- Configurar alertas para errores críticos

## 13. Mejoras Futuras

- Implementar autenticación de usuarios para personalizar la experiencia
- Añadir funcionalidad de búsqueda avanzada de citas
- Mejorar las visualizaciones de datos con gráficos interactivos
- Desplegar la aplicación en una plataforma cloud como AWS Elastic Beanstalk o Google Cloud Platform para mejorar la escalabilidad y confiabilidad

## 14. Contribución

### Pautas para contribuir al proyecto

- Fork el repositorio y cree una nueva rama para su función o corrección
- Siga las convenciones de código existentes
- Escriba pruebas para cualquier nueva funcionalidad
- Asegúrese de que todas las pruebas pasen antes de enviar un pull request
- Documente cualquier cambio en el README o la documentación relevante

### Proceso de pull request

1. Crear un fork del repositorio
2. Clonar su fork localmente
3. Crear una nueva rama para su función
4. Hacer cambios y commit
5. Empujar los cambios a su fork
6. Crear un pull request desde su fork al repositorio principal

## 15. Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulte el archivo `LICENSE` en el repositorio para obtener el texto completo de la licencia.

La Licencia MIT es una licencia de software permisiva que permite la reutilización del software dentro de software propietario siempre que se incluya el texto de la licencia. Es compatible con muchas licencias copyleft, como la GNU General Public License.

## 16. Información de Contacto
`Angel Maria Martinez Allue

https://www.linkedin.com/in/angelmariamartinez/`

