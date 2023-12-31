# SmartTunqui AWS Rest Full - AWS PERUUUU

_Sistema que permite consultar cualquier tipo de documento fiscal en SUNAT en tiempo Real
## Desploy 📦

_Agrega notas referenciales al deploy a realizar previa validacion en tu ambiente local._
https://www.youtube.com/watch?v=snDW-5n01ak

#URL Invoque service rest

https://38dieon4wh.execute-api.us-east-2.amazonaws.com/Develpment

## Construido con 🛠️

_Herramientas utilizadas para este proyecto_

* [Flask - Python](https://flask.palletsprojects.com/en/3.0.x/) - ID de Desarrollo
* [Servicios Rest Full](https://cdn.www.gob.pe/uploads/document/file/536289/Manual_de_Consulta_Integrada_de_Validez_de_CdP_por_Servicio_WEB.pdf?v=1583255585) - Servicios Implementados de SUNAT
## Tipo de Documentos Fiscales habilitados para la validacion 📦

* 01 FACTURA  
* 03 BOLETA DE VENTA  
* 04 LIQUIDACIÓN DE COMPRA
* 07 NOTA DE CREDITO
* 08 NOTA DE DEBITO
* R1 RECIBO POR HONORARIOS
* R7 NOTA DE CREDITO DE RECIBOS

## Example de Request ✒️
-Url para consulta via metodo Get!!!
http://10.84.8.2:2069/tunquiapiconsultasunat/20511315922/01/F001/658376/2023-11-07/6723.72

  _Request con exito!!!

````json response success!!!
{
   "Importe": "6723.72",
   "System": "SmartTunquiRestFull",
   "fuente": "Servicios Rest SUNAT - RealTime",
   "nro_invoice": "F001-658376",
   "ruc_emisor": "20511315922",
   "status_comprobante": "ACEPTADO",
   "status_ruc_emisor": "ACTIVO",
   "type_document_fiscal": "FACTURA ELECTRÓNICA"
}

````
 _Request con error!!!
````json response success!!!
{
    "errorCode": "99",
    "message": "Error en los criterios de consulta enviados(Nro de Serie incorrecto)",
    "success": false
}

````

## Autores ✒️

_Personas Involucradas en el Inicio del Desarrollo_

* **Luis Azañero** - *Desarrollo del Proyecto* - [DevSmartFitPeru](https://github.com/DevSmartFitPeru)
* **Michael Balladares** - *Trabajo de Implementacion* - [DevSmartFitPeru](https://github.com/DevSmartFitPeru)
* **Carlos Prado Tarma** - *Aprobacion del Proyecto* - [DevSmartFitPeru](https://github.com/DevSmartFitPeru)

* Ayuda a tus colegas e mejorar el proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* Somos TI Perú

---
⌨️ con ❤️ por [Dev Luis Azañero](https://github.com/Luis-Azanero-Developer) 😊
