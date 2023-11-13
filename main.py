import requests as requests
from flask import Flask, jsonify,request,json
import awsgi
from pyathena import connect
from datetime import datetime

app = Flask(__name__)

url_token = "https://api-seguridad.sunat.gob.pe/v1/clientesextranet/39c980ce-544e-4d05-b5b5-3b773c4bddb8/oauth2/token/"

payloadd = 'grant_type=client_credentials&scope=https%3A%2F%2Fapi.sunat.gob.pe%2Fv1%2Fcontribuyente%2Fcontribuyentes&client_id=39c980ce-544e-4d05-b5b5-3b773c4bddb8&client_secret=OlKbXg9Xj0vPjt2IkCt20A%3D%3D'
headerss = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'BIGipServerpool-e-plataformaunica-https=!JPVeQyTpCFQ7RtMHZp9yNlHgef0B46QfzCTQCe1dBTzhCHQUT9BWZrxQYJAOTLaeZ+zFs2/sTHLqbA==; TS019e7fc2=019edc9eb8342c91ebb7e7c7ae91f2fd531370b1d139ca79a553735935e155ec5d1334574d97c081f5cc2e44ccf89b3d1b7cc48ca5'
}

response_token = requests.request("POST", url_token, headers=headerss, data=payloadd)
get_token =  response_token.text
#Extraccion de Token
data = json.loads(get_token)
token = data['access_token']#Receuperacion de Token unico para cada peticion de invoice
#print(token)

@app.route('/tunquiapiconsultasunat/<numRuc>/<codComp>/<numeroSerie>/<numero>/<fechaEmision>/<monto>')
def string(numRuc,codComp,numeroSerie,numero,fechaEmision,monto):

    numRucAPI= numRuc
    codCompAPI= codComp
    numeroSerieAPI = numeroSerie
    numeroAPI = numero
    fechaEmisionAPI= fechaEmision
    montoAPI= monto
    #Formateando fecha para la consulta via rest
    diaAPI= fechaEmisionAPI[8:10]
    mesAPI = fechaEmisionAPI[5:7]
    yearAPI = fechaEmisionAPI[0:4]
    fechaEmisionFormalAPI = diaAPI +'/' +mesAPI+'/'+yearAPI

    url = "https://api.sunat.gob.pe/v1/contribuyente/contribuyentes/20600597940/validarcomprobante"
    payload = json.dumps({
        "numRuc": numRucAPI,
        "codComp": codCompAPI,
        "numeroSerie": numeroSerieAPI,
        "numero": numeroAPI,
        "fechaEmision": fechaEmisionFormalAPI,
        "monto": montoAPI
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Cookie': 'TS012c881c=019edc9eb8b6bc7f71c3e8c4a2a787b98bc9755d9085353e8e33b1d872d3f271362740b89734bf7fa9e3d3837b2c81ce95a3c9f97c'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    mensaje_sunat = response.text
    response_doc_fiscal = json.loads(mensaje_sunat)

    id_boleando = response_doc_fiscal['success']
    format_booleando = json.dumps(id_boleando)

    if format_booleando == "true":
        status_doc_fiscal = response_doc_fiscal['data']['estadoCp']
        if codCompAPI == "01":
            name_doc_fiscal = "FACTURA ELECTRÓNICA"
        elif codCompAPI == "03":
            name_doc_fiscal = "BOLETA DE VENTA ELECTRÓNICA"
        elif codCompAPI == "04":
            name_doc_fiscal = "LIQUIDACIÓN DE COMPRA"
        elif codCompAPI == "07":
            status_ruc_emisor = "NOTA DE CRÉDITO ELECTRÓNICA"
        elif codCompAPI == "08":
            name_doc_fiscal = "NOTA DE DÉBITO ELECTRÓNICA"
        elif codCompAPI == "R1":
            sname_doc_fiscal = "RECIBO POR HONORARIOS"
        elif codCompAPI == "R7":
            name_doc_fiscal = "NOTA DE CREDITO DE RECIBOS"
        else:
            name_doc_fiscal = "TIPO DE COMPROBANTE NO IDENTIFICADO, FAVOR DE VERIFICAR"

        if status_doc_fiscal =="0":
            mensaje_al_mortal  = {"System": "SmartTunquiRestFull","errorCode": "100","Menssage":"LA FACTURA INGRESADA NO EXISTE, VERIFICAR LOS DATOS EN EL PDF Y VOLVER A CONSULTAR","success": "false"}
            return  mensaje_al_mortal

        elif status_doc_fiscal == "1":
            doc_fiscal ="ACEPTADO"
        elif status_doc_fiscal == "2":
            doc_fiscal = "ANULADO"
        elif status_doc_fiscal == "3":
            doc_fiscal = "AUTORIZADO"
        elif status_doc_fiscal == "4":
            doc_fiscal = "NO AUTORIZADO"
        else:
            doc_fiscal = "ESTADO NO IDENTIFICADO, VALIDAR DIRECTO EN SUNAT"
        #FIN DE VALIDACION DE DOCUMENTO FISCAL
        #INICIO DE VALIDACION DE RUC EMISOR
        status_ruc_proveedor = response_doc_fiscal['data']['estadoRuc']
        if status_ruc_proveedor == "00":
            status_ruc_emisor = "ACTIVO"
        elif status_ruc_proveedor == "01":
            status_ruc_emisor = "BAJA_PROVISIONAL"
        elif status_ruc_proveedor == "02":
            status_ruc_emisor = "BAJA PROV. POR OFICIO"
        elif status_ruc_proveedor == "03":
            status_ruc_emisor = "SUSPENSION TEMPORAL"
        elif status_ruc_proveedor == "10":
            status_ruc_emisor = "BAJA DEFINITIVA"
        elif status_ruc_proveedor == "11":
            status_ruc_emisor = "BAJA DE OFICIO"
        elif status_ruc_proveedor == "22":
            status_ruc_emisor = "INHABILITADO-VENT.UNICA"
        else:
            status_ruc_emisor = "ESTADO DE CONTRIBUYENTE NO IDENTIFICADO, VALIDAR EL CONSULTA RUC"
        #FIN DE VALIDACION STATUS DE RUC EMISOR
        #VALIDACION DEL NOMBRE DEL COMPROBANTE
        mensaje_al_mortal = {"fuente": "Servicios Rest SUNAT - RealTime","System": "SmartTunquiRestFull","status_comprobante": doc_fiscal, "ruc_emisor": numRucAPI,"status_ruc_emisor": status_ruc_emisor,"nro_invoice": numeroSerieAPI+'-'+numeroAPI,"type_document_fiscal":name_doc_fiscal,"Importe":montoAPI}
        return  mensaje_al_mortal

    elif format_booleando == "false":
        response_doc_fiscal
    else:
        response_doc_fiscal
    return  response_doc_fiscal
@app.route('/deploy')
def index():
    return jsonify(status=200, message='API SUNAT Online AWS')
def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})

server_name = app.config['SERVER_NAME']
if server_name and ':' in server_name:
    host, port = server_name.split(":")
    port = int(port)
else:
    port = 1248
    host = "0.0.0.0"
    app.run(debug=True,host=host, port=port)

#Consulta de status de Documento Fiscal CHUNAT
