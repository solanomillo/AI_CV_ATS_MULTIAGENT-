# 🤖 AI CV ATS Multi-Agent Analyzer

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=flat&logo=googlegemini&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blue?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

**AI CV ATS Multi-Agent** es una solución avanzada de análisis de currículums que utiliza una arquitectura de **multi-agentes inteligentes** para evaluar, calificar y optimizar perfiles profesionales bajo estándares ATS (Applicant Tracking System).

---

## 📌 Descripción
A diferencia de los analizadores tradicionales, este sistema orquesta múltiples agentes especializados (basados en Google Gemini 1.5 Flash) que trabajan en conjunto para:

* Analizar la estructura del CV

* Detectar errores críticos

* Evaluar compatibilidad ATS

* Calcular métricas cuantitativas y cualitativas

* Generar recomendaciones estratégicas

* Crear una versión optimizada lista para postulación

Desarrollado con una arquitectura limpia, desacoplada y modular, el proyecto está preparado para:

* Uso personal

* Distribución como software de escritorio (.exe)

* Evolución futura a modelo SaaS

## 🚀 Stack Tecnológico

El proyecto se apoya en herramientas modernas orientadas a arquitectura escalable:

🔹 Core IA

* langchain

* langgraph (Orquestación basada en grafos)

* google-generativeai (Google Gemini 1.5 Flash)

🔹 Interfaz Gráfica

* customtkinter (Modern Desktop UI en Python)

🔹 Procesamiento de Documentos

* pypdf / PyPDF2

* python-docx

🔹 Generación de Reportes

* reportlab (PDF dinámicos profesionales)

🔹 Validación y Configuración

* pydantic (Modelado estructurado)

* python-dotenv (Gestión segura de variables)

🔹 Persistencia

* sqlite3 (Base de datos local)

🔹 Distribución

* pyinstaller (Empaquetado profesional a .exe)

---

## 🧠 Arquitectura de Multi-Agentes
El núcleo del sistema se basa en la colaboración de agentes especializados, coordinados mediante un grafo de ejecución:

### 🧾 Reader Agent

Encargado de la lectura y normalización del contenido del CV (PDF / DOCX).

### 🧩 Extractor Agent

Estructura la información en entidades procesables (experiencia, habilidades, educación, etc.).

### 📊 Scoring Agent

Aplica lógica de evaluación cuantitativa y genera métricas de calidad.

### 🧠 ATS Agent

Evalúa compatibilidad con sistemas de filtrado automático (palabras clave, estructura, formato).

### ✍️ Optimizer Agent

Genera mejoras estratégicas y redacta una versión optimizada del CV.

### 💾 Persistence Agent  
Gestiona el almacenamiento del análisis en SQLite y mantiene historial.

---

## ⚙️ Funcionalidades

✅ Análisis automático con IA  
✅ Evaluación bajo criterios ATS  
✅ Score LLM  
✅ Score por reglas estructurales  
✅ Score final combinado  
✅ Generación de versión optimizada  
✅ Descarga manual de reporte PDF  
✅ Historial de análisis  
✅ Base de datos local  
✅ Arquitectura preparada para SaaS  

## 📂 Estructura del Proyecto

```text
AI_CV_ATS_MULTIAGENT/
├── agents/                 # Cerebro del sistema (Multi-Agentes)
│   ├── ats_agent.py        # Especialista en criterios de filtrado
│   ├── extractor_agent.py  # Extracción de entidades y datos
│   ├── optimizer_agent.py  # Generación de mejoras y sugerencias
│   ├── persistence_agent.py# Orquestador de guardado
│   ├── reader_agent.py     # Procesamiento inicial de texto
│   └── scoring_agent.py    # Cálculo de métricas y scores
├── application/            # Lógica de orquestación
│   └── graph_builder.py    # Construcción del flujo de trabajo (Grafo)
├── domain/                 # Reglas de negocio y modelos
│   ├── models.py           # Estructuras de datos (Pydantic)
│   └── state.py            # Definición del estado del flujo
├── infrastructure/         # Servicios externos y clientes
│   ├── cv_reader.py        # Driver de lectura de archivos (PDF/Docx)
│   └── gemini_client.py    # Conexión con Google Gemini API
├── persistence/            # Capa de datos
│   └── memory_store.py     # Manejo de SQLite y persistencia local
├── ui/                     # Interfaz de Usuario
│   └── main_window.py      # GUI principal (CustomTkinter)
├── utils/                  # Herramientas de soporte
│   └── pdf_generator.py    # Generador de reportes en PDF
├── app.py                 # Punto de entrada
├── requirements.txt        # Dependencias
└── .env                    # Configuración (NO versionado)
```

---

## 🛠️ Instalación y Configuración

1️⃣ Clonar el repositorio
```bash
git clone https://github.com/solanomillo/AI_CV_ATS_MULTIAGENT-.git
cd AI_CV_ATS_MultiAgent
```

2️⃣ Crear entorno virtual
```bash
python -m venv env
env\Scripts\activate
```

3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

4️⃣ Configurar variables de entorno
Crear un archivo .env en la raíz:
```bash
GEMINI_API_KEY=tu_api_key_aqui
```
El archivo .env no debe subirse al repositorio

▶️ Ejecutar en modo desarrollo
```bash
python app.py
```
---

## 🖥️ Generar Ejecutable Profesional
Generar una nueva carpeta assets, dentro de ella el icono de la app
```bash
pyinstaller main.py --name "AI_CV_ATS_MultiAgent" --onefile --windowed --icon=assets/icono.ico
```
El ejecutable se generará en:
```text
dist/AI_CV_ATS_MultiAgent.exe
```

Para su correcto funcionamiento, el archivo .env debe estar en la misma carpeta que el .exe.

---

## 🔐 Seguridad

✔️ Sin credenciales hardcodeadas  
✔️ API Key mediante variables de entorno  
✔️ Persistencia local controlada  
✔️ Arquitectura desacoplada  
✔️ Preparado para backend centralizado  

---

## 🏗️ Roadmap Futuro

* 🔐 Sistema de autenticación

* 🌐 Migración a versión web (Django / SaaS)

* 💳 Modelo de suscripción mensual

* ☁️ Backend centralizado con control de API

* 📊 Dashboard analítico de métricas

* 👥 Multiusuario empresarial

---

**Julio Solano**  
🔗 GitHub: [https://github.com/solanomillo](https://github.com/solanomillo)  
📧 Email: [solanomillo144@gmail.com](mailto:solanomillo144@gmail.com)

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.
Podés usarlo, modificarlo y compartirlo libremente.

