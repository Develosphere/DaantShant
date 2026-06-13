"""Embedding service for product semantic search.

Uses OpenAI's text-embedding-3-small via the OpenAI SDK.
Falls back to a simple TF-IDF-style keyword vector if OpenAI key is unavailable.
"""

import logging
import os
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

_openai_client = None


def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        try:
            from openai import AsyncOpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                _openai_client = AsyncOpenAI(api_key=api_key)
                logger.info("[EMBEDDING] OpenAI client initialized")
            else:
                logger.warning("[EMBEDDING] OPENAI_API_KEY not set — using keyword fallback")
        except ImportError:
            logger.warning("[EMBEDDING] openai package not installed — using keyword fallback")
    return _openai_client


async def embed_text(text: str) -> list[float]:
    """Embed text using OpenAI text-embedding-3-small. Falls back to keyword vector."""
    client = _get_openai_client()
    if client:
        try:
            response = await client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
            )
            return response.data[0].embedding
        except Exception as exc:
            logger.warning("[EMBEDDING] OpenAI embed failed: %s — using fallback", exc)

    # Keyword fallback: fixed-vocabulary 128-dim binary vector
    return _keyword_vector(text)


def _keyword_vector(text: str) -> list[float]:
    """Deterministic 128-dim keyword vector from dental vocabulary."""
    VOCAB = [
        "plaque", "tartar", "cavity", "decay", "gingivitis", "gum", "bleed", "sensitive",
        "sensitivity", "whitening", "yellow", "stain", "discolor", "brush", "floss",
        "mouthwash", "fluoride", "enamel", "toothpaste", "toothbrush", "antibacterial",
        "charcoal", "whitening", "pain", "ache", "sore", "swollen", "inflamed", "fresh",
        "breath", "halitosis", "dry", "mouth", "orthodon", "brace", "aligner", "crown",
        "filling", "extraction", "root", "canal", "wisdom", "broken", "chip", "crack",
        "loose", "electric", "manual", "soft", "medium", "hard", "bristle", "head",
        "tongue", "scraper", "xylitol", "peroxide", "baking", "soda", "mint", "spearmint",
        "peppermint", "natural", "herbal", "organic", "kids", "children", "adult", "pro",
        "professional", "clinical", "dentist", "recommended", "clean", "deep", "clean",
        "interdental", "pick", "water", "flosser", "irrigator", "gel", "foam", "strip",
        "tray", "night", "guard", "grind", "jaw", "tmj", "remineraliz", "strengthen",
        "protect", "prevent", "treat", "repair", "restore", "rebuild", "sealant",
        "varnish", "rinse", "antiseptic", "chlorhexidine", "cetylpyridinium", "zinc",
        "calcium", "phosphate", "potassium", "nitrate", "arginine", "novamin",
        "hydroxyapatite", "nano", "micro", "ultra", "max", "complete", "total",
        "advanced", "sensitive", "original", "classic", "fresh", "cool", "ice",
        "extra", "plus", "pro", "elite", "premium", "budget", "value", "pack",
        "travel", "portable", "rechargeable", "battery", "sonic", "ultrasonic",
        "timer", "pressure", "sensor", "smart", "connected", "app", "bluetooth",
        "tongue", "cheek", "lip", "saliva", "xerostomia", "ulcer", "sore", "canker",
        "abscess", "infection", "bacteria", "fungal", "viral", "immune",
    ]
    text_lower = text.lower()
    vec = [1.0 if word in text_lower else 0.0 for word in VOCAB]
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors."""
    va, vb = np.array(a, dtype=float), np.array(b, dtype=float)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)
