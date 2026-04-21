<template>
  <div class="mis-reservas-container">
    <h1>Mis Reservas</h1>
    <p class="descripcion">Aquí puedes consultar y gestionar tus próximos espacios.</p>

    <div v-if="cargando" class="estado">Cargando tus datos...</div>

    <div v-else-if="reservas.length === 0" class="estado-vacio">
      <p>No tienes reservas registradas.</p>
      <router-link to="/" class="btn-enlace">Explorar salas ahora</router-link>
    </div>

    <div v-else class="tabla-contenedor">
      <table class="tabla-reservas">
        <thead>
          <tr>
            <th>Sala</th>
            <th>Inicio</th>
            <th>Fin</th>
            <th>Precio Total</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="reserva in reservas" :key="reserva.id">
            <td class="nombre-sala">{{ reserva.room_name }}</td>
            <td>{{ reserva.start_time }}</td>
            <td>{{ reserva.end_time }}</td>
            <td>{{ reserva.total_price }}€</td>
            <td>
              <span :class="['badge', reserva.status]">
                {{ reserva.status === 'confirmed' ? 'Confirmada' : 'Cancelada' }}
              </span>
            </td>
            <td>
              <button 
                v-if="reserva.status === 'confirmed'" 
                @click="cancelarReserva(reserva.id)"
                class="btn-cancelar"
              >
                Cancelar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserReservasView',
  data() {
    return {
      reservas: [],
      cargando: true
    };
  },
  async created() {
    this.obtenerReservas();
  },
  methods: {
    async obtenerReservas() {
      try {
        const token = localStorage.getItem('user-token');
        const response = await axios.get('http://localhost:8000/api/bookings/my-bookings', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.reservas = response.data;
      } catch (error) {
        console.error("Error al cargar reservas:", error);
      } finally {
        this.cargando = false;
      }
    },
    async cancelarReserva(id) {
      if (!confirm("¿Estás seguro de que deseas cancelar esta reserva?")) return;

      try {
        const token = localStorage.getItem('user-token');
        // Usamos PATCH y la URL /cancel que tienes en tu bookings.py
        await axios.patch(`http://localhost:8000/api/bookings/${id}/cancel`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });

        // Actualizamos la lista localmente para reflejar el cambio
        const reserva = this.reservas.find(r => r.id === id);
        if (reserva) reserva.status = 'cancelled';
        
        alert("Reserva cancelada con éxito");
      } catch (error) {
        alert(error.response?.data?.message || "No se pudo cancelar la reserva");
      }
    }
  }
};
</script>

<style scoped>
.mis-reservas-container { padding: 2rem; max-width: 1000px; margin: 0 auto; }
.descripcion { color: #666; margin-bottom: 2rem; }
.tabla-contenedor { background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }
.tabla-reservas { width: 100%; border-collapse: collapse; }
.tabla-reservas th, .tabla-reservas td { padding: 1rem; text-align: left; border-bottom: 1px solid #eee; }
.tabla-reservas th { background-color: #f8f9fa; font-weight: bold; }
.nombre-sala { font-weight: bold; color: #2c3e50; }

.badge { padding: 4px 8px; border-radius: 4px; font-size: 0.85rem; font-weight: bold; }
.badge.confirmed { background-color: #d4edda; color: #155724; }
.badge.cancelled { background-color: #f8d7da; color: #721c24; }

.btn-cancelar { background: none; border: 1px solid #dc3545; color: #dc3545; padding: 5px 10px; border-radius: 4px; cursor: pointer; transition: 0.3s; }
.btn-cancelar:hover { background: #dc3545; color: white; }
.btn-enlace { display: inline-block; margin-top: 1rem; color: #42b983; text-decoration: none; font-weight: bold; }
</style>