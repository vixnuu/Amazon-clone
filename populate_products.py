import os
import django
from django.core.files import File

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EkartProject.settings')
django.setup()

from ekartApp.models import Category, Products
from django.db.models import Count

# Get all categories
categories = Category.objects.all()
if not categories:
    print("No categories found. Please create categories first.")
    exit()

# Delete duplicate products (keep the first one)
duplicates = Products.objects.values('product_name', 'category').annotate(count=Count('id')).filter(count__gt=1)
for dup in duplicates:
    products_to_delete = Products.objects.filter(product_name=dup['product_name'], category=dup['category']).order_by('id')[1:]
    for product in products_to_delete:
        product.delete()
    print(f"Deleted {len(products_to_delete)} duplicate(s) for product '{dup['product_name']}' in category '{dup['category']}'")

# Sample product data for each category
product_data = {
    'Electronics': [
        {'name': 'Wireless Headphones', 'price': 199, 'description': 'High-quality wireless headphones with noise cancellation.'},
        {'name': 'Smartphone', 'price': 699, 'description': 'Latest smartphone with advanced features.'},
        {'name': 'Laptop', 'price': 999, 'description': 'Powerful laptop for work and gaming.'},
        {'name': 'Smart Watch', 'price': 299, 'description': 'Fitness tracking smart watch.'},
        {'name': 'Bluetooth Speaker', 'price': 79, 'description': 'Portable Bluetooth speaker with great sound.'},
        {'name': 'Tablet', 'price': 499, 'description': '10-inch tablet for entertainment and productivity.'},
        {'name': 'Gaming Mouse', 'price': 49, 'description': 'Ergonomic gaming mouse with RGB lighting.'},
        {'name': 'External Hard Drive', 'price': 89, 'description': '1TB external hard drive for data storage.'},
        {'name': 'Webcam', 'price': 39, 'description': 'HD webcam for video calls and streaming.'},
        {'name': 'Power Bank', 'price': 29, 'description': '10000mAh power bank for charging on the go.'},
        {'name': 'Wireless Charger', 'price': 39, 'description': 'Fast wireless charger for compatible devices.'},
        {'name': 'Action Camera', 'price': 249, 'description': 'Waterproof action camera for adventure filming.'},
    ],
    'Fashion': [
        {'name': 'Running Shoes', 'price': 129, 'description': 'Comfortable running shoes for athletes.'},
        {'name': 'Leather Jacket', 'price': 299, 'description': 'Stylish leather jacket for all seasons.'},
        {'name': 'Denim Jeans', 'price': 89, 'description': 'Classic blue denim jeans.'},
        {'name': 'Cotton T-Shirt', 'price': 19, 'description': 'Soft cotton t-shirt in various colors.'},
        {'name': 'Winter Coat', 'price': 199, 'description': 'Warm winter coat with fur lining.'},
        {'name': 'Sneakers', 'price': 79, 'description': 'Casual sneakers for everyday wear.'},
        {'name': 'Sunglasses', 'price': 49, 'description': 'UV protection sunglasses.'},
        {'name': 'Backpack', 'price': 59, 'description': 'Durable backpack for school or travel.'},
        {'name': 'Wrist Watch', 'price': 149, 'description': 'Elegant wrist watch for formal occasions.'},
        {'name': 'Baseball Cap', 'price': 15, 'description': 'Adjustable baseball cap.'},
        {'name': 'Handbag', 'price': 89, 'description': 'Stylish handbag for everyday use.'},
        {'name': 'Scarf', 'price': 25, 'description': 'Warm wool scarf for winter.'},
    ],
    ' Kitchen': [
        {'name': 'Coffee Maker', 'price': 89, 'description': 'Automatic coffee maker for fresh brews.'},
        {'name': 'Blender', 'price': 49, 'description': 'High-speed blender for smoothies.'},
        {'name': 'Microwave Oven', 'price': 149, 'description': 'Compact microwave oven.'},
        {'name': 'Vacuum Cleaner', 'price': 199, 'description': 'Powerful vacuum cleaner for home cleaning.'},
        {'name': 'Air Fryer', 'price': 99, 'description': 'Healthy air fryer for frying without oil.'},
        {'name': 'Toaster', 'price': 29, 'description': '4-slice toaster with adjustable settings.'},
        {'name': 'Electric Kettle', 'price': 39, 'description': 'Fast-boiling electric kettle.'},
        {'name': 'Dish Rack', 'price': 19, 'description': 'Stainless steel dish drying rack.'},
        {'name': 'Cutting Board Set', 'price': 24, 'description': 'Set of 3 bamboo cutting boards.'},
        {'name': 'Storage Containers', 'price': 14, 'description': 'Plastic storage containers with lids.'},
        {'name': 'Knife Set', 'price': 59, 'description': 'Professional chef knife set.'},
        {'name': 'Non-stick Pan', 'price': 34, 'description': 'Durable non-stick frying pan.'},
    ],
    'Books': [
        {'name': 'Python Programming', 'price': 39, 'description': 'Comprehensive guide to Python programming.'},
        {'name': 'Data Science Handbook', 'price': 49, 'description': 'Essential guide for data scientists.'},
        {'name': 'Web Development', 'price': 34, 'description': 'Learn modern web development techniques.'},
        {'name': 'Machine Learning', 'price': 59, 'description': 'Introduction to machine learning algorithms.'},
        {'name': 'Fiction Novel', 'price': 19, 'description': 'Bestselling fiction novel.'},
        {'name': 'Biography', 'price': 29, 'description': 'Inspiring biography of a great leader.'},
        {'name': 'Cookbook', 'price': 24, 'description': 'Delicious recipes from around the world.'},
        {'name': 'Self-Help Book', 'price': 16, 'description': 'Guide to personal development.'},
        {'name': 'History Book', 'price': 31, 'description': 'Fascinating history of ancient civilizations.'},
        {'name': 'Science Fiction', 'price': 22, 'description': 'Thrilling science fiction adventure.'},
        {'name': 'Mystery Novel', 'price': 27, 'description': 'Gripping mystery novel with unexpected twists.'},
        {'name': 'Travel Guide', 'price': 21, 'description': 'Comprehensive travel guide for explorers.'},
    ],
    'Sports & Outdoors': [
        {'name': 'Yoga Mat', 'price': 29, 'description': 'Non-slip yoga mat for exercise.'},
        {'name': 'Dumbbells Set', 'price': 79, 'description': 'Adjustable dumbbells for strength training.'},
        {'name': 'Tennis Racket', 'price': 89, 'description': 'Professional tennis racket.'},
        {'name': 'Camping Tent', 'price': 149, 'description': '4-person camping tent.'},
        {'name': 'Bicycle', 'price': 399, 'description': 'Mountain bike for outdoor adventures.'},
        {'name': 'Swimming Goggles', 'price': 14, 'description': 'Anti-fog swimming goggles.'},
        {'name': 'Football', 'price': 24, 'description': 'Official size football.'},
        {'name': 'Basketball', 'price': 39, 'description': 'Durable basketball for outdoor play.'},
        {'name': 'Hiking Boots', 'price': 119, 'description': 'Waterproof hiking boots.'},
        {'name': 'Fishing Rod', 'price': 69, 'description': 'Telescopic fishing rod.'},
        {'name': 'Skateboard', 'price': 89, 'description': 'Complete skateboard for beginners.'},
        {'name': 'Golf Clubs Set', 'price': 499, 'description': 'Full set of golf clubs.'},
        {'name': 'Running Shorts', 'price': 25, 'description': 'Lightweight running shorts.'},
    ],
    'Toys & Games': [
        {'name': 'Building Blocks', 'price': 49, 'description': 'Creative building blocks set.'},
        {'name': 'Board Game', 'price': 29, 'description': 'Fun family board game.'},
        {'name': 'Puzzle Set', 'price': 19, 'description': '500-piece jigsaw puzzle.'},
        {'name': 'Remote Control Car', 'price': 39, 'description': 'High-speed RC car.'},
        {'name': 'Stuffed Animal', 'price': 14, 'description': 'Soft plush teddy bear.'},
        {'name': 'Art Supplies', 'price': 24, 'description': 'Complete art set for kids.'},
        {'name': 'Educational Tablet', 'price': 79, 'description': 'Learning tablet for children.'},
        {'name': 'Doll House', 'price': 89, 'description': 'Beautiful doll house with furniture.'},
        {'name': 'Action Figures', 'price': 19, 'description': 'Set of superhero action figures.'},
        {'name': 'Musical Instruments', 'price': 34, 'description': 'Kids musical keyboard.'},
        {'name': 'Outdoor Playset', 'price': 199, 'description': 'Backyard playset with slide and swings.'},
        {'name': 'Kite', 'price': 15, 'description': 'Colorful outdoor kite.'},
    ],
    'Beauty & Personal Care': [
        {'name': 'Face Cream', 'price': 24, 'description': 'Moisturizing face cream.'},
        {'name': 'Shampoo', 'price': 12, 'description': 'Herbal shampoo for healthy hair.'},
        {'name': 'Lipstick', 'price': 19, 'description': 'Long-lasting matte lipstick.'},
        {'name': 'Perfume', 'price': 49, 'description': 'Elegant fragrance for women.'},
        {'name': 'Hair Dryer', 'price': 59, 'description': 'Professional hair dryer.'},
        {'name': 'Nail Polish Set', 'price': 14, 'description': 'Colorful nail polish collection.'},
        {'name': 'Makeup Brush Set', 'price': 29, 'description': 'Professional makeup brushes.'},
        {'name': 'Sunscreen', 'price': 16, 'description': 'SPF 50 sunscreen lotion.'},
        {'name': 'Body Lotion', 'price': 11, 'description': 'Hydrating body lotion.'},
        {'name': 'Hair Straightener', 'price': 39, 'description': 'Ceramic hair straightener.'},
        {'name': 'Makeup Remover', 'price': 18, 'description': 'Gentle makeup remover wipes.'},
        {'name': 'Facial Cleanser', 'price': 22, 'description': 'Deep cleansing facial wash.'},
    ],
    'Automotive': [
        {'name': 'Car Air Freshener', 'price': 8, 'description': 'Long-lasting car air freshener.'},
        {'name': 'Car Vacuum', 'price': 49, 'description': 'Handheld car vacuum cleaner.'},
        {'name': 'Tire Pressure Gauge', 'price': 12, 'description': 'Digital tire pressure gauge.'},
        {'name': 'Car Wax', 'price': 19, 'description': 'Premium car wax for shine.'},
        {'name': 'Jump Starter', 'price': 89, 'description': 'Portable car jump starter.'},
        {'name': 'Car Cover', 'price': 39, 'description': 'Weatherproof car cover.'},
        {'name': 'Seat Covers', 'price': 69, 'description': 'Universal car seat covers.'},
        {'name': 'GPS Navigator', 'price': 149, 'description': 'Touchscreen GPS device.'},
        {'name': 'Car Battery', 'price': 99, 'description': 'Heavy-duty car battery.'},
        {'name': 'Windshield Wipers', 'price': 24, 'description': 'Set of 2 windshield wipers.'},
        {'name': 'Dash Cam', 'price': 79, 'description': 'Full HD dash camera.'},
        {'name': 'Car Phone Mount', 'price': 15, 'description': 'Adjustable car phone holder.'},
    ],
    'Health & Wellness': [
        {'name': 'Vitamins', 'price': 29, 'description': 'Multivitamin supplement.'},
        {'name': 'Protein Powder', 'price': 49, 'description': 'Whey protein powder.'},
        {'name': 'Yoga Block', 'price': 14, 'description': 'Foam yoga block for support.'},
        {'name': 'Massage Gun', 'price': 79, 'description': 'Deep tissue massage gun.'},
        {'name': 'Blood Pressure Monitor', 'price': 39, 'description': 'Digital blood pressure monitor.'},
        {'name': 'Resistance Bands', 'price': 19, 'description': 'Set of resistance bands.'},
        {'name': 'Foam Roller', 'price': 24, 'description': 'High-density foam roller.'},
        {'name': 'Essential Oils', 'price': 16, 'description': 'Lavender essential oil.'},
        {'name': 'Herbal Tea', 'price': 11, 'description': 'Organic herbal tea bags.'},
        {'name': 'Fitness Tracker', 'price': 99, 'description': 'Advanced fitness tracking band.'},
        {'name': 'Sleep Mask', 'price': 9, 'description': 'Comfortable sleep mask.'},
        {'name': 'First Aid Kit', 'price': 34, 'description': 'Comprehensive first aid kit.'},
    ],
    'Baby & Kids': [
        {'name': 'Baby Diapers', 'price': 24, 'description': 'Pack of 50 baby diapers.'},
        {'name': 'Baby Formula', 'price': 39, 'description': 'Infant milk formula.'},
        {'name': 'Baby Monitor', 'price': 79, 'description': 'Video baby monitor.'},
        {'name': 'Stroller', 'price': 199, 'description': 'Foldable baby stroller.'},
        {'name': 'Baby Clothes', 'price': 19, 'description': 'Set of 5 baby onesies.'},
        {'name': 'Baby Toys', 'price': 14, 'description': 'Soft baby rattle toys.'},
        {'name': 'Baby Bath Tub', 'price': 49, 'description': 'Foldable baby bath tub.'},
        {'name': 'Baby Carrier', 'price': 39, 'description': 'Ergonomic baby carrier.'},
        {'name': 'Baby Bottle', 'price': 9, 'description': 'Anti-colic baby bottle.'},
        {'name': 'Baby Blanket', 'price': 16, 'description': 'Soft fleece baby blanket.'},
        {'name': 'High Chair', 'price': 89, 'description': 'Adjustable baby high chair.'},
        {'name': 'Teething Toys', 'price': 12, 'description': 'Set of 3 teething toys.'},
    ],
    'Home & Decor': [
        {'name': 'Scented Candles', 'price': 19, 'description': 'Set of 3 scented candles.', 'image': 'scented_candles.jpg'},
        {'name': 'Wall Art', 'price': 49, 'description': 'Abstract wall art decor.', 'image': 'wall_art.jpg'},
        {'name': 'Throw Pillows', 'price': 29, 'description': 'Decorative throw pillows.', 'image': 'throw_pillows.jpg'},
        {'name': 'Area Rug', 'price': 99, 'description': 'Soft area rug for living room.', 'image': 'area_rug.jpg'},
        {'name': 'Table Lamp', 'price': 39, 'description': 'Modern table lamp.', 'image': 'table_lamp.jpg'},
        {'name': 'Curtains', 'price': 59, 'description': 'Blackout curtains for bedroom.', 'image': 'curtains.jpg'},
        {'name': 'Picture Frames', 'price': 24, 'description': 'Set of 4 picture frames.', 'image': 'picture_frames.jpg'},
        {'name': 'Vase', 'price': 19, 'description': 'Ceramic decorative vase.', 'image': 'vase.jpg'},
        {'name': 'Clocks', 'price': 34, 'description': 'Wall clock with modern design.', 'image': 'clocks.jpg'},
        {'name': 'Storage Baskets', 'price': 29, 'description': 'Set of 3 woven storage baskets.', 'image': 'storage_baskets.jpg'},
        {'name': 'Mirrors', 'price': 79, 'description': 'Decorative wall mirror.', 'image': 'mirrors.jpg'},
        {'name': 'Planters', 'price': 22, 'description': 'Set of 2 indoor plant planters.', 'image': 'planters.jpg'},
    ],
    'Smartphones': [
        {'name': 'iPhone 13', 'price': 799, 'description': 'Latest Apple iPhone with A15 Bionic chip.', 'image': 'iphone_13.jpg'},
        {'name': 'Samsung Galaxy S21', 'price': 699, 'description': 'Flagship Samsung smartphone with AMOLED display.', 'image': 'samsung_galaxy_s21.jpg'},
        {'name': 'Google Pixel 6', 'price': 599, 'description': 'Google\'s newest smartphone with excellent camera.', 'image': 'google_pixel_6.jpg'},
        {'name': 'OnePlus 9', 'price': 729, 'description': 'High-performance smartphone with fast charging.', 'image': 'oneplus_9.jpg'},
        {'name': 'Sony Xperia 5 II', 'price': 949, 'description': 'Compact smartphone with professional-grade camera.', 'image': 'sony_xperia_5_ii.jpg'},
        {'name': 'Motorola Edge', 'price': 699, 'description': 'Motorola\'s sleek smartphone with edge display.', 'image': 'motorola_edge.jpg'},
        {'name': 'Nokia 8.3', 'price': 499, 'description': 'Affordable smartphone with great features.', 'image': 'nokia_8.3.jpg'},
        {'name': 'Xiaomi Mi 11', 'price': 749, 'description': 'Powerful smartphone with high refresh rate display.', 'image': 'xiaomi_mi_11.jpg'},
        {'name': 'Oppo Find X3', 'price': 899, 'description': 'Premium smartphone with advanced camera system.', 'image': 'oppo_find_x3.jpg'},
        {'name': 'Asus ROG Phone 5', 'price': 999, 'description': 'Gaming smartphone with top-tier specs.', 'image': 'asus_rog_phone_5.jpg'},
        {'name': 'LG Velvet', 'price': 599, 'description': 'Stylish smartphone with dual-screen capability.', 'image': 'lg_velvet.jpg'},
        {'name': 'Huawei P40 Pro', 'price': 899, 'description': 'High-end smartphone with excellent camera performance.', 'image': 'huawei_p40_pro.jpg'}
    ],
}

# Create products for each category
for category in categories:
    cat_name = category.category_name
    if cat_name in product_data:
        products_list = product_data[cat_name]
        for prod in products_list:
            # Check if product already exists
            existing_product = Products.objects.filter(product_name=prod['name'], category=category).first()
            if existing_product:
                # Product exists, check if we need to update the image
                if 'image' in prod and (not existing_product.image or existing_product.image.name != prod['image']):
                    with open(f'media/{prod["image"]}', 'rb') as f:
                        existing_product.image = File(f, name=prod['image'])
                        existing_product.save()
                    print(f"Updated image for product: {existing_product.product_name} in category {cat_name}")
                else:
                    print(f"Product {prod['name']} already exists in {cat_name} with image")
            else:
                # Product does not exist, create it
                # if 'image' in prod:
                #     with open(f'media/{prod["image"]}', 'rb') as f:
                #         product = Products.objects.create(
                #             product_name=prod['name'],
                #             category=category,
                #             price=prod['price'],
                #             description=prod['description'],
                #             image=File(f, name=prod['image'])
                #         )
                # else:
                    product = Products.objects.create(
                        product_name=prod['name'],
                        category=category,
                        price=prod['price'],
                        description=prod['description'],
                        # For image, we'll use a placeholder or skip for now
                        # image='media/placeholder.jpg'  # You can add placeholder images later
                    )
                # print(f"Created product: {product.product_name} in category {cat_name}")

print("Product creation completed!")
