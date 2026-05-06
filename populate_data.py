
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obrador.settings')
django.setup()

from shop.models import Categoria, Producto, Alergeno

def populate():
    # Crear Alérgenos
    alergeno_data = [
        ("Gluten", "fas fa-seedling"),
        ("Lácteos", "fas fa-cheese"),
        ("Frutos Secos", "fas fa-cookie"),
        ("Huevos", "fas fa-egg"),
    ]
    
    alergenos_obj = {}
    for nombre, icono in alergeno_data:
        alg, created = Alergeno.objects.update_or_create(nombre=nombre, defaults={'icono': icono})
        alergenos_obj[nombre] = alg

    categories = [
        "Panadería Tradicional",
        "Panes Especiales / Saludables",
        "Bollería Dulce",
        "Pastelería y Tartas",
        "Salados",
        "Bebidas y Complementos"
    ]

    for cat_name in categories:
        Categoria.objects.get_or_create(nombre=cat_name)

    images = {
        "pan_blanco": "/static/productos/pan_blanco.jpg",
        "baguette": "/static/productos/baguette.jpg",
        "pan_integral": "/static/productos/pan_integral.jpg",
        "pan_masa_madre": "/static/productos/pan_masa_madre.jpg",
        "pan_centeno": "/static/productos/pan_centeno.jpg",
        "pan_multicereal": "/static/productos/pan_multicereal.jpg",
        "pan_espinacas": "/static/productos/pan_espinacas.png",
        "pan_avena": "/static/productos/pan_integral.jpg",
        "pan_sesamo": "/static/productos/pan_sesamo.png",
        "pan_semillas": "/static/productos/pan_semillas.png",
        
        "croissant": "/static/productos/croissant.png",
        "napolitana": "/static/productos/napolitana.jpg",
        "caracola": "/static/productos/caracola_pasas.png",
        "palmera": "/static/productos/palmera.jpg",
        "ensaimada": "/static/productos/ensaimada.jpg",
        
        "tarta_queso": "/static/productos/tarta_queso.jpg",
        "tarta_manzana": "/static/productos/tarta_manzana.jpg",
        "tarta_chocolate": "/static/productos/tarta_chocolate.jpg",
        "red_velvet": "/static/productos/red_velvet.png",
        "tarta_zanahoria": "/static/productos/tarta_zanahoria.jpg",
        
        "empanada": "/static/productos/empanada_atun.jpg",
        "empanadilla": "/static/productos/empanadilla_carne.jpg",
        "quiche": "/static/productos/quiche.jpg",
        "croquetas": "/static/productos/croquetas.jpg",
        "saladitos_surtidos": "/static/productos/saladitos_surtidos.jpg",
        
        "zumo_naranja": "/static/productos/zumo_naranja.jpg",
        "cafe": "/static/productos/cafe.jpg",
        "infusion": "/static/productos/infusion.jpg",
        "agua": "/static/productos/agua.jpg",
        "batido": "/static/productos/batido.jpg",
    }

    products_data = [
        # (Nombre, Precio, Categoría, URL, Descripción, Lista_Alérgenos)
        ("Pan blanco", 2.00, "Panadería Tradicional", images["pan_blanco"], "", ["Gluten"]),
        ("Pan integral", 2.20, "Panadería Tradicional", images["pan_integral"], "El pan integral se elabora con harina que aprovecha el grano entero...", ["Gluten"]),
        ("Pan de centeno", 3.00, "Panadería Tradicional", images["pan_centeno"], "", ["Gluten"]),
        ("Pan de masa madre", 3.50, "Panadería Tradicional", images["pan_masa_madre"], "", ["Gluten"]),
        ("Pan multicereal", 2.30, "Panadería Tradicional", images["pan_multicereal"], "", ["Gluten"]),
        ("Baguette", 0.80, "Panadería Tradicional", images["baguette"], "", ["Gluten"]),
        
        ("Pan de espelta", 3.50, "Panes Especiales / Saludables", images["pan_centeno"], "", ["Gluten"]),
        ("Pan de sésamo", 2.80, "Panes Especiales / Saludables", images["pan_sesamo"], "", ["Gluten", "Frutos Secos"]),
        ("Pan de semillas", 3.20, "Panes Especiales / Saludables", images["pan_semillas"], "", ["Gluten", "Frutos Secos"]),
        ("Pan de avena", 3.00, "Panes Especiales / Saludables", images["pan_avena"], "", ["Gluten"]),
        ("Pan de espinacas", 3.80, "Panes Especiales / Saludables", images["pan_espinacas"], "", ["Gluten"]),
        
        ("Croissant", 1.50, "Bollería Dulce", images["croissant"], "", ["Gluten", "Lácteos", "Huevos"]),
        ("Napolitana de chocolate", 1.80, "Bollería Dulce", images["napolitana"], "", ["Gluten", "Lácteos", "Huevos"]),
        ("Caracola de pasas", 1.70, "Bollería Dulce", images["caracola"], "", ["Gluten", "Lácteos", "Huevos"]),
        ("Palmera de hojaldre", 2.00, "Bollería Dulce", images["palmera"], "", ["Gluten", "Lácteos"]),
        ("Ensaimada", 2.20, "Bollería Dulce", images["ensaimada"], "", ["Gluten", "Lácteos", "Huevos"]),
        
        ("Tarta de queso", 15.00, "Pastelería y Tartas", images["tarta_queso"], "", ["Gluten", "Lácteos", "Huevos"]),
        ("Tarta de manzana", 12.00, "Pastelería y Tartas", images["tarta_manzana"], "", ["Gluten", "Lácteos", "Huevos"]),
        ("Tarta de chocolate", 18.00, "Pastelería y Tartas", images["tarta_chocolate"], "", ["Gluten", "Lácteos", "Huevos", "Frutos Secos"]),
        ("Tarta Red Velvet", 20.00, "Pastelería y Tartas", images["red_velvet"], "", ["Gluten", "Lácteos", "Huevos"]),
        ("Tarta de zanahoria", 16.00, "Pastelería y Tartas", images["tarta_zanahoria"], "", ["Gluten", "Lácteos", "Huevos", "Frutos Secos"]),
        
        ("Empanada de atún", 12.00, "Salados", images["empanada"], "", ["Gluten", "Huevos"]),
        ("Empanadilla de carne", 1.50, "Salados", images["empanadilla"], "", ["Gluten", "Huevos"]),
        ("Quiche de jamón y queso", 4.50, "Salados", images["quiche"], "", ["Gluten", "Lácteos", "Huevos"]),
        ("Croquetas de la casa", 6.00, "Salados", images["croquetas"], "Deliciosas croquetas caseras recién hechas.", ["Gluten", "Lácteos", "Huevos"]),
        ("Surtido de Saladitos", 1.20, "Salados", images["saladitos_surtidos"], "Variedad de bocaditost de hojaldre salado.", ["Gluten"]),
        
        ("Zumo de naranja", 2.50, "Bebidas y Complementos", images["zumo_naranja"], "", []),
        ("Café con leche", 1.80, "Bebidas y Complementos", images["cafe"], "", ["Lácteos"]),
        ("Infusión de manzanilla", 1.50, "Bebidas y Complementos", images["infusion"], "", []),
        ("Agua mineral", 1.00, "Bebidas y Complementos", images["agua"], "", []),
        ("Batido de chocolate", 2.50, "Bebidas y Complementos", images["batido"], "", ["Lácteos"]),
    ]

    for nombre, precio, cat_name, url, desc, alergs in products_data:
        cat = Categoria.objects.get(nombre=cat_name)
        p, created = Producto.objects.update_or_create(
            nombre=nombre,
            defaults={'precio': precio, 'categoria': cat, 'stock': 10, 'imagen_url': url, 'descripcion': desc}
        )
        
        # Update allergens
        p.alergenos.clear()
        for al_name in alergs:
            if al_name in alergenos_obj:
                p.alergenos.add(alergenos_obj[al_name])
                
        print(f"Sincronizado: {nombre}")

    # Prune extra products
    current_names = [p[0] for p in products_data]
    deleted_count, _ = Producto.objects.exclude(nombre__in=current_names).delete()
    if deleted_count:
        print(f"Eliminados {deleted_count} productos obsoletos (incluyendo Saladito de lomo)")

    # Create admin if it doesn't exist
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        print("Superusuario 'admin' creado correctamente.")
    else:
        print("El superusuario 'admin' ya existe.")

if __name__ == '__main__':
    populate()
