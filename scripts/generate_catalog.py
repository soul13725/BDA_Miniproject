import json
import random
import os
from pathlib import Path

# Fix seed for reproducibility
random.seed(42)

CATEGORIES_MAP = {
    "Electronics": ["Televisions", "Home Audio", "Headphones", "Speakers", "Cameras", "Projectors", "Electronic Devices", "Cables"],
    "Computers": ["Laptops", "Desktop Computers", "Monitors", "Keyboards", "Mice", "Printers", "Storage Devices", "Routers"],
    "Mobile Phones": ["Smartphones", "Feature Phones", "Power Banks", "Phone Cases", "Wireless Chargers"],
    "Gadgets": ["Smartwatches", "Fitness Trackers", "Smart Bands", "Smart Glasses", "Portable Gadgets"],
    "Gaming": ["Gaming Consoles", "Game Controllers", "Gaming Headsets", "PC Games", "Console Games"],
    "Toys": ["Educational Toys", "Building Blocks", "Action Figures", "Plush Toys", "Outdoor Toys"],
    "Games & Puzzles": ["Board Games", "Card Games", "Strategy Games", "Jigsaw Puzzles", "Party Games"],
    "Groceries": ["Rice", "Pulses", "Cooking Oils", "Spices", "Snacks", "Cereals", "Pasta", "Sauces"],
    "Beverages": ["Tea", "Coffee", "Juices", "Soft Drinks", "Energy Drinks"],
    "Snacks & Confectionery": ["Biscuits", "Chips", "Chocolates", "Candy", "Popcorn"],
    "Dairy & Breakfast": ["Milk Products", "Cheese", "Butter", "Breakfast Cereals", "Oats"],
    "Fresh Food": ["Fruits", "Vegetables", "Fresh Produce", "Bakery"],
    "Apparel": ["Men's Clothing", "Women's Clothing", "Kids Clothing", "Winter Wear", "Activewear"],
    "Footwear": ["Men's Shoes", "Women's Shoes", "Sports Shoes", "Casual Shoes", "Sandals", "Boots"],
    "Jewellery": ["Fine Jewellery", "Fashion Jewellery", "Earrings", "Necklaces", "Rings"],
    "Watches": ["Analog Watches", "Digital Watches", "Luxury Watches", "Sports Watches"],
    "Beauty": ["Makeup", "Foundation", "Lip Products", "Eye Makeup"],
    "Skincare": ["Face Wash", "Moisturizers", "Sunscreen", "Face Masks"],
    "Haircare": ["Shampoo", "Conditioner", "Hair Oil", "Hair Styling"],
    "Personal Care": ["Bath Products", "Soaps", "Body Wash", "Deodorants", "Fragrances", "Oral Care"],
    "Personal Care Appliances": ["Hair Dryers", "Trimmers", "Shavers", "Massagers"],
    "Health & Wellness": ["Vitamins", "Health Supplements", "Fitness Supplements", "First Aid"],
    "Baby Products": ["Diapers", "Baby Wipes", "Baby Clothing", "Strollers", "Baby Toys"],
    "Home": ["Home Organization", "Storage", "Household Accessories", "Home Essentials"],
    "Furniture": ["Sofas", "Beds", "Tables", "Chairs", "Desks", "Office Furniture"],
    "Home Decor": ["Wall Art", "Clocks", "Cushions", "Rugs", "Curtains"],
    "Kitchen": ["Cookware", "Pressure Cookers", "Kitchen Tools", "Containers", "Tableware"],
    "Kitchen Appliances": ["Mixers", "Blenders", "Microwaves", "Ovens", "Coffee Machines"],
    "Large Appliances": ["Refrigerators", "Washing Machines", "Air Conditioners", "Water Heaters"],
    "Home Cleaning": ["Laundry Products", "Detergents", "Floor Cleaners", "Cleaning Tools"],
    "Home Improvement": ["Hand Tools", "Power Tools", "Hardware", "Electrical Supplies"],
    "Lighting": ["LED Bulbs", "Ceiling Lights", "Table Lamps", "Smart Lights"],
    "Garden & Outdoor": ["Gardening Tools", "Planters", "Seeds", "Outdoor Furniture"],
    "Sports": ["Cricket", "Football", "Tennis", "Badminton", "Swimming"],
    "Fitness": ["Dumbbells", "Yoga Mats", "Exercise Equipment", "Treadmills", "Fitness Accessories"],
    "Outdoor & Camping": ["Tents", "Sleeping Bags", "Hiking Gear", "Backpacks"],
    "Automotive": ["Car Accessories", "Bike Accessories", "Helmets", "Vehicle Cleaning"],
    "Travel & Luggage": ["Suitcases", "Trolleys", "Duffel Bags", "Travel Accessories"],
    "Pet Supplies": ["Dog Food", "Cat Food", "Pet Toys", "Pet Beds"],
    "Books": ["Fiction", "Non-Fiction", "Academic Books", "Business Books", "Self-Development"],
    "Office Products": ["Office Supplies", "Notebooks", "Writing Supplies", "Organizers"],
    "School & Stationery": ["Pens", "Pencils", "Art Supplies", "School Bags", "Markers"],
    "Musical Instruments": ["Guitars", "Keyboards", "Pianos", "Drums", "Microphones"],
    "Arts & Crafts": ["Painting", "Sketching", "Craft Kits", "DIY Kits"],
    "Luggage & Bags": ["Handbags", "Wallets", "Laptop Bags", "Sling Bags"],
    "Security": ["Safes", "Locks", "Security Cameras", "Alarm Systems"],
    "Smart Home": ["Smart Plugs", "Smart Bulbs", "Smart Locks", "Smart Cameras"],
    "Software & Digital Products": ["Productivity Software", "Security Software", "Digital Subscriptions"],
    "Movies & Entertainment": ["Movies", "Music", "Collectibles", "Digital Entertainment"],
    "Collectibles & Hobbies": ["Model Kits", "Hobby Kits", "Trading Items"],
    "Gifting": ["Gift Sets", "Greeting Cards", "Personalized Gift Simulation"],
    "Religious & Festival Products": ["Pooja Essentials", "Diyas", "Festival Decorations"],
    "Consumables": ["Everyday Consumables", "Household Consumables", "Office Consumables"]
}

CITIES = [
    "Mumbai", "Pune", "Nashik", "Nagpur", "Thane", "Aurangabad", "Bengaluru", "Mysuru", 
    "Mangaluru", "Chennai", "Coimbatore", "Madurai", "Hyderabad", "Visakhapatnam", 
    "Vijayawada", "Delhi", "New Delhi", "Noida", "Gurugram", "Ghaziabad", "Faridabad", 
    "Kolkata", "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Jaipur", "Jodhpur", "Udaipur", 
    "Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj", "Meerut", "Chandigarh", "Amritsar", 
    "Ludhiana", "Bhopal", "Indore", "Patna", "Ranchi", "Bhubaneswar", "Guwahati", "Dehradun", 
    "Raipur", "Kochi", "Thiruvananthapuram", "Kozhikode", "Tirupati", "Navi Mumbai", 
    "Vasai-Virar", "Jamshedpur", "Dhanbad", "Srinagar", "Jammu"
]

def generate_catalog():
    catalog_dir = Path("data/catalog")
    catalog_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Cities
    cities_list = []
    for city in set(CITIES):
        # assign weights - metros higher
        weight = 5 if city in ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune"] else random.randint(1, 3)
        cities_list.append({"city_name": city, "demand_weight": weight})
    
    with open(catalog_dir / "cities.json", "w", encoding="utf-8") as f:
        json.dump(cities_list, f, indent=2)

    # 2. Categories
    categories_list = []
    for cat in CATEGORIES_MAP.keys():
        weight = random.randint(1, 10)
        categories_list.append({"category_name": cat, "demand_weight": weight})
    
    with open(catalog_dir / "categories.json", "w", encoding="utf-8") as f:
        json.dump(categories_list, f, indent=2)

    # 3. Products
    products_list = []
    pid_counter = 1
    
    class_rules = {
        "Groceries": "Convenience",
        "Beverages": "Convenience",
        "Snacks & Confectionery": "Convenience",
        "Dairy & Breakfast": "Convenience",
        "Fresh Food": "Convenience",
        "Home Cleaning": "Convenience",
        "Consumables": "Convenience",
        
        "Electronics": "Shopping",
        "Computers": "Shopping",
        "Mobile Phones": "Shopping",
        "Apparel": "Shopping",
        "Footwear": "Shopping",
        "Furniture": "Shopping",
        "Large Appliances": "Shopping",
        "Kitchen Appliances": "Shopping",
        
        "Jewellery": "Specialty",
        "Watches": "Specialty",
        "Musical Instruments": "Specialty",
        "Collectibles & Hobbies": "Specialty",
        
        "Security": "Unsought",
        "Health & Wellness": "Unsought",
        "Home Improvement": "Unsought",
        "Automotive": "Unsought"
    }

    for cat, subcats in CATEGORIES_MAP.items():
        base_class = class_rules.get(cat, "Shopping")
        
        # generate 10-30 products per category
        num_products = random.randint(10, 30)
        for _ in range(num_products):
            subcat = random.choice(subcats)
            
            # Determine product class with some variation
            p_class = base_class
            if random.random() < 0.1: # 10% chance of variance
                p_class = random.choice(["Convenience", "Shopping", "Specialty", "Unsought"])
                
            # Price generation based on class
            if p_class == "Convenience":
                price = round(random.uniform(10.0, 500.0), 2)
            elif p_class == "Shopping":
                price = round(random.uniform(500.0, 15000.0), 2)
            elif p_class == "Specialty":
                price = round(random.uniform(5000.0, 100000.0), 2)
            else: # Unsought
                price = round(random.uniform(100.0, 5000.0), 2)
                
            name_suffix = random.choice(["Pro", "Max", "Ultra", "Basic", "Premium", "Essential", "Plus", "V2", "Edition", "Pack", "Set"])
            brand = random.choice(["BrandA", "BrandB", "BrandC", "BrandD", "Generic"])
            product_name = f"{brand} {subcat} {name_suffix}"
            
            products_list.append({
                "product_id": f"PRD{str(pid_counter).zfill(5)}",
                "product_name": product_name,
                "category": cat,
                "subcategory": subcat,
                "product_class": p_class,
                "brand": brand,
                "unit_price": price,
                "demand_weight": random.randint(1, 10)
            })
            pid_counter += 1

    with open(catalog_dir / "products.json", "w", encoding="utf-8") as f:
        json.dump(products_list, f, indent=2)

    print(f"Catalog generated: {len(cities_list)} cities, {len(categories_list)} categories, {len(products_list)} products.")

if __name__ == "__main__":
    generate_catalog()
