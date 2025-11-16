import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from crud import get_vendedor_by_email, create_vendedor, get_productos, create_producto as crud_create_producto, update_producto as crud_update_producto, delete_producto as crud_delete_producto
from models import Vendedor, Producto
from schemas import VendedorCreate, Vendedor as VendedorSchema, Token, TokenData, Producto as ProductoSchema, ProductoCreate, ProductoUpdate
from security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_access_token, verify_password
from gemini_client import generar_descripcion, generar_imagen
from database import SessionLocal, engine, Base


load_dotenv()

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    os.getenv("FRONTEND_URL"),
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

product_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_vendedor(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except Exception as e:
        print(f"Error al decodificar el token: {e}")
        raise credentials_exception
    vendedor = get_vendedor_by_email(db, email=token_data.email)
    if vendedor is None:
        raise credentials_exception
    return vendedor

@app.post("/register", response_model=VendedorSchema)
def register_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    db_vendedor = get_vendedor_by_email(db, email=vendedor.email)
    if db_vendedor:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_vendedor(db=db, vendedor=vendedor)

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    vendedor = get_vendedor_by_email(db, email=form_data.username)
    if not vendedor or not verify_password(form_data.password, vendedor.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": vendedor.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@product_router.get("/productos/", response_model=list[ProductoSchema])
def read_productos(current_vendedor: VendedorSchema = Depends(get_current_vendedor), db: Session = Depends(get_db)):
    productos = get_productos(db)
    return productos

@product_router.post("/productos/", response_model=ProductoSchema)
def create_producto(producto: ProductoCreate, current_vendedor: VendedorSchema = Depends(get_current_vendedor), db: Session = Depends(get_db)):
    # Generar descripción de marketing con Gemini
    descripcion_marketing = generar_descripcion(producto.nombre)
    # Generar URL de imagen con Gemini (o la API de tu elección)
    imagen_url = generar_imagen(descripcion_marketing, producto.nombre)

    # Crear el producto en la base de datos
    db_producto = crud_create_producto(db=db, producto=producto, descripcion_marketing=descripcion_marketing, imagen_url=imagen_url, vendedor_email=current_vendedor.email)
    return db_producto

@product_router.delete("/productos/{producto_id}")
def delete_producto(producto_id: int, current_vendedor: VendedorSchema = Depends(get_current_vendedor), db: Session = Depends(get_db)):
    db_producto = crud_delete_producto(db=db, producto_id=producto_id, vendedor_email=current_vendedor.email)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado exitosamente"}

@product_router.put("/productos/{producto_id}", response_model=ProductoSchema)
def update_producto(producto_id: int, producto: ProductoUpdate, current_vendedor: VendedorSchema = Depends(get_current_vendedor), db: Session = Depends(get_db)):
    db_producto = crud_update_producto(db=db, producto_id=producto_id, producto_update=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

app.include_router(product_router)

# Serve static files