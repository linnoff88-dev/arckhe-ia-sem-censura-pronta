# Uncensored AI, ready to use

[![Uncensored AI, ready to use](guia/assets/banner-en.jpg)](https://linnoff88-dev.github.io/

**🇧🇷 [Português](../../README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](../es/README.md)**

[🎬 Video: talk to your AI without internet (audio in Portuguese).](https://www.youtube.com/watch?v=TJ9omYZdIrE)

Full guide: https://linnoff88-dev.github.io/

**Real Linux validation:** execution without an external network, a contextual conversation, and shutdown of the dedicated processes were confirmed. All 14 software tests passed. The model answered correctly on two tested cases, got the private-kit account wrong (answer: 600; expected: 1000), and answered the debate topic. These results do not measure its overall quality. See [the complete results](../../verificacao/STATUS.md).

## What it is

This free kit runs a model published as abliterated: a modified version designed to have fewer refusals. It is for anyone who wants to try this type of model in practice, with conversation and text reading. The model runs on the machine where the kit is installed, with no external inference API. You need Python, Ollama, and enough memory. Fewer refusals do not guarantee that it will accept every request or answer every question correctly.

This kit runs an abliterated model for you to chat with on your own computer: a published version with fewer response restrictions. The focus is on running the model for real, not just explaining the topic. The default is Huihui Qwen3.8-abliterated 27B. It also runs locally in this kit; fewer refusals and privacy remain distinct properties.

**You finish by chatting with a real model.** The kit includes the launcher, model profile, weight preparation, contextual conversation, file-based questions, a Linux offline mode, and an executable check. No key, model subscription, or extra Python libraries are required.

## Requirements

- Git to clone, or [download the ZIP](https://github.com/linnoff88-dev/ia-sem-censura-pronta/archive/refs/heads/main.zip) and extract the folder.
- Python 3.10 or newer: [official installer](https://www.python.org/downloads/).
- [Ollama installed](https://ollama.com/download), on Linux, macOS, or Windows.
- For the default model: approximately **18 GB to download**, **32 GB RAM recommended**, free space for the weights, and resources for the system. Default context: 2048; actual memory use depends on the runtime. A GPU is optional: CPU works, with different performance.
- On Linux, for offline mode: `bubblewrap` and `iproute2`. This mode requires user namespaces to be allowed by the system.

Check before you start:

```bash
python3 --version
ollama --version
```

On Windows, use `py` instead of `python3` if needed. After installing Python or Ollama, open a new terminal. The kit does not install packages with elevated privileges or change the Ollama used by other projects.

## Install and chat

```bash
git clone https://github.com/linnoff88-dev/ia-sem-censura-pronta.git
cd ia-sem-censura-pronta
python3 ia.py diagnostico
python3 ia.py preparar
python3 ia.py verificar
python3 ia.py conversar
```

`preparar` uses the internet to download or check the model weights. Afterward, `verificar` and `conversar` use the downloaded local model without automatically downloading another one. The weights are stored by Ollama itself, not in the repository.

During the conversation, type `/limpar` to reset the context and `/sair` to exit. The kit keeps only a few recent messages in memory and does not save a history. When you exit, it unloads the model and stops only its own instance and child processes. The terminal or operating system may still record what appears on screen.

## Linux: block the process's network access

After preparing the weights, install the two system tools if they are missing:

```bash
sudo apt install bubblewrap iproute2
bash sem-rede.sh verificar
bash sem-rede.sh conversar
```

The launcher creates a separate network with only the local `lo` interface. The model and client continue to communicate inside it; there is no interface for accessing the internet. The computer remains connected normally for other programs. This mode isolates the network, not user files; it is not a virtual machine.

On macOS/Windows, local conversation works through `ia.py`; the offline launcher is Linux-specific. For a manual check on these systems, prepare first, disconnect Wi-Fi/cable, and run `verificar`. We do not claim to have run this test on systems we did not use.

## Single question and file

```bash
python3 ia.py perguntar "Escreva três ideias para organizar uma reuniêo curta."
python3 ia.py perguntar --arquivo exemplos/primeiro-pedido.txt
```

For sensitive text, prefer `--arquivo` or standard input: arguments typed on the command line may remain in shell history. Answers are text; the kit does not execute commands suggested by the AI.

## How to tell it worked

```bash
python3 ia.py verificar
```

The check sends a real question to the model (`17 + 25`) and expects `42`. It saves the result to `.estado/verificacao.json`, including the weights' digest, generated tokens, and network interfaces. Exit code 0 means this case passed; 1 indicates a different answer; 2 indicates a preparation/execution error. A correct answer does not prove general competence or an absence of refusals.

Also read [verificacao/STATUS.md](../../verificacao/STATUS.md): it distinguishes software tests from inference that was actually run. The answer key for a second exercise is in `exemplos/documento-ficticio.txt`.

## What each choice means

**Privacy:** who receives the data and where the task runs. In this kit, the request goes only to the dedicated Ollama instance at `127.0.0.1`. Cloud and external tools are disabled. Linux offline mode adds an operating-system restriction.

**Uncensored:** a model published by its maintainer with fewer refusals. This term does not promise acceptance of every request, accuracy on every answer, or a replacement for human review. The kit adds no topic filters and does not modify the model automatically.

## Model, version, and memory

The profile uses **`huihui_ai/Qwen3.8-abliterated:27b`**, checked on 15/11/2026. `perfil.json` records the expected weights digest to prevent a silent model change. If the maintainer changes the tag and the digest no longer matches, execution stops: check the new version before updating `digest_esperado`. Do not remove the check just to make it pass.

The profile limits context to 2048 and responses to 512 tokens. The conversation window is short; long documents need to be split. The first response time includes loading the weights. If memory is insufficient, use a machine with adequate capacity or consciously choose another local model, adjusting its name and digest. There is no cloud fallback.

## Important behavior

- Dedicated instance, exclusive port, and cloud disabled. An occupied port causes an error; the kit never silently connects to another service.
- Inherited proxies do not receive requests, and HTTP redirects are rejected.
- A remote model name, missing weights, a different digest, or an empty response stops execution.
- No connectors, web search, agents that execute tools, or automatic publishing.
- This workflow's privacy does not protect against malware, computer administrators, screen capture, backups, or a compromised runtime.

## Software tests

```bash
python3 -m unittest discover -s tests -v
```

These tests use a simulated runtime and do not count as a model test. The real AI test is `verificar`.

## Tool documentation

[Ollama: local execution and cloud](https://docs.ollama.com/faq) · [Local chat API](https://docs.ollama.com/api/chat) · [Default model](https://ollama.com/huihui_ai/Qwen3.8-abliterated:27b).

Kit code: MIT. The runtime and weights have their own licenses; the weights are not redistributed here.

## If you downloaded the ZIP

Extract the folder. On Windows, open the folder containing ia.py, click the address bar, type powershell, and press Enter. Run the Python commands in the guide, using py if needed. The preparar.cmd and conversar.cmd shortcuts also work with a double-click. On Linux/macOS, open Terminal and use cd to enter the extracted folder; the path depends on where you saved the ZIP. Do not run git clone if you chose the ZIP.

Runtime is the program that runs the model; digest is the exact identification of the weights; a network namespace is a separate network for the process on Linux. If the digest changes, the error shows the expected and found values: confirm the version on the tag's official page before deciding to update digest_esperado in perfil.json. Without confirmation, keep the protection.
