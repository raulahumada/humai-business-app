# humai-business-app

E-commerce demo (carrito, cupones, checkout) instrumentado con Langfuse.
Sirve como producto observado por el agente de `langfuse-ops`.

```bash
uv sync
cp .env.example .env   # completar keys de Langfuse
uv run python traffic.py 40
uv run pytest
```
