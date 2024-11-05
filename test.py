historico_conversas = {}
def adicionar_conversa(id_user, pergunta, resposta_tiago):
    if id_user not in historico_conversas:
        historico_conversas[id_user] = []
    historico_conversas[id_user].append({
        "pergunta": pergunta,
        "resposta_tiago": resposta_tiago
    })

adicionar_conversa("6ce65d99-796c-4bec-80af-a9df86b9f26f", "Qual é a sua cor favorita?", "Azul")
adicionar_conversa("9f26c2a6-612a-4a6d-8262-965ce7a9b34e", "Que dia é hoje?", "Dia 04")
adicionar_conversa("9f26c2a6-612a-4a6d-8262-965ce7a9b34e", "Qual é o seu animal favorito?", "Gato")
adicionar_conversa("9f26c2a6-612a-4a6d-8262-965ce7a9b34e", "Qual é a sua comida favorita?", "Pizza")
adicionar_conversa("cd11ba0b-52a2-4025-91df-990a2eef0a8f", "Que dia é hoje?", "Não sei, desculpe")


def mostrar_mensagens_usuario(id_user):
    if id_user in historico_conversas:
        for conversa in historico_conversas[id_user]:
            print(f"Pergunta: {conversa['pergunta']}")
            print(f"Resposta de Tiago: {conversa['resposta_tiago']}")
            print("")
    else:
        print(f"Usuário {id_user} não encontrado.")

mostrar_mensagens_usuario("6ce65d99-796c-4bec-80af-a9df86b9f26f")


