
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
        "pan_blanco": "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?q=80&w=800",
        "baguette": "https://images.unsplash.com/photo-1597079910443-60c43fc4f729?q=80&w=800",
        "pan_integral": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=800",
        "pan_masa_madre": "https://images.unsplash.com/photo-1585478259715-876a6a8cffcc?q=80&w=800",
        "pan_centeno": "https://images.unsplash.com/photo-1603532648955-0393a0b4edbd?q=80&w=800",
        "pan_multicereal": "https://images.unsplash.com/photo-1555951015-6da899b5c2cd?q=80&w=800",
        "pan_espinacas": "https://images.unsplash.com/photo-1533130061792-64b345e4a833?q=80&w=800",
        "pan_avena": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=800",
        "pan_sesamo": "https://images.unsplash.com/photo-1555951015-6da899b5c2cd?q=80&w=800",
        "pan_semillas": "https://images.unsplash.com/photo-1603532648955-0393a0b4edbd?q=80&w=800",
        
        "croissant": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=800",
        "napolitana": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?q=80&w=800",
        "caracola": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=800",
        "palmera": "https://images.unsplash.com/photo-1530610476181-d83430b64dcd?q=80&w=800",
        "ensaimada": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=800",
        
        "tarta_queso": "https://images.unsplash.com/photo-1524351199679-46cddf302c31?q=80&w=800",
        "tarta_manzana": "https://images.unsplash.com/photo-1568571780765-9276ac8b75a2?q=80&w=800",
        "tarta_chocolate": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?q=80&w=800",
        "red_velvet": "https://images.unsplash.com/photo-1586788680434-30d324b2d46f?q=80&w=800",
        "tarta_zanahoria": "https://images.unsplash.com/photo-1622920453303-34e8e19c0827?q=80&w=800",
        
        "empanada": "https://images.unsplash.com/photo-1628192134724-40e38a4cd33a?q=80&w=800",
        "empanadilla": "https://images.unsplash.com/photo-1628192134724-40e38a4cd33a?q=80&w=800",
        "quiche": "https://images.unsplash.com/photo-1612392166886-ee8475b03af2?q=80&w=800",
        "croquetas": "https://images.unsplash.com/photo-1612392062631-94dd858cba88?q=80&w=800",
        "saladitos_surtidos": "https://images.unsplash.com/photo-1628192134724-40e38a4cd33a?q=80&w=800",
        
        "zumo_naranja": "https://images.unsplash.com/photo-1547514701-42782101795e?q=80&w=800",
        "cafe": "https://images.unsplash.com/photo-1541167760496-162956ed836f?q=80&w=800",
        "infusion": "https://images.unsplash.com/photo-1571935443242-c1a1a79aa7c8?q=80&w=800",
        "agua": "https://images.unsplash.com/photo-1548839140-29a749e1cf3d?q=80&w=800",
        "batido": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?q=80&w=800",
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
