import paho.mqtt.client as mqtt
import threading

broker = "localhost"  # Broker local
port = 1883  # Porta padrão do MQTT
topic = "chat/mensagens"

# Solicita o nome de usuário ao iniciar a aplicação
username = input("Digite seu username: ")

# Função para processar mensagens recebidas
def on_message(client, userdata, msg):
    # Decodifica a mensagem recebida e a separa em remetente e conteúdo
    payload = msg.payload.decode()
    sender_username, mensagem = payload.split(": ", 1)
    
    # Verifica se a mensagem foi enviada por outro cliente
    if sender_username != username:
        print(f"{sender_username} diz: {mensagem}")

# Função para conectar ao broker
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Conectado com código de retorno: {str(rc)}")
    client.subscribe(topic)

# Função para enviar mensagens
def enviar_mensagens(client):
    while True:
        mensagem = input("Digite sua mensagem: ")
        # Anexa o username à mensagem para identificar o remetente
        client.publish(topic, f"{username}: {mensagem}")

# Criação do cliente MQTT
client = mqtt.Client(client_id=username, protocol=mqtt.MQTTv5)

# Define os callbacks
client.on_connect = on_connect
client.on_message = on_message

# Conecta ao broker
client.connect(broker, port, 60)

# Inicia uma thread separada para envio de mensagens, enquanto a principal fica ouvindo
threading.Thread(target=enviar_mensagens, args=(client,)).start()

# Mantém o cliente escutando novas mensagens
client.loop_forever()

