# Contrato da entrega

Este kit executa **huihui_ai/Qwen3.8-abliterated:27b** no computador do usuário e oferece conversa no terminal, perguntas por arquivo e verificação real da resposta. O perfil sem-censura define a finalidade do kit. Preparar exige baixar o runtime Ollama e os pesos; usar um modelo já presente não baixa pesos automaticamente.

O runtime próprio fica em 127.0.0.1:11542, com OLLAMA_NO_CLOUD=1. O programa não usa o servidor global em11434, não habilita busca, extensões ou ferramentas e não envia conteúdo a provedores de inferência. O cliente HTTP ignora proxies e redirecionamentos; só fala com a porta local fixa da instância própria. Não há histórico salvo pelo kit; o usuário pode salvar a saída por redirecionamento do terminal.

Privacidade é uma propriedade deste caminho de processamento, não proteção contra malware, administrador do computador, gravação de tela, backup do sistema ou componentes comprometidos. O modo normal desativa nuvem mas não é um bloqueio de rede do sistema operacional. A prova com rede isolada, quando disponível no Linux, é uma evidência separada.

O termo sem censura indica modelo publicado pelo mantenedor como abliterated, com menos recusas. Não existe garantia de aceitar todo pedido ou de acertar respostas. Nenhum filtro local adicional é colocado sobre a resposta. As instruções para admitir incerteza não são um filtro de temas. Nenhum kit executa comandos gerados pelo modelo.

Pronto significa: runtime inicia no endereço local, modelo existe e é local, pergunta conhecida recebe resposta de modelo real, conversa mantém contexto e saída encerra somente os processos próprios. Testes simulados não contam como inferência real.
