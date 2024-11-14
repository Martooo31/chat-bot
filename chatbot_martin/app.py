import streamlit as st #libreria 
from groq import Groq #importamos libreria
st.set_page_config(page_title="Mi ChatBot", page_icon="⚡")

opciones =['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']   #selector de opciones 

#conexion con la API, creando usuario
def crear_usuario_grog():
    clave_secreta = st.secrets["CLAVE_API"]#llama la clave de la api
    return Groq(api_key = clave_secreta)# nos conectamos 

def configurar_modelo(cliente,modelo,mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, #llama a al modelo de la ia
        messages = [{"role":"user","content": mensajeDeEntrada}],
        stream = True #funcionalidad de que me responda en tiempo real
    )#devuelve la respuesta  que manda la ia

#historial de mensaje 
def inicializar_estado():
    if "mensajes" not in st.session_state:
     st.session_state.mensajes = [] # []historial vacio

def configurar_pag():
    st.title("El ChatBot de Martin ")
    st.sidebar.title("Configuraciones")
    opcion = st.sidebar.selectbox(
        "Modos",
        options = opciones,
        index = 0  
    )
    return opcion #nos devuelve el nombre del modelo

def actualizar_historial(rol, contenido, avatar):#rol, contenido y avatar cambian constantemente
    st.session_state.mensajes.append(
        {"role":rol, "content":contenido, "avatar":avatar}
    ) #metodo append agrega datos a la lista

def mostrar_historial():
     for mensaje in st.session_state.mensajes:
         with st.chat_message(mensaje["role"],avatar= mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDeChat = st.container(height= 400, border = True)
    with contenedorDeChat : mostrar_historial()             

def generar_respuesta(chat_completo):
    respuesta_completa = ""#estoy logrando una variable vacia
    for frase in chat_completo:
        if frase.choices[0].delta.content:#evtiamos el dato NONE
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa        


#INVOCACION DE FUNCIONES
modelo = configurar_pag()#agarramos el modelo seleccionado 
clienteUsuario = crear_usuario_grog()#conecta con la API GROQ
inicializar_estado()#se crea en memoria el historial vacio 
area_chat()#se crea la agrupacion de los mensajes 

mensaje = st.chat_input("escribe aqui lo que quieras buscar...")
#verificar que cuando nos manden un mensaje tenga algo
if mensaje: 
    actualizar_historial("user",mensaje, "♟️")#mostramos el mensaje en el chat
    respuesta_ia = configurar_modelo(clienteUsuario,modelo,mensaje)#obtenemos la respuesta de la ia
    if respuesta_ia: #verificamos que la variable tenga algo
        with st.chat_message("assistant"):
            respuesta_completa = st.write_stream(generar_respuesta(respuesta_ia))
            actualizar_historial("assistant", respuesta_completa,"🤖")
            st.rerun()



#codigo para empezar el programa (py -m streamlit run chatbot.py)


