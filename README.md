# ai-redteam-lab
> **AI Red Teaming learning lab** — un cuaderno de laboratorio, con código y writeups, sobre cómo se atacan (y se defienden) los modelos de lenguaje. Aprendizaje incremental, experimentos propios y reflexión honesta sobre los resultados.

Empecé este verano prácticamente desde cero (poca programación, cero ciberseguridad). Este repo es el registro público de ese aprendizaje en **AI Red Teaming**, sesión a sesión. No pretende impresionar por la ingeniería del código —todavía es sencillo—, sino mostrar **cómo pienso como atacante** y cómo documento lo que aprendo.

Todo se ejecuta en local contra modelos servidos por [LM Studio](https://lmstudio.ai/) (API compatible con OpenAI). Todos los ataques son contra mis propios laboratorios de juguete. **Cero ataques a sistemas reales o ajenos.**

---

## El hilo conductor
Cada sesión construye sobre la anterior. La progresión es el mensaje:

```
Prompt manual (Gandalf)
   → Ataque por API (script)
      → Fuzzer automatizado
         → Prompt Injection directa + defensa
            → Prompt Injection indirecta (documento / web real)
               → Comparativa entre modelos
                  → LLM-as-Judge (2º modelo de guardia)
                     → Prompt Injection de 2º orden (romper el guardia)
                        → Primer agente autónomo
                           → Reward Hacking
                              → Cliente reutilizable + primeras métricas
```

## Mapeo OWASP LLM
- **LLM01 — Prompt Injection:** sesiones 1–8 (directa, indirecta, vía web, de 2º orden).
- **LLM06:2025 — Excessive Agency:** sesión 9 (agente autónomo, reward hacking).
- **Fuga y extracción de datos** (system prompt leakage, training data extraction): sesiones 3 y 10.

## Sesiones
| # | Tema | Artefacto | Lección central |
|---|------|-----------|-----------------|
| 1 | Gandalf N1–N2 · narrative jailbreak | `writeups/writeup-gandalf-sesion1.md` | El idioma importa; verificar la salida ES parte del ataque (falso negativo) |
| 2 | Gandalf N3 · primer ataque por API | `labs/ataque_llm.py` | Patrón URL→datos→POST→leer JSON |
| 3 | Fuzzer + extracción de datos | `labs/fuzzer_llm.py`, `labs/fuzzer_extraccion.py` | Verificar contra la fuente: el modelo miente con la misma cara con que dice la verdad |
| 4 | Inyección indirecta + su defensa | `labs/asistente.py` | No hay defensa perfecta; solo eliges dónde duele (agujero vs falsos positivos) |
| 5 | Inyección indirecta vía web real | `labs/asistente_web.py`, `labs/asistente_web_naive.py` | Cambiar el canal no cambia el problema |
| 6 | Mismo ataque vs 3 modelos | `labs/comparar_modelos.py` | Capacidad ≠ seguridad; "usa un modelo mejor" no es defensa |
| 7 | 2º modelo de guardia (output verification) | `labs/asistente_con_guardia.py` | La defensa que funciona no es un modelo más caro, es darle CONTEXTO al juez |
| 8 | Inyección de 2º orden vs el guardia | `labs/web_2orden.txt` | Una defensa hecha con un LLM es atacable por el mismo canal que vigila |
| 9 | Primer agente + reward hacking | `labs/agente.py`, `labs/reto/` | Una regla en el prompt no es un límite de seguridad; el barrote va en el sistema (deny-by-default) |
| 10 | Cliente reutilizable (`llm.py`) + primeras métricas | `labs/llm.py`, `labs/prueba_llm.py`, `labs/fuzzer_llm.py` | Refuse-and-leak: el modelo rechaza y filtra el secreto en la misma frase; la métrica caza el falso negativo que el ojo humano pasa por alto. Temperatura = palanca de varianza, no de fuerza |

Los writeups (`writeups/`) llevan el detalle de cada ataque, la defensa, el bypass y la lección.

## Estructura
```
labs/        scripts de cada experimento (ataques y defensas)
writeups/    análisis detallado de cada sesión
prompts/     payloads y páginas maliciosas de los labs
notes/       notas de aprendizaje
```

## Cómo ejecutarlo
1. **LM Studio** sirviendo uno o varios modelos por API local (`/v1/chat/completions`). En estos labs uso `llama-3.2-3b-instruct`, `mistral-small-3.2` y `gemma-3-4b`.
2. **Python 3.12**. Los scripts usan `requests`; los más nuevos importan el cliente reutilizable `labs/llm.py` (`from llm import preguntar`), que devuelve respuesta + tokens + tiempo.
3. En la mayoría de scripts hay que ajustar la **URL del servidor** de LM Studio. Yo trabajo desde WSL2, donde `localhost` no ve el host Windows; la IP se obtiene con `ip route show | grep default` y cambia en cada reinicio.
4. `python3 labs/<script>.py`.

## Hoja de ruta
Este repo está vivo. Próximos pasos:
- **Resultados cuantitativos:** tasas de éxito (ASR), tablas por modelo/temperatura/defensa, gráficas. (La instrumentación base ya existe: `llm.py` registra tokens y tiempo.)
- **Mini eval harness:** correr N payloads × N modelos/defensas con métricas automáticas.
- Reparar el agente de la S9 con un límite real (allowlist de comandos / sandbox sin red) y medir que ya no puede escaparse.

## Aviso
Material educativo y defensivo. Todos los experimentos se ejecutan contra laboratorios de juguete propios y en local. Nada aquí está pensado para atacar sistemas de terceros.

---
**Autor:** Marco · Ingeniería en Ciberseguridad · [github.com/marco99avi-cyber](https://github.com/marco99avi-cyber)
