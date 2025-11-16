import os
from dotenv import load_dotenv

load_dotenv()

# Placeholder for Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generar_descripcion(nombre_producto: str) -> str:
    """Genera una descripción de marketing atractiva de un solo párrafo para el producto usando la API de Gemini."""
    # Aquí iría la lógica real para llamar a la API de Gemini
    # Por ahora, es una implementación de marcador de posición.
    if not GEMINI_API_KEY:
        print("Advertencia: GEMINI_API_KEY no está configurada. Usando descripción de marcador de posición.")
    return f"¡Descubre el increíble {nombre_producto}! Este producto revolucionario combina diseño elegante con funcionalidad de vanguardia para ofrecerte una experiencia inigualable. Perfecto para el día a día o para ocasiones especiales, el {nombre_producto} es la elección ideal para quienes buscan calidad y estilo."

def generar_imagen(descripcion_marketing: str, nombre_producto: str) -> str:
    """Genera una URL de imagen para el producto usando Pollinations.ai."""
    prompt = descripcion_marketing
    width = 1024
    height = 1024
    seed = 42 # Cada seed genera una nueva variación de imagen
    model = 'flux' # Usando 'flux' como default si el modelo no es proporcionado

    image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
    return image_url