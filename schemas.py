from pydantic import BaseModel

class VendedorBase(BaseModel):
    email: str

class VendedorCreate(VendedorBase):
    password: str

class Vendedor(VendedorBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    imagen_url: str
    vendedor_email: str | None = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: str | None = None
    precio: float | None = None

class Producto(ProductoBase):
    id: int
    descripcion_marketing: str
    imagen_url: str

    class Config:
        from_attributes = True