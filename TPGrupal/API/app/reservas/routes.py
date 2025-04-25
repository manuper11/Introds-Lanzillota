import os
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging
import secrets
import datetime

reservas_bp = Blueprint('reservas', __name__)

def calculo_precio_total(cantidad_habitaciones, cantidad_noches, habitacion_id):
    try:
        engine = current_app.config['engine']
        conn = engine.connect()
        
        query = text("SELECT precio_noche FROM Habitaciones WHERE id = :habitacion_id")
        result = conn.execute(query, {'habitacion_id': habitacion_id})
        row = result.fetchone()
        
        if not row:
            return False, "Habitación no encontrada"

        precio_por_noche = float(row[0])
        precio_total = precio_por_noche * int(cantidad_habitaciones) * int(cantidad_noches)

        return True, precio_total
    
    except SQLAlchemyError as e:
        return False, str(e)
    
    finally:
        if conn:
            conn.close()

@reservas_bp.route('/calcular-precio', methods=['GET'])
def calcular_precio():

    habitacion_id = request.args.get('habitacionId')
    cantidad_habitaciones = request.args.get('cantidadHabitaciones')
    cantidad_noches = request.args.get('cantidadNoches')

    if not habitacion_id or not cantidad_habitaciones or not cantidad_noches:
        return jsonify({"success": False, "message": "Falta alguno de los parametros obligatorios: cantidadHabitaciones, cantidadNoches, habitacionId"}), 400

    try:
        cantidad_habitaciones = int(cantidad_habitaciones)
        cantidad_noches = int(cantidad_noches)
    except ValueError:
        return jsonify({"success": False, "message": "Los parámetros cantidadHabitaciones y cantidadNoches deben ser números enteros"}), 400

    if cantidad_habitaciones <= 0 or cantidad_noches <= 0:
        return jsonify({"success": False, "message": "Los parámetros cantidadHabitaciones y cantidadNoches deben ser mayores que cero"}), 400

    try:
        exito, resultado = calculo_precio_total(cantidad_habitaciones, cantidad_noches, habitacion_id)
    
        if exito:
            return jsonify({"success": True, "precioTotal": resultado}), 200
        else:
            return jsonify({"success": False, "message": resultado}), 400
    
    except Exception as e:
        logging.error(f"General Error: {str(e)}")
        return jsonify({"success": False, "message": "Error del servidor"}), 500


@reservas_bp.route('/', methods=['POST'])
def create_reserva():
    data = request.json
    query = text("""
        INSERT INTO Reservas (email_cliente, nombre_cliente, telefono_cliente, fecha_desde, fecha_hasta, 
            cantidad_habitaciones, cantidad_personas, metodo_pago, estado, precio_total, habitacion_id, codigo_reserva) 
        VALUES (:email_cliente, :nombre_cliente, :telefono_cliente, :fecha_desde, :fecha_hasta, :cantidad_habitaciones, 
            :cantidad_personas, :metodo_pago, :estado, :precio_total, :habitacion_id, :codigo_reserva)
        """)
    
    try:
        engine = current_app.config['engine']
        conn = engine.connect()

        # Calcular la cantidad de noches
        fecha_desde = datetime.datetime.strptime(data['fecha_desde'], '%Y-%m-%d')
        fecha_hasta = datetime.datetime.strptime(data['fecha_hasta'], '%Y-%m-%d')
        cantidad_noches = (fecha_hasta - fecha_desde).days
        
        if cantidad_noches <= 0:
            return jsonify({"success": False, "message": "La fecha 'hasta' debe ser posterior a la fecha 'desde'"}), 400

        exito_calculo_precio, resultado_calculo = calculo_precio_total(data['cantidad_habitaciones'], cantidad_noches, data['habitacion_id'])
    
        if exito_calculo_precio:
            precio_total_reserva = resultado_calculo
        else:
            return jsonify({"success": False, "message": resultado_calculo}), 400
        

        codigo_reserva = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(6))
        
        conn.execute(query, {
            'email_cliente': data['email_cliente'],
            'nombre_cliente': data['nombre_cliente'],
            'telefono_cliente': data['telefono_cliente'],
            'fecha_desde': data['fecha_desde'],
            'fecha_hasta': data['fecha_hasta'],
            'cantidad_habitaciones': data['cantidad_habitaciones'],
            'cantidad_personas': data['cantidad_personas'],
            'metodo_pago': data['metodo_pago'],
            'estado': "aceptada",
            'precio_total': precio_total_reserva,
            'habitacion_id': data['habitacion_id'],
            'codigo_reserva': codigo_reserva
        })

        template_confirmacion_id = "d-67983c7f34e346e7b32b820d2eda80af"
        titulo = "¡Felicidades! Su reserva ha sido confirmada"
        subtitulo = "Codigo de reserva: " + codigo_reserva

        dynamic_template_data = {
            'resultado': titulo,
            'subtitulo_resultado': subtitulo,
            'desde': data['fecha_desde'],
            'hasta': data['fecha_hasta'],
            'nombre_cliente': data['nombre_cliente'],
            'habitaciones': data['cantidad_habitaciones'],
            'personas': data['cantidad_personas'],
            'precio': precio_total_reserva,
            'metodo': data['metodo_pago']
        }
        
        send_email(
            data['email_cliente'],
            dynamic_template_data,
            template_confirmacion_id
        )
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Reserva añadida correctamente", "codigo_reserva": codigo_reserva}), 200
    
    except SQLAlchemyError as e:
        logging.error(f"SQL Error: {str(e)}")
        error = str(e.__cause__)
        conn.close()
        return jsonify({"success": False, "message": error}), 500
    
    except Exception as e:
        logging.error(f"General Error: {str(e)}")
        if conn:
            conn.close()
        return jsonify({"success": False, "message": "Error del servidor"}), 500
    
@reservas_bp.route('/', methods=['GET'])
def get_reservas():
    estado = request.args.get('estado')
    codigo_reserva = request.args.get('codigo_reserva')

    query = "SELECT r.*, h.nombre FROM Reservas r INNER JOIN Habitaciones h ON r.habitacion_id = h.id WHERE 1 = 1"
    params = {}

    if estado:
        query += " AND r.estado = :estado"
        params['estado'] = estado

    if codigo_reserva:
        query += " AND r.codigo_reserva = :codigo_reserva"
        params['codigo_reserva'] = codigo_reserva

    try:
        engine = current_app.config['engine']
        conn = engine.connect()
        result = conn.execute(text(query), params)
        reservas = []
        for row in result:
            reserva = {
                'id': row[0],
                'email_cliente': row[1],
                'nombre_cliente': row[2],
                'telefono_cliente': row[3],
                'fecha_desde': row[4].strftime('%Y-%m-%d'),
                'fecha_hasta': row[5].strftime('%Y-%m-%d'),
                'cantidad_habitaciones': row[6],
                'cantidad_personas': row[7],
                'metodo_pago': row[8],
                'estado': row[9],
                'motivo_rechazo': row[10],
                'precio_total': row[11],
                'habitacion_id': row[12],
                'codigo_reserva': row[13],
                'tipo_habitacion': row[14]
            }
            reservas.append(reserva)
        conn.close()
        return jsonify({"success": True, "reservas": reservas}), 200
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        if(conn):
            conn.close()
        return jsonify({"success": False, "message": error}), 500
    except Exception as e:
        error = str(e.__cause__)
        if(conn):
            conn.close()
        return jsonify({"success": False, "message": error}), 500
    


@reservas_bp.route('/<int:id>/update', methods=['PUT'])
def update_reserva(id):
    data = request.json
    estado = data['estado']
    
    if estado not in ['rechazada']:
        return jsonify({"success": False, "message": "Estado inválido. Solo se permite 'rechazada'."}), 400
    
    motivo_rechazo = data['motivo_rechazo']
    query_update = text("""
        UPDATE Reservas 
        SET estado = :estado, motivo_rechazo = :motivo_rechazo
        WHERE id = :id
        """)
    
    query_select = text("""
        SELECT R.email_cliente, R.nombre_cliente, R.telefono_cliente, R.fecha_desde, R.fecha_hasta, 
                R.cantidad_habitaciones, R.cantidad_personas, R.metodo_pago, R.precio_total, H.nombre, R.codigo_reserva
        FROM Reservas R
        INNER JOIN Habitaciones H ON R.habitacion_id = H.id
        WHERE R.id = :id
        """)
        
    try:
        engine = current_app.config['engine']
        conn = engine.connect()

        result_get_reserva = conn.execute(query_select, {'id': id})

        if result_get_reserva.rowcount == 0:
            conn.close()
            return jsonify({"success": False, "message": "Reserva no encontrada"}), 404
        
        conn.execute(query_update, {
            'estado': estado,
            'motivo_rechazo': motivo_rechazo,
            'id': id
        })
        
        reserva = result_get_reserva.fetchone()
        reserva_data = {
            'email_cliente': reserva[0],
            'nombre_cliente': reserva[1],
            'telefono_cliente': reserva[2],
            'fecha_desde': reserva[3],
            'fecha_hasta': reserva[4],
            'cantidad_habitaciones': reserva[5],
            'cantidad_personas': reserva[6],
            'metodo_pago': reserva[7],
            'precio_total': reserva[8],
            'nombre_habitacion': reserva[9],
            'codigo_reserva': reserva[10]
        }

        if estado == 'rechazada':
            titulo = "Lo sentimos, su reserva ha sido rechazada"
            subtitulo = "Hemos dado de baja su reserva " + reserva_data["codigo_reserva"]
        else:
            titulo = ""
            subtitulo = ""

        template_confirmacion_id = "d-18e23cf95aaf4d5ea38a78406d9757d2"

        dynamic_template_data = {
            'resultado': titulo,
            'subtitulo_resultado': subtitulo,
            'datos': f"Motivo: {motivo_rechazo}"
        }
        
        send_email(
            reserva_data['email_cliente'],
            dynamic_template_data,
            template_confirmacion_id
        )
        
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Reserva actualizada correctamente"}), 200
    
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        conn.close()
        return jsonify({"success": False, "message": error}), 500

def send_email(to_email, dynamic_template_data, template_id):

    from_email = 'mriveiro@fi.uba.ar'
    
    message = Mail(
        from_email=from_email,
        to_emails=to_email
    )
    message.template_id = template_id
    message.dynamic_template_data = dynamic_template_data

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        logging.info(f'Status Code: {response.status_code}')
        logging.info(f'Response Body: {response.body}')
        logging.info(f'Response Headers: {response.headers}')
    except Exception as e:
        logging.error(f'Error: {str(e)}')


@reservas_bp.route('/check-disponibilidad', methods=['GET'])
def check_disponibilidad():
    habitacion_id = request.args.get('habitacionId')
    cantidad_habitaciones = int(request.args.get('cantidadHabitaciones'))
    fecha_desde = request.args.get('fechaDesde')
    fecha_hasta = request.args.get('fechaHasta')

    if not habitacion_id or not cantidad_habitaciones or not fecha_desde or not fecha_hasta:
        return jsonify({"success": False, "message": "Falta alguno de los parametros obligatorios: habitacionId, cantidadHabitaciones, fechaDesde, fechaHasta"}), 400

    try:
        fecha_desde = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d')
        fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d')
    except ValueError:
        return jsonify({"success": False, "message": "Formato de fecha incorrecto. Use 'YYYY-MM-DD'"}), 400

    if fecha_hasta <= fecha_desde:
        return jsonify({"success": False, "message": "La fecha 'hasta' debe ser posterior a la fecha 'desde'"}), 400

    try:
        engine = current_app.config['engine']
        conn = engine.connect()

        query_habitacion = text("SELECT cantidad_disponible FROM Habitaciones WHERE id = :habitacion_id")
        result_query_habitacion = conn.execute(query_habitacion, {'habitacion_id': habitacion_id})
        
        if result_query_habitacion.rowcount == 0:
            conn.close()
            return jsonify({"success": False, "message": "Habitación no encontrada"}), 404

        habitacion_total_disponible = result_query_habitacion.fetchone()[0]
        
        query_ocupacion = text("""
            SELECT SUM(cantidad_habitaciones) 
            FROM Reservas 
            WHERE habitacion_id = :habitacion_id 
            AND (
                (fecha_desde <= :fecha_desde AND fecha_hasta >= :fecha_desde) OR 
                (fecha_desde <= :fecha_hasta AND fecha_hasta >= :fecha_hasta) OR
                (fecha_desde >= :fecha_desde AND fecha_hasta <= :fecha_hasta)
            )
            AND estado = 'aceptada'
        """)
        result_query_ocupacion = conn.execute(query_ocupacion, {'habitacion_id': habitacion_id, 'fecha_desde': fecha_desde, 'fecha_hasta': fecha_hasta})
        cantidad_ocupadas = result_query_ocupacion.fetchone()[0] or 0
        
        disponibles = habitacion_total_disponible - cantidad_ocupadas
        
        if disponibles >= cantidad_habitaciones:
            # Si hay disponibilidad calcular precio total
            cantidad_noches = (fecha_hasta - fecha_desde).days
            exito, precio_total = calculo_precio_total(cantidad_habitaciones, cantidad_noches, habitacion_id)
            if exito:
                return jsonify({"success": True, "disponible": True, "precioTotal": precio_total}), 200
            else:
                return jsonify({"success": False, "message": "Error al calcular precio total: " + precio_total}), 500
        else:
            return jsonify({"success": True, "disponible": False, "message": "No hay disponibilidad para el tipo de habitacion en las fechas solicitadas"}), 200

    except SQLAlchemyError as e:
        logging.error(f"SQL Error: {str(e)}")
        conn.close()
        return jsonify({"success": False, "message": "Error del servidor"}), 500
    
    except Exception as e:
        logging.error(f"General Error: {str(e)}")
        if conn:
            conn.close()
        return jsonify({"success": False, "message": "Error del servidor"}), 500