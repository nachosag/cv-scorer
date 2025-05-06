# Aplicacion web para buscar coincidencias dentro de currículums

Pasos para ejecutar el código:
1. Instalar las dependencias con ``pip install -r requirements.txt``
2. Instalar los modelos de Spacy ejecutando:
 - python -m spacy download es_core_news_lg
 - python -m spacy download en_core_web_lg
3. Ejecutar main.py para levantar el servidor en local.
4. Dirigirse a localhost:5000
5. Ingresar las etiquetas a buscar.
6. Ingresar los CVs a analizar.
7. Presionar "Match Resumes" y visualizar resultados.