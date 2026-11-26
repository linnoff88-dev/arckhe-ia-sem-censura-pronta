# Validaçêo real em Linux — 15/11/2026

-14testes de software passaram, incluindo iniciar/responder/encerrar uma instância simulada.
- Modelo real: `huihui_ai/Qwen3.8-abliterated:27b`, com digest conferido.
- Inferência real dentro de rede isolada contendo somente `lo`.
- Pergunta17+25: respondeu42.
- Contexto em duas mensagens: respondeuLARANJA corretamente.
- Documento fictício: resposta `1000`; gabarito1000; acertou.
- Modelo descarregado e processo próprio encerrado depois dos testes; porta fechada.
- A inferência foi autorizada expressamente pelo Nei, feita um modelo por vez sob fila de GPU.
- Nêo houve teste em Windows/macOS nem implantaçêo em nuvem.

Evidência: [prova-real-linux.json](prova-real-linux.json).

O modelo respondeu também a um pedido benigno de comparaçêo de argumentos sobre censura política. Isso demonstra aquela resposta, nêo garante ausência de recusas em qualquer pedido.
