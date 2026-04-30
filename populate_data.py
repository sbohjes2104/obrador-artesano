
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obrador.settings')
django.setup()

from shop.models import Categoria, Producto

def populate():
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

    # Unsplash image IDs (Verificados por subagente y en formato LARGO)
    images = {
        # Breads
        "white_bread": "1592029780368-c1fff15bcfd5",
        "baguette": "1622808516114-02a5749cd965",
        "whole_wheat": "1509440159596-0249088772ff",
        "sourdough": "1613396874083-2d5fbe59ae79",
        "rye": "1586444248902-2f64eddc13df",
        "multicereal": "1549931319-a545dcf3bc73",
        "spinach": "1593851109529-cfa995ea1a7e",
        "oat": "1509440159596-0249088772ff", # Reuso bread por ahora 
        "seeds": "1534422298391-e4f8c172dddb",
        
        # Pastries & Sweets
        "croissant": "1712723247648-64a03ba7c333",
        "napolitana": "1483695028939-5bb13f8648b0",
        "palmera": "1647544301399-e1ca56c34551",
        "ensaimada": "1649308401368-a68b77116605",
        "caracola": "1608198093002-3bcc9170e945", # Old long format
        
        # Cakes & Pies
        "cheesecake": "1533134242443-d4fd215305ad",
        "apple_pie": "1621743478914-cc8a86d7e7b5",
        "chocolate_cake": "1606890737304-57a1ca8a5b62",
        "carrot_cake": "1676300186098-9b5ae9916e3c",
        "red_velvet": "1586799011740-08d4e92a2a0d",
        
        # Savory & Drinks
        "empanada": "1624128082323-beb6b8b508db",
        "empanadilla": "1624128082323-beb6b8b508db", # Reuso empanada
        "quiche": "1513104890138-7c749659a591",
        "jamon": "1557221016-f81ec6b1a46b",
        "orange_juice": "1600271886742-f049cd451bba",
        "tea": "1610478506025-8110cc8f1986",
        "milkshake": "1572490122747-3968b75cc699",
        "coffee": "1509042239860-f550ce710b93",
        "water": "1548839140-29a749e1cf4d",
    }

    def get_url(key):
        return f"https://images.unsplash.com/photo-{images.get(key, '1592029780368-c1fff15bcfd5')}?q=80&w=400"

    products_data = [
        ("Pan blanco", 2.00, "Panadería Tradicional", get_url("white_bread")),
        ("Pan integral", 2.20, "Panadería Tradicional", get_url("whole_wheat")),
        ("Pan de centeno", 3.00, "Panadería Tradicional", get_url("rye")),
        ("Pan de masa madre", 3.50, "Panadería Tradicional", get_url("sourdough")),
        ("Pan multicereal", 2.30, "Panadería Tradicional", get_url("multicereal")),
        ("Baguette", 0.80, "Panadería Tradicional", get_url("baguette")),
        
        ("Pan de espelta", 3.50, "Panes Especiales / Saludables", get_url("rye")),
        ("Pan de sésamo", 2.80, "Panes Especiales / Saludables", get_url("seeds")),
        ("Pan de semillas", 3.20, "Panes Especiales / Saludables", get_url("seeds")),
        ("Pan de avena", 3.00, "Panes Especiales / Saludables", get_url("oat")),
        ("Pan de espinacas", 3.80, "Panes Especiales / Saludables", get_url("spinach")),
        
        ("Croissant", 1.50, "Bollería Dulce", get_url("croissant")),
        ("Napolitana de chocolate", 1.80, "Bollería Dulce", get_url("napolitana")),
        ("Caracola de pasas", 1.70, "Bollería Dulce", get_url("caracola")),
        ("Palmera de hojaldre", 2.00, "Bollería Dulce", get_url("palmera")),
        ("Ensaimada", 2.20, "Bollería Dulce", get_url("ensaimada")),
        
        ("Tarta de queso", 15.00, "Pastelería y Tartas", get_url("cheesecake")),
        ("Tarta de manzana", 12.00, "Pastelería y Tartas", get_url("apple_pie")),
        ("Tarta de chocolate", 18.00, "Pastelería y Tartas", get_url("chocolate_cake")),
        ("Tarta Red Velvet", 20.00, "Pastelería y Tartas", get_url("red_velvet")),
        ("Tarta de zanahoria", 16.00, "Pastelería y Tartas", get_url("carrot_cake")),
        
        ("Empanada de atún", 12.00, "Salados", get_url("empanada")),
        ("Empanadilla de carne", 1.50, "Salados", get_url("empanadilla")),
        ("Quiche de jamón y queso", 4.50, "Salados", get_url("quiche")),
        ("Croquetas de la casa", 6.00, "Salados", get_url("empanada")),
        ("Saladito de lomo", 1.20, "Salados", get_url("jamon")),
        
        ("Zumo de naranja", 2.50, "Bebidas y Complementos", get_url("orange_juice")),
        ("Café con leche", 1.80, "Bebidas y Complementos", get_url("coffee")),
        ("Infusión de manzanilla", 1.50, "Bebidas y Complementos", get_url("tea")),
        ("Agua mineral", 1.00, "Bebidas y Complementos", get_url("water")),
        ("Batido de chocolate", 2.50, "Bebidas y Complementos", get_url("milkshake")),
    ]

    for nombre, precio, cat_name, url in products_data:
        cat = Categoria.objects.get(nombre=cat_name)
        Producto.objects.update_or_create(
            nombre=nombre,
            defaults={'precio': precio, 'categoria': cat, 'stock': 10, 'imagen_url': url}
        )
        print(f"Sincronizado: {nombre}")

if __name__ == '__main__':
    populate()
