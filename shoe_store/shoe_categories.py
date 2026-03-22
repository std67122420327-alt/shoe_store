categories= [
    'Nike',
    'Adidas',
    'Converse',
    'Vans',
    'Puma',
    'New Balance',
    'Jordan',
    'Reebok',
    'ASICS',
    'Crocs'
]

from shoe_store.models import Category 
shoe_categories = [Category(name=cat) for cat in categories ]
