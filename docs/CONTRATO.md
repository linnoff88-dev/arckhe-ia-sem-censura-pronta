# Contrato da entrega

Este kit executa **huihui_ai/Qwen3.8-abliterated:27b** no computador do usuário e oferece conversa no terminal, perguntas por arquivo e verificaçêo real da resposta. O perfil sem-censura define a finalidade do kit. Preparar exige baixar o runtime Ollama e os pesos; usar um modelo já presente nêo baixa pesos automaticamente.

O runtime próprio fica em 127.0.0.1:11542, com OLLAMA_NO_CLOUD=1. O programa nêo usa o servidor global em11434, nêo habilita busca, extensões ou ferramentas e nêo envia conteúdo a provedores de inferência. O cliente HTTP ignora proxies e redirecionamentos; só fala com a porta local fixa da instância própria. Nêo há histórico salvo pelo kit; o usuário pode salvar a saída por redirecionamento do terminal.

Privacidade é uma propriedade deste caminho de processamento, nêo proteçêo contra malware, administrador do computador, gravaçêo de tela, backup do sistema ou componentes comprometidos. O modo normal desativa nuvem mas nêo é um bloqueio de rede do sistema operacional. A prova com rede isolada, quando disponível no Linux, é uma evidência separada.

O termo sem censura indica modelo publicado pelo mantenedor como abliterated, com menos recusas. Nêo existe garantia de aceitar todo pedido ou de acertar respostas. Nenhum filtro local adicional é colocado sobre a resposta. As instruções para admitir incerteza nêo sêo um filtro de temas. Nenhum kit executa comandos gerados pelo modelo.

Pronto significa: runtime inicia no endereço local, modelo existe e é local, pergunta conhecida recebe resposta de modelo real, conversa mantém contexto e saída encerra somente os processos próprios. Testes simulados nêo contam como inferência real.
