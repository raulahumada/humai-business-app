"""Reporta excepciones a Langfuse con contexto útil para diagnosticar."""

import traceback

from langfuse import get_client


def report_error(exc: Exception) -> None:
    tb = traceback.extract_tb(exc.__traceback__)
    last = tb[-1] if tb else None
    get_client().update_current_span(
        level="ERROR",
        status_message=f"{type(exc).__name__}: {exc}",
        metadata={
            "error.type": type(exc).__name__,
            "error.location": f"{last.filename.split('/')[-1]}:{last.lineno} en {last.name}" if last else None,
            "error.stacktrace": "".join(traceback.format_exception(exc))[-1500:],
        },
    )
