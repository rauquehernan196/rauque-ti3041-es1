Documento de Uso de Inteligencia Artificial (uso_ia.md)

Parte 1: Registro de Consultas

Consulta 1
    Prompt: "¿Cómo puedo correr el server, cual el comando?"
    Resumen de la respuesta:** La IA indicó ejecutar el comando `python manage.py runserver` en la terminal para iniciar el servidor local de Django en la dirección `http://127.0.0.1:8000/`. Se ejecutó el comando directamente en la terminal de VS Code para verificar el despliegue del proyecto.

Consulta 2
    Prompt:** "De las primeras opciones cuál tomo si está así mi proyecto y no esta funcionando?  [Captura de pantalla con la estructura del proyecto y views.py]"
    Resumen de la respuesta:** La IA identificó que los datos se leían desde un archivo `datos.json` local (Opción B) y entregó el código ajustado para la vista `lista_productos` agregando el conteo de total de registros y stock disponible. Se copió la lógica de la función `lista_productos` en `catalogo/views.py` para procesar los datos del JSON y pasarlos al contexto del template.

Consulta 3
    Prompt:** "¿En el paso dos debo reemplazar todo?"
    Resumen de la respuesta:** Aclaró que no hacía falta rehacer el archivo, sino estructurar las tarjetas de productos e incorporar el cuadro resumen superior mediante clases de Bootstrap y condicionales en Jinja/Django template. Se utilizó la estructura de tarjetas HTML propuesta en `catalogo/templates/catalogo/lista.html`, adaptando las etiquetas de estado de stock y diseño de las cards.

Consulta 4
    Prompt:** "¿Por qué ahora se ve así? [Captura de pantalla de la página sin estilos CSS]"
    Resumen de la respuesta:** Diagnosticó que la falta de estilos se debía a que no estaba cargada la CDN de Bootstrap en la cabecera HTML del proyecto y entregó una plantilla base con los CDN de Bootstrap 5 incluidos. Se actualizó la plantilla `base.html` incorporando el enlace CDN de Bootstrap en la etiqueta `<head>` y la barra de navegación responsive.

Consulta 5
    Prompt:** "¿Puedes darme el JSON más las imagenes a los que los nombres hacen referencia para agilizar este proceso?
    Resumen de la respuesta:** La IA proporcionó la lista completa de 40 productos formateados en JSON con claves de ID, nombre, categoría, precio, stock y URLs de imágenes temáticas de herramientas. Se reemplazó por completo el contenido del archivo `catalogo/datos.json` con la nueva estructura provista.

Consulta 6
    Prompt:** "¿En qué parte va la última línea de código que me diste?"
    Resumen de la respuesta:** Muestra la posición exacta donde debe ubicarse la etiqueta `<img>` en `lista.html` (dentro de `.card` y justo arriba del `.card-body`).
    Lo que se utilizó o modificó:** Se insertó la etiqueta `<img src="{{ p.imagen }}" class="card-img-top">` en la ubicación señalada en `catalogo/templates/catalogo/lista.html`.

Consulta 7
    Prompt:** "crea un landing donde haya un breve resumen de la pagina y a que publico esta dirigido, que incluya un login funcional el cual tenga la opcion de ingresar como usuario normal y un super usuario o admin que maneje los stock, las cuentas de los que se vayan registrando. Separa el apartado cartalogo paraque me envie directamente y me enseñe todas las tarjetas con los productos una vez se seleccione."
    Resumen: 

Parte 2: Explicación del Proceso

En el desarrollo de este sitio web se utilizo la IA como apoyo y guia tecnica para resolver dudas puntuales y la organizacion, configuracion. Al principio se uso la IA para poder refrescar el como se inciaba o lanzaba el servidor, ya que, no habia revisado la plataforma de Inacap y ver que habia un Notion, alo que esta me dioi el comando directo `python manage.py runserver` y tambien principalmente que me ayude a estructurar la lectura de mi archibo `datos.json` en la vista de la palicacion, esta ayuda se pidio para ajustar la logica de conteo del resumen de productos y asegurar que la plantilla lo interprete correctamente 

Las respuestas sobre la lógica de Python en `views.py` y la solicitud del catálogo completo en `datos.json` me sirvieron tal cual fueron entregadas, ya que contaban con la estructura exacta de claves que requería mi proyecto reduciendo drasticamente el tiemo de desarrollo. Sin embargo, en la parte del diseño HTML tuve que realizar ajustes visuales; por ejemplo, al integrar el código de las tarjetas noté que los estilos no se aplicaban y swe veía de manera lateral sin estilos ni fuentes, lo que me llevó a consultar nuevamente para corregir la falta de la CDN de Bootstrap en la plantilla `base.html`. En el proceso aprendí a vincular recursos estáticos externamente mediante CDN, a manejar etiquetas condicionales de Django en los archivos HTML para resaltar elementos sin stock, y a ubicar correctamente los componentes dentro del modelo de cajas y tarjetas de Bootstrap.