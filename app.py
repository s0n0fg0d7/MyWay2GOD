import streamlit as st
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List
import json

# --- TUS CLASES (La lógica original) ---
@dataclass
class SpiritualState:
    apertura: float = 0.5
    humildad: float = 0.5
    compasion: float = 0.5
    gratitud: float = 0.5
    curiosidad: float = 0.5
    busqueda_de_Dios: float = 0.5
    paz_interior: float = 0.5

    def evolve(self, quality: str, change: float):
        if hasattr(self, quality):
            current = getattr(self, quality)
            setattr(self, quality, max(0.0, min(1.0, current + change)))

    def reflection(self):
        return asdict(self)

@dataclass
class SpiritualJourney:
    tradition: str = "Búsqueda universal de Dios"
    central_message: str = "La verdad, el amor y la conciencia pueden abrir el corazón a una relación más profunda con Dios."
    practices: List[str] = field(default_factory=lambda: [
        "Oración o contemplación", "Silencio interior", "Servicio al prójimo", 
        "Gratitud diaria", "Búsqueda sincera de la verdad"
    ])

class DivineSearchAI:
    def __init__(self):
        self.state = SpiritualState()
        self.journey = SpiritualJourney()
        self.history = []

    def record(self, user_message, AI_message):
        self.history.append({"fecha": datetime.now().isoformat(), "usuario": user_message, "guia": AI_message})

    def evaluate(self, answer: str):
        answer = answer.lower()
        if any(word in answer for word in ["gracias", "agradezco", "bendición"]): self.state.evolve("gratitud", 0.1)
        if any(word in answer for word in ["ayudar", "amor", "servir"]): self.state.evolve("compasion", 0.1)
        if any(word in answer for word in ["buscar", "dios", "verdad", "sentido"]): self.state.evolve("busqueda_de_Dios", 0.1)

    def welcome(self):
        return "✨ BIENVENIDO A TU CAMINO DE BÚSQUEDA ESPIRITUAL ✨\n\nNo estoy aquí para reemplazar tu conciencia, sino para acompañarte en tu búsqueda sincera.\n\n¿Qué te mueve hoy a buscar a Dios?"

    def respond(self, user_answer: str):
        self.evaluate(user_answer)
        questions = ["¿Qué experiencia de tu vida te ha hecho preguntarte por Dios?", "¿Qué significa para ti el amor verdadero?", "¿Qué parte de tu corazón necesita más luz?", "Si Dios pudiera hablarte ahora, ¿qué pregunta le harías?"]
        index = len(self.history) % len(questions)
        message = f"Tu reflexión ha sido recibida.\n\n{self.journey.central_message}\n\nPregunta: {questions[index]}\n\nPráctica sugerida: {self.journey.practices[index % len(self.journey.practices)]}\n\nEstado:\n{json.dumps(self.state.reflection(), indent=2, ensure_ascii=False)}"
        self.record(user_answer, message)
        return message

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Camino Espiritual", page_icon="✨")
st.title("✨ Acompañante Espiritual")

if 'ai' not in st.session_state:
    st.session_state.ai = DivineSearchAI()

# Mostrar historial
for entry in st.session_state.ai.history:
    st.markdown(f"**Tú:** {entry['usuario']}")
    st.markdown(f"**Guía:** {entry['guia']}")

# Entrada de texto
user_input = st.text_input("Tu respuesta:")

if st.button("Enviar"):
    if user_input:
        response = st.session_state.ai.respond(user_input)
        st.rerun() # Actualiza la pantalla para mostrar la nueva respuesta
    else:
        st.warning("Por favor, escribe algo para continuar.")
