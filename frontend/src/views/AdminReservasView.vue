<template>
  <div class="admin-container">
    <h1>Panel de Control: Todas las Reservas</h1>
    
    <div class="admin-filters">
      <label for="mes-filtro">📊 Análisis del periodo:</label>
      <select id="mes-filtro" v-model="mesSeleccionado">
        <option value="todos">Histórico Completo</option>
        <option value="0">Enero</option>
        <option value="1">Febrero</option>
        <option value="2">Marzo</option>
        <option value="3">Abril</option>
        <option value="4">Mayo</option>
        <option value="5">Junio</option>
      </select>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <span class="label">Ingresos Totales</span>
        <span class="value">{{ ingresosTotales }}€</span>
      </div>
      <div class="stat-card">
        <span class="label">Reservas para hoy</span>
        <span class="value">{{ reservasHoy }}</span>
      </div>
      <div class="stat-card">
        <span class="label">Sala más rentable</span>
        <span class="value sala">{{ salaMasRentable }}</span>
      </div>
      <div class="stat-card">
        <span class="label">Total Reservas</span>
        <span class="value">{{ reservas.length }}</span>
      </div>
    </div>

    <div class="dashboard-visual">
      <div class="chart-container">
        <h3>Distribución de Ingresos por Sala</h3>
        <div class="placeholder-grafico">
          <div v-for="(total, sala) in prepararDatosGrafico()" :key="sala" class="bar-row">
            <span class="bar-label">{{ sala }}</span>
            <div class="bar-wrapper">
              <div class="bar-fill" :style="{ width: (total / ingresosTotales * 100) + '%' }"></div>
            </div>
            <span class="bar-value">{{ total.toFixed(2) }}€</span>
          </div>
        </div>
      </div>
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
        <tr v-for="reserva in reservasFiltradasPorMes" :key="reserva.id">
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
      mesSeleccionado: 'todos',
      cargando: true
    }
  },
  computed: {
    reservasFiltradasPorMes() {
    if (this.mesSeleccionado === 'todos') return this.reservas;
    
    return this.reservas.filter(r => {
      // Evitamos fallos si start_time no es un objeto fecha válido
      const fecha = new Date(r.start_time);
      return fecha.getMonth().toString() === this.mesSeleccionado;
    });
  },
  ingresosTotales() {
    return this.reservasFiltradasPorMes
      .filter(r => r.status === 'confirmed')
      .reduce((acc, r) => acc + r.total_price, 0).toFixed(2);
  },
  salaMasRentable() {
    // Cambiado this.reservas por this.reservasFiltradasPorMes
    if (this.reservasFiltradasPorMes.length === 0) return "N/A";
    
    const ingresosPorSala = {};
    this.reservasFiltradasPorMes.forEach(r => {
      if (r.status === 'confirmed') {
        ingresosPorSala[r.room_name] = (ingresosPorSala[r.room_name] || 0) + r.total_price;
      }
    });

    if (Object.keys(ingresosPorSala).length === 0) return "Ninguna";

    return Object.keys(ingresosPorSala).reduce((a, b) => 
      ingresosPorSala[a] > ingresosPorSala[b] ? a : b);
  },
  reservasHoy() {
    const hoy = new Date().toISOString().split('T')[0];
    // Cambiado this.reservas por this.reservasFiltradasPorMes
    return this.reservasFiltradasPorMes.filter(r => r.start_time.startsWith(hoy)).length;
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
    },
    prepararDatosGrafico() {
      const resumen = {};
      this.reservasFiltradasPorMes.forEach(r => {
        if (r.status === 'confirmed') {
          resumen[r.room_name] = (resumen[r.room_name] || 0) + r.total_price;
        }
      });
      return resumen;
    }
  }
}
</script>

<style scoped>
.admin-container { padding: 2rem; }
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  border: 1px solid #eee;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-card .label {
  font-size: 0.85rem;
  color: #7f8c8d;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.stat-card .value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2c3e50;
}

.stat-card .value.sala {
  font-size: 1.2rem;
  color: #3498db;
}
.card { background: #34495e; color: white; padding: 1.5rem; border-radius: 8px; flex: 1; text-align: center; font-size: 1.2rem; }
.tabla-admin { width: 100%; border-collapse: collapse; background: white; }
.tabla-admin th, .tabla-admin td { padding: 12px; border: 1px solid #ddd; text-align: left; }
.tabla-admin th { background: #f4f4f4; }
.badge.confirmed { color: green; font-weight: bold; }
.badge.cancelled { color: red; }
.btn-delete { background: #e74c3c; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; }

.dashboard-visual {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.placeholder-grafico {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bar-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.bar-label { width: 150px; font-size: 0.9rem; color: #34495e; }

.bar-wrapper {
  flex-grow: 1;
  background: #f0f2f5;
  height: 12px;
  border-radius: 6px;
  overflow: hidden;
}

.bar-fill {
  background: #3498db;
  height: 100%;
  transition: width 0.5s ease-out;
}

.bar-value { width: 80px; text-align: right; font-weight: bold; font-size: 0.9rem; }

.admin-filters {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-left: 4px solid #3498db;
}

.admin-filters select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

</style>