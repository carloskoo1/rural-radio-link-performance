# Reproducibilidad del material del artículo

## Alcance

Esta documentación corresponde a la extensión de publicación article/beyond-rssi y al manuscrito Beyond RSSI: Configuration-Dependent Performance and Temporal Stability in a Long-Distance Point-to-Point Wireless Link.

El análisis del artículo excluye ERA5-Land y NASA POWER. El repositorio conserva esos recursos porque pertenecen al proyecto experimental original, pero no forman parte de la evidencia presentada en esta extensión.

## Evidencia congelada

La tabla outputs/article_tables/Table_MTRA_validated.csv contiene la evidencia estadística congelada utilizada para el análisis MTRA. Las escalas son 15, 30 y 60 minutos. Para cada escala se documentan N, H de Kruskal-Wallis, grados de libertad, p, epsilon-squared y el número de comparaciones Dunn-Holm significativas.

Las figuras Fig02_configuration_profiles.svg, Fig03_performance_stability.svg, Fig04_MTRA_effect_sizes.svg y Fig05_stability_scales.svg son productos versionados de esa evidencia.

## Generación

La generación de las figuras y de la tabla MTRA se ejecuta con:

node scripts/article/generate_article_figures.js

La ejecución es determinista: los productos se reconstruyen a partir de los valores de evidencia congelados definidos en el generador de publicación. Esto permite reproducir exactamente las figuras versionadas, pero no sustituye una recomputación estadística desde los datos brutos.

## Trazabilidad

Cadena de trazabilidad para la extensión del artículo:

datos experimentales versionados
        |
        v
pipeline estadístico de tesis
        |
        v
evidencia MTRA validada
outputs/article_tables/Table_MTRA_validated.csv
        |
        v
scripts/article/generate_article_figures.js
        |
        +--> Fig. 2
        +--> Fig. 3
        +--> Fig. 4
        +--> Fig. 5

La liberación de tesis reproducible permanece identificada por v1.0.0. La extensión del artículo se mantiene en article/beyond-rssi.

## Limitaciones conocidas

1. El generador de figuras utiliza valores estadísticos congelados y no recalcula Kruskal-Wallis, Dunn-Holm ni epsilon-squared desde los CSV de entrada.
2. Por tanto, la reproducibilidad de esta extensión es de nivel output-reproducible: permite reconstruir exactamente las figuras y tablas publicadas, mientras que la reproducibilidad analítica completa depende de ejecutar y auditar previamente el pipeline estadístico de tesis.
3. E0 se excluye de las comparaciones de throughput observado porque esa métrica no está disponible para dicho escenario.
4. Los archivos auxiliares locales y respaldos no versionados no forman parte del artefacto científico.

## Verificación mínima antes de una nueva versión

node scripts/article/generate_article_figures.js
git status
git diff --exit-code -- outputs/article_figures outputs/article_tables

Si no aparece diferencia en los productos versionados, la generación conserva la evidencia publicada.
