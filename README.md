# Artesanía en cada bocado - Obrador Artesano Digital

## Proyecto de Fin de Ciclo Formativo de Grado Superior

### Definición del Proyecto
El presente proyecto surge de la necesidad urgente de digitalizar el comercio tradicional de panadería/pastelería, un sector que actualmente pierde competitividad frente a las grandes superficies debido a la falta de gestión de stock en tiempo real. 

La solución propuesta es una aplicación web que permite conectar la empresa con el cliente final. El proyecto se desarrolla en base a las necesidades reales del negocio: un catálogo digital administrable, gestión de usuarios y un sistema de pedidos para recogida en tienda, garantizando así la reserva de producto y minimizando el desperdicio alimentario.

---

## 🚀 Características Principales

- **Catálogo Digital Interactivo**: Exposición de productos organizada por categorías (Panes, Bollería, Tartas) con imágenes de alta calidad.
- **Gestión de Stock en Tiempo Real**: Control administrativo de existencias para evitar ventas sin stock físico.
- **Sistema de Usuarios y Autenticación**: Registro e inicio de sesión seguro para clientes y administradores.
- **Reserva de Pedidos (Click & Collect)**: Los usuarios pueden realizar su pedido online y recogerlo en el obrador físico.
- **Diseño Mobile-First**: Interfaz optimizada para su uso en dispositivos móviles, ofreciendo una experiencia elegante y profesional.

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django (Python)**: Framework de alto rendimiento utilizado por su arquitectura robusta y su sistema de administración nativo.

### Base de Datos
- **MySQL**: Base de datos relacional para garantizar la integridad referencial. El esquema ha sido normalizado hasta la **Tercera Forma Normal (3FN)**.

### Frontend
- **HTML5 y CSS3**: Implementación de una interfaz responsive sin dependencias externas pesadas, asegurando velocidad y control absoluto del diseño.
- **Google Fonts**: Playfair Display (Títulos) y Nunito (Cuerpo).

### Infraestructura y Despliegue
- **Docker & Docker-Compose**: Contenerización completa del entorno para asegurar la portabilidad y facilitar el despliegue tanto en desarrollo como en producción.

---

## 🏗️ Estructura de Datos (E-R)

El sistema se basa en las siguientes entidades principales:
1. **Categorías**: Clasificación de los productos del obrador.
2. **Productos**: Información detallada, precios y stock.
3. **Usuarios**: Gestión de clientes y personal administrativo.
4. **Pedidos e Inea de Pedidos**: Registro histórico y detalle de cada transacción.

---

## 📦 Instalación y Ejecución

Para poner en marcha el proyecto en un entorno local, sigue estos pasos:

1. **Clonar el repositorio**:
   ```bash
   git clone [URL-DEL-REPOSITORIO]
   cd obrador-artesano
   ```

2. **Levantar los contenedores**:
   ```bash
   docker-compose up --build -d
   ```

3. **Ejecutar migraciones**:
   ```bash
   docker-compose run web python manage.py migrate
   ```

4. **Crear usuario administrador**:
   ```bash
   docker-compose run web python manage.py createsuperuser
   ```

5. **Acceder a la aplicación**:
   - Web: `http://localhost:8000`
   - Admin: `http://localhost:8000/admin`

---

## 🎨 Diseño y UX/UI

El diseño fue concebido para transmitir la calidez de un obrador artesano tradicional, utilizando una paleta de colores tierra y chocolate, combinada con una tipografía serifa elegante que refuerza la calidad premium de nuestros productos.

---

**Desarrollado por Sergio Bohórquez Jesús - 2026**
