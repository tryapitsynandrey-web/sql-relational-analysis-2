from typing import Callable
from functools import wraps
import streamlit as st

def with_cache(ttl_seconds: int = 300):
    """with_cache — Decorator utilizing Streamlit's native data cache to avoid Pandas SerializationErrors."""
    def decorator(func: Callable):
        # We define a helper that is wrapped by st.cache_data
        # _self tells Streamlit to NOT hash the MetricEngine class instance
        @st.cache_data(ttl=ttl_seconds, show_spinner=False)
        def _cached_func(_self, *args, **kwargs):
            return func(_self, *args, **kwargs)
            
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return _cached_func(self, *args, **kwargs)
        return wrapper
    return decorator
