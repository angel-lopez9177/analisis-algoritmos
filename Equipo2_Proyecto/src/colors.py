class Colores:
    """Paleta inspirada en tonos púrpura y azul profundo"""

    # Colores base
    NEGRO_PROFUNDO = "#050205"
    MORADO_NOCHE = "#140919"
    INDIGO_OSCURO = "#23162E"
    AZUL_VIOLACEO = "#2E2B4D"
    CIRUELA_METALICO = "#4E325C"

    # Acentos brillantes
    TEXTO_CLARO = "#E3D7FF"
    DETALLE_MAGENTA = "#C67AFF"
    DETALLE_AZUL = "#8A7BFF"

    @classmethod
    def tk(cls):
        """Retorna un diccionario listo para usar en la GUI (versión original)"""
        return {
            "bg": cls.NEGRO_PROFUNDO,
            "panel_left": cls.MORADO_NOCHE,
            "panel_right": cls.INDIGO_OSCURO,
            "text": cls.TEXTO_CLARO,
            "accent": cls.DETALLE_MAGENTA,
            "accent2": cls.DETALLE_AZUL,
            "cell_match": cls.CIRUELA_METALICO,
            "cell_default": cls.AZUL_VIOLACEO,
            "highlight": cls.DETALLE_MAGENTA,
        }

    @classmethod
    def tk_light(cls):
        """Retorna un diccionario con la nueva paleta de colores para mejor visualización."""
        return {
            "bg": cls.MORADO_NOCHE,       # Fondo principal de la ventana
            "panel": cls.INDIGO_OSCURO,    # Fondo para campos de entrada y celdas
            "text": cls.TEXTO_CLARO,       # Color principal del texto
            "highlight": cls.DETALLE_MAGENTA, # Resaltado principal (barras, botones activos)
            "accent2": cls.DETALLE_AZUL,   # Acento secundario (botones)
            "cell_match": cls.CIRUELA_METALICO, # Celda donde hay coincidencia
        }