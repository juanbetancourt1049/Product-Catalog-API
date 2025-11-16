from sqlalchemy.orm import Session
from models import Vendedor, Producto
from schemas import VendedorCreate, ProductoCreate, ProductoUpdate
from security import get_password_hash

def get_vendedor_by_email(db: Session, email: str):
    return db.query(Vendedor).filter(Vendedor.email == email).first()

def create_vendedor(db: Session, vendedor: VendedorCreate):
    hashed_password = get_password_hash(vendedor.password)
    db_vendedor = Vendedor(email=vendedor.email, hashed_password=hashed_password)
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Producto).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate, descripcion_marketing: str, imagen_url: str, vendedor_email: str):
    print(f"[crud.py] Recibido para crear: Nombre={producto.nombre}, Precio={producto.precio}, Vendedor Email={vendedor_email}")
    db_producto = Producto(nombre=producto.nombre, precio=producto.precio, descripcion_marketing=descripcion_marketing, imagen_url=imagen_url, vendedor_email=vendedor_email)
    print(f"[crud.py] Producto antes de añadir a DB: {db_producto.nombre}, {db_producto.vendedor_email}")
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto_update: ProductoUpdate):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto:
        update_data = producto_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_producto, key, value)
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int, vendedor_email: str):
    print(f"[crud.py] Recibido para eliminar: ID={producto_id}, Vendedor Email={vendedor_email}")
    db_producto = db.query(Producto).filter(Producto.id == producto_id, Producto.vendedor_email == vendedor_email).first()
    print(f"[crud.py] Resultado de la consulta de eliminación: {db_producto}")
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto