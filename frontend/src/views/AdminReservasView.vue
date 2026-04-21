<template>
  <div class="admin-container">
    <h1>Panel de Control: Todas las Reservas</h1>
    
    <div class="stats-cards">
      <div class="card">Total Reservas: {{ reservas.length }}</div>
      <div class="card">Ingresos Totales: {{ ingresosTotales }}€</div>
    </div>

    <div v-if="cargando">Cargando historial global...</div>

    <table v-else class="tabla-admin">
      <thead>
        <tr>
          <th>ID</th>
          <th>Usuario</th>
          <th>Sala</th>
          <th>Fecha / Hora</th>
          <th>Total</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reserva in reservas" :key="reserva.id">
          <td>#{{ reserva.id }}</td>
          <td><strong>{{ reserva.user_name }}</strong></td>
          <td>{{ reserva.room_name }}</td>
          <td>{{ reserva.start_time }}</td>
          <td>{{ reserva.total_price }}€</td>
          <td>
            <span :class="['badge', reserva.status]">{{ reserva.status }}</span>
          </td>
          <td>
            <button v-if="reserva.status !== 'cancelled'" 
                    @click="cancelarComoAdmin(reserva.id)" 
                    class="btn-delete">
              Anular
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      reservas: [],
      cargando: true
    }
  },
  computed: {
    ingresosTotales() {
      return this.reservas
        .filter(r => r.status === 'confirmed')
        .reduce((acc, r) => acc + r.total_price, 0).toFixed(2);
    }
  },
  async created() {
    try {
      const token = localStorage.getItem('user-token');
      // Llamada a tu ruta @bookings_bp.route('/admin/all')
      const response = await axios.get('http://localhost:8000/api/bookings/admin/all', {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.reservas = response.data;
    } catch (error) {
      alert("Error: No tienes permisos de administrador.");
      this.$router.push('/');
    } finally {
      this.cargando = false;
    }
  },
  methods: {
    async cancelarComoAdmin(id) {
      if (!confirm("¿Anular esta reserva como administrador?")) return;
      try {
        const token = localStorage.getItem('user-token');
        await axios.patch(`http://localhost:8000/api/bookings/${id}/cancel`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        const r = this.reservas.find(res => res.id === id);
        if (r) r.status = 'cancelled';
      } catch (e) {
        alert("Error al anular");
      }
    }
  }
}
</script>

<style scoped>
.admin-container { padding: 2rem; }
.stats-cards { display: flex; gap: 1rem; margin-bottom: 2rem; }
.card { background: #34495e; color: white; padding: 1.5rem; border-radius: 8px; flex: 1; text-align: center; font-size: 1.2rem; }
.tabla-admin { width: 100%; border-collapse: collapse; background: white; }
.tabla-admin th, .tabla-admin td { padding: 12px; border: 1px solid #ddd; text-align: left; }
.tabla-admin th { background: #f4f4f4; }
.badge.confirmed { color: green; font-weight: bold; }
.badge.cancelled { color: red; }
.btn-delete { background: #e74c3c; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; }
</style>