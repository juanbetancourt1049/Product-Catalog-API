import os
from dotenv import load_dotenv
from database import Base, engine, SessionLocal

def init_db():
    load_dotenv()
    print("Eliminando todas las tablas existentes...")
    Base.metadata.drop_all(bind=engine)
    print("Creando todas las tablas...")
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada correctamente.")

if __name__ == "__main__":
    init_db()