from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from api.commerce.product.models import Product


@registry.register_document
class ProductDocument(Document):
    product = fields.ObjectField(properties={"name": fields.TextField()})
    brand = fields.ObjectField(properties={"name": fields.TextField()})

    class Index:
        name = "product"

    class Django:
        model = Product
        fields = ['name']
