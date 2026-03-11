"""
pnl_service.py — Procesamiento de Lenguaje Natural
Librerías usadas:
  - spacy: resumen y entidades
  - transformers: análisis de sentimientos
  - deep_translator: traducción
"""
import json
from typing import Dict, Any


def analizar_texto(texto: str) -> Dict[str, Any]:
    """
    Analiza un texto con PNL y retorna:
    - resumen
    - entidades (síntomas, enfermedades, medicamentos)
    - traduccion (español → inglés)
    - sentimiento (positivo/negativo/neutro)
    - score_sentimiento (0.0 a 1.0)
    """
    resultado = {
        "resumen": None,
        "entidades": None,
        "traduccion": None,
        "sentimiento": None,
        "score_sentimiento": None,
    }

    # 1. RESUMEN con spacy
    try:
        import spacy
        nlp = spacy.load("es_core_news_sm")
        doc = nlp(texto)
        oraciones = [sent.text.strip() for sent in doc.sents]
        resultado["resumen"] = " ".join(oraciones[:3]) if len(oraciones) > 3 else texto
    except Exception as e:
        resultado["resumen"] = texto[:300] + "..." if len(texto) > 300 else texto

    # 2. ENTIDADES con spacy
    try:
        import spacy
        nlp = spacy.load("es_core_news_sm")
        doc = nlp(texto)
        entidades = [
            {"texto": ent.text, "tipo": ent.label_}
            for ent in doc.ents
        ]
        resultado["entidades"] = json.dumps(entidades, ensure_ascii=False)
    except Exception:
        resultado["entidades"] = json.dumps([])

    # 3. TRADUCCIÓN con deep_translator
    try:
        from deep_translator import GoogleTranslator
        traduccion = GoogleTranslator(source="es", target="en").translate(texto)
        resultado["traduccion"] = traduccion
    except Exception:
        resultado["traduccion"] = "Traducción no disponible"

    # 4. SENTIMIENTOS con transformers
    try:
        from transformers import pipeline
        classifier = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        pred = classifier(texto[:512])[0]
        label = pred["label"]   # "1 star" a "5 stars"
        score = pred["score"]

        # Convertir a positivo/negativo/neutro
        stars = int(label.split()[0])
        if stars <= 2:
            sentimiento = "negativo"
        elif stars == 3:
            sentimiento = "neutro"
        else:
            sentimiento = "positivo"

        resultado["sentimiento"] = sentimiento
        resultado["score_sentimiento"] = round(score, 4)
    except Exception:
        resultado["sentimiento"] = "neutro"
        resultado["score_sentimiento"] = 0.5

    return resultado
