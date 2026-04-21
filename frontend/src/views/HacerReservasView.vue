<template>
  <div class="contenedor-reservas">
    <div class="tarjeta-reserva">
      <h2>Reservar Espacio</h2>
      <p v-if="salaNombre" class="sala-seleccionada">Estás reservando: <strong>{{ salaNombre }}</strong></p>

      <form @submit.prevent="confirmarReserva" class="formulario">
        <div class="campo">
          <label>Fecha</label>
          <input v-model="fecha" type="date" :min="hoy" required>
        </div>

        <div class="campo-grupo">
          <div class="campo">
            <label>Hora Inicio</label>
            <input v-model="horaInicio" type="time" required>
          </div>
          <div class="campo">
            <label>Hora Fin</label>
            <input v-model="horaFin" type="time" required>
          </div>
        </div>

        <button type="submit" :disabled="cargando" class="boton-reserva">
          {{ cargando ? 'Procesando...' : 'Confirmar Reserva' }}
        </button>
      </form>

      <p v-if="mensaje" :class="['mensaje', esError ? 'error' : 'exito']">
        {{ mensaje }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ReservasView',
  data() {
    return {
      salaId: this.$route.query.sala || null,
      salaNombre: this.$route.query.nombre || '',
      fecha: '',
      horaInicio: '',
      horaFin: '',
      cargando: false,
      mensaje: '',
      esError: false,
      hoy: new Date().toISOString().split('T')[0]
    }
  },
  methods: {
    async confirmarReserva() {
        this.cargando = true;
        this.mensaje = '';
        
        try {
            const token = localStorage.getItem('user-token');

            // 1. Preparamos las fechas en el formato que espera tu Python: AAAA-MM-DD HH:MM:SS
            // Concatenamos la fecha seleccionada con la hora y añadimos ":00" para los segundos
            const inicioCompleto = `${this.fecha} ${this.horaInicio}:00`;
            const finCompleto = `${this.fecha} ${this.horaFin}:00`;

            const datosReserva = {
            room_id: this.salaId,
            start_time: inicioCompleto, // Enviamos el string completo
            end_time: finCompleto
            };

            // 2. Ajustamos la URL a la que definiste en tu archivo bookings.py
            await axios.post('http://localhost:8000/api/bookings/', datosReserva, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
            });

            this.esError = false;
            this.mensaje = "¡Reserva realizada con éxito!";
            
            // Redirigir a "Mis Reservas" para que el usuario vea su reserva recién creada
            setTimeout(() => this.$router.push('/mis-reservas'), 2000);

        } catch (err) {
            this.esError = true;
            // Si hay solapamiento, tu Python devuelve el mensaje "La sala ya está reservada..."
            this.mensaje = err.response?.data?.message || "Error al realizar la reserva";
        } finally {
            this.cargando = false;
        }
        }
  }
}
</script>

<style lang="scss" scoped>
.contenedor-reservas {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.tarjeta-reserva {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 500px;
}

.sala-seleccionada {
  background: #e8f5e9;
  padding: 10px;
  border-radius: 6px;
  color: #2e7d32;
  margin-bottom: 1.5rem;
}

.campo-grupo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.campo {
  margin-bottom: 1.2rem;
  label { display: block; margin-bottom: 0.5rem; font-weight: bold; text-align: left; }
  input { width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 8px; }
}

.boton-reserva {
  width: 100%;
  padding: 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  &:hover { background-color: #2980b9; }
  &:disabled { background-color: #bdc3c7; }
}

.mensaje {
  margin-top: 1rem;
  padding: 10px;
  border-radius: 6px;
  &.exito { background: #d4edda; color: #155724; }
  &.error { background: #f8d7da; color: #721c24; }
}
</style>