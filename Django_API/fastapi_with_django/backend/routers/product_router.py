from product.models import Product
from fastapi import APIRouter, Form, File, UploadFile
from django.core.files.base import ContentFile

router = APIRouter()

@router.post("/add_product")
def add_product(
    name : str = Form(...),
    description : str = Form(...),
    image : UploadFile = File(...)
):
    product = Product.objects.create(
        name = name,
        description = description,
    )
    product.image.save(
        image.filename,
        ContentFile(image.file.read()),
        save=True
    )
    return {"msg":"Product Added Successfully"}

@router.get("/get_product")
def get_product():
    products = Product.objects.all()

    data = []
    for product in products:
        data.append({
            "id" : product.id,
            "name" : product.name,
            "description" : product.description,
            "image" : f"http://127.0.0.1:8000/media/products/{product.image}"
        })
    return data

@router.put("/update_product/{id}")
def update_product(
    id : int,
    name : str = Form(None),
    description : str = Form(None),
    image : UploadFile = File(None)
):
    product = Product.objects.get(id=id)
    if name:
        product.name = name

    if description:
        product.description = description

    if image:
        product.image.save(
            image.filename,
            image.file,
            save = False
        )
    product.save()
    return {
        "product id" : product.id,
        "msg":"Product updated successfully"
    }

@router.delete("/delete_product/{id}")
def delete_product(id : int):
    product = Product.objects.get(id = id)
    product.delete()
    return {
        "msg" : "Product deleted successfully"
    }
