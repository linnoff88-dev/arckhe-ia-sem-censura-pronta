# IA sin censura lista

[![IA sin censura lista](guia/assets/banner-es.jpg)](https://linnoff88-dev.github.io/

**🇧🇷 [Português](../../README.md) · 🇺🇸 [English](../en/README.md) · 🇪🇸 [Español](README.md)**

[🎬 Video: conversa con tu IA sin internet (audio en portugués).](https://www.youtube.com/watch?v=TJ9omYZdIrE)

Guía completa: https://linnoff88-dev.github.io/

**Validación real en Linux:** se confirmó la ejecución sin red externa, la conversación con contexto y el cierre de los procesos propios. Pasaron las 14 pruebas de software. El modelo acertó los tres casos probados y respondió sobre el tema de debate; esto no mide toda su calidad. Consulta [los resultados completos](../../verificacao/STATUS.md).

## Qué es

Este kit gratuito ejecuta un modelo publicado como abliterated: una versión modificada para tener menos rechazos. Sirve para quienes quieren probar este tipo de modelo en funcionamiento, con conversación y lectura de texto. El modelo se ejecuta en la máquina donde se instala el kit, sin una API externa de inferencia. Necesitas Python, Ollama y suficiente memoria. Menos rechazos no garantiza que acepte todas las solicitudes ni que todas las respuestas sean correctas.

Este kit pone a tu disposición un modelo abliterated para conversar en tu propio ordenador: una versión publicada con menos restricciones de respuesta. El objetivo es ejecutar el modelo de verdad, no solo explicar el tema. El modelo predeterminado es Huihui Qwen3.8-abliterated 27B. También se ejecuta localmente con este kit; menos rechazos y privacidad son características distintas.

**Terminas conversando con un modelo real.** El kit incluye el lanzador, el perfil del modelo, la preparación de los pesos, conversación con contexto, preguntas mediante archivos, un modo Linux sin red y una verificación ejecutable. No necesitas una clave, una suscripción al modelo ni bibliotecas adicionales de Python.

## Requisitos

- Git para clonar, o [descarga el ZIP](https://github.com/linnoff88-dev/ia-sem-censura-pronta/archive/refs/heads/main.zip) y extrae la carpeta.
- Python 3.10 o superior: [instalador oficial](https://www.python.org/downloads/).
- [Ollama instalado](https://ollama.com/download), en Linux, macOS o Windows.
- Para el modelo predeterminado: aproximadamente **18 GB de descarga**, **se recomiendan 32 GB de RAM**, espacio libre para los pesos y recursos para el sistema. El contexto predeterminado es 2048; el consumo real depende del runtime. La GPU es opcional: funciona con CPU, con un rendimiento diferente.
- En Linux, para el modo sin red: `bubblewrap` e `iproute2`. El modo requiere que el sistema permita los espacios de nombres de usuario.

Comprueba antes de empezar:

```bash
python3 --version
ollama --version
```

En Windows, usa `py` en lugar de `python3` si hace falta. Después de instalar Python u Ollama, abre una terminal nueva. El kit no instala paquetes con privilegios ni cambia el Ollama que usan otros proyectos.

## Instalar y conversar

```bash
git clone https://github.com/linnoff88-dev/ia-sem-censura-pronta.git
cd ia-sem-censura-pronta
python3 ia.py diagnostico
python3 ia.py preparar
python3 ia.py verificar
python3 ia.py conversar
```

`preparar` usa internet para descargar o comprobar los pesos del modelo. Después, `verificar` y `conversar` usan el modelo local ya descargado, sin descargar automáticamente otro modelo. Ollama almacena los pesos; no se guardan dentro del repositorio.

Durante la conversación, escribe `/limpar` para reiniciar el contexto y `/sair` para terminar. El kit conserva en memoria solo unos pocos mensajes recientes y no guarda el historial. Al salir, descarga el modelo de la memoria y cierra únicamente su propia instancia y sus procesos hijos. La terminal o el sistema operativo aún pueden registrar lo que aparece en pantalla.

## Linux: conversación con la red bloqueada para el proceso

Después de preparar los pesos, instala los dos componentes del sistema si faltan:

```bash
sudo apt install bubblewrap iproute2
bash sem-rede.sh verificar
bash sem-rede.sh conversar
```

El lanzador crea una red separada que solo tiene la interfaz local `lo`. El modelo y el cliente siguen comunicándose dentro de ella; no hay una interfaz para salir a internet. El ordenador sigue conectado normalmente para los demás programas. Este modo aísla la red, no los archivos del usuario; no es una máquina virtual.

En macOS/Windows, la conversación local funciona con `ia.py`; el lanzador sin red es específico de Linux. Para hacer una comprobación manual en esos sistemas, prepara primero el modelo, desconecta el Wi-Fi o el cable y ejecuta `verificar`. No afirmamos que esta prueba se haya realizado en sistemas que no usamos.

## Pregunta única y archivo

```bash
python3 ia.py perguntar "Escreva três ideias para organizar uma reunião curta."
python3 ia.py perguntar --arquivo exemplos/primeiro-pedido.txt
```

Para texto sensible, prefiere `--arquivo` o la entrada estándar: los argumentos escritos en la línea de comandos pueden quedar en el historial del shell. Las respuestas son texto; el kit no ejecuta los comandos sugeridos por la IA.

## Cómo saber si funcionó

```bash
python3 ia.py verificar
```

La verificación envía una pregunta real al modelo (`17 + 25`) y espera `42`. Guarda el resultado en `.estado/verificacao.json`, con el digest de los pesos, los tokens generados y las interfaces de red. El código de salida 0 significa que ese caso pasó; 1 indica una respuesta distinta; 2 indica un error de preparación o ejecución. Una respuesta correcta no demuestra competencia general ni ausencia de rechazos.

Lee también [verificacao/STATUS.md](../../verificacao/STATUS.md): distingue las pruebas de software de la inferencia realmente ejecutada. La respuesta correcta de un segundo ejercicio está en `exemplos/documento-ficticio.txt`.

## Qué significa cada elección

**Privacidad:** quién recibe los datos y dónde se ejecuta la tarea. En este kit, la solicitud solo llega a la instancia propia de Ollama en `127.0.0.1`. La nube y las herramientas externas están desactivadas. El modo Linux sin red añade una restricción del sistema operativo.

**Sin censura:** modelo publicado por quien lo mantiene con menos rechazos. Este término no promete que acepte todas las solicitudes, que todas las respuestas sean correctas ni que sustituya la revisión humana. El kit no añade filtros temáticos ni modifica el modelo automáticamente.

## Modelo, versión y memoria

El perfil usa **`huihui_ai/Qwen3.8-abliterated:27b`**, comprobado el 15/11/2026. `perfil.json` registra el digest esperado de los pesos para impedir que el modelo cambie sin aviso. Si quien lo mantiene cambia la etiqueta y el digest deja de coincidir, la ejecución se detiene: comprueba la nueva versión antes de actualizar `digest_esperado`. No elimines la comprobación solo para continuar.

El perfil limita el contexto a 2048 y la respuesta a 512 tokens. La conversación tiene una ventana breve; hay que dividir los documentos largos. La primera respuesta tarda más porque incluye la carga de los pesos. Si falta memoria, usa una máquina con capacidad adecuada o elige conscientemente otro modelo local, ajustando el nombre y el digest. No hay alternativa automática en la nube.

## Comportamientos importantes

- Instancia propia, puerto exclusivo y nube desactivada. Si el puerto está ocupado, se produce un error; nunca nos conectamos en silencio a otro servicio.
- Las solicitudes no se envían a proxies heredados y se rechazan las redirecciones HTTP.
- Un nombre de modelo remoto, la ausencia de pesos, un digest distinto o una respuesta vacía interrumpen la ejecución.
- No hay conectores, búsquedas web, agentes que ejecuten herramientas ni publicaciones automáticas.
- La privacidad de este flujo no protege frente a malware, administradores del ordenador, capturas de pantalla, copias de seguridad ni un runtime comprometido.

## Pruebas de software

```bash
python3 -m unittest discover -s tests -v
```

Estas pruebas usan un runtime simulado y no cuentan como una prueba del modelo. La prueba con IA real es `verificar`.

## Documentación de las herramientas

[Ollama: ejecución local y nube](https://docs.ollama.com/faq) · [API local de conversación](https://docs.ollama.com/api/chat) · [Modelo predeterminado](https://ollama.com/huihui_ai/Qwen3.8-abliterated:27b).

El código del kit tiene licencia MIT. El runtime y los pesos tienen sus propias licencias; aquí no se redistribuyen los pesos.

## Si descargaste el ZIP

Extrae la carpeta. En Windows, abre la carpeta que contiene ia.py, haz clic en la barra de direcciones, escribe powershell y presiona Enter. Ejecuta los comandos de Python de la guía, usando py si es necesario. Los accesos directos preparar.cmd y conversar.cmd también funcionan con doble clic. En Linux/macOS, abre Terminal y usa cd para entrar en la carpeta extraída; la ruta depende de dónde guardaste el ZIP. No ejecutes git clone si elegiste el ZIP.

Runtime es el programa que ejecuta el modelo; digest es la identificación exacta de los pesos; un espacio de nombres de red es una red separada para el proceso en Linux. Si cambia el digest, el error muestra los valores esperado y encontrado: confirma la versión en la página oficial de la etiqueta antes de decidir actualizar digest_esperado en perfil.json. Sin confirmación, conserva la protección.
