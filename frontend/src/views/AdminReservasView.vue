<template>
  <div class="admin-container">
    <header class="dashboard-header">
      <h1>Panel de control</h1>
      
      <div class="admin-filters">
        <label for="mes-filtro">📊 Periodo:</label>
        <select id="mes-filtro" v-model="mesSeleccionado">
          <option value="todos">Histórico Completo</option>
          <option value="0">Enero</option>
          <option value="1">Febrero</option>
          <option value="2">Marzo</option>
          <option value="3">Abril</option>
          <option value="4">Mayo</option>
          <option value="5">Junio</option>
          <option value="6">Julio</option>
          <option value="7">Agosto</option>
          <option value="8">Septiembre</option>
          <option value="9">Octubre</option>
          <option value="10">Noviembre</option>
          <option value="11">Diciembre</option>
        </select>
      </div>
    </header>
    
    <div class="stats-grid">
      
      <div class="stat-card">
        <div class="stat-head">
          <span class="label">Total Reservas (Periodo)</span>
          <div class="badge-container">
            <span :class="['chip', variacionMes >= 0 ? 'positive' : 'negative']">{{ variacionMes >= 0 ? '+' : '' }}{{ variacionMes }}</span>
            <span class="chip status-live">Hoy: {{ reservasHoy }}</span>
          </div>
        </div>
        <span class="value">{{ reservasFiltradasPorMes.length }}</span>
        <span class="sub">Histórico cargado en panel</span>
        
        <div class="mock-bars">
          <div
            v-for="(count, mes) in reservasPorMes"
            :key="mes"
            class="bar-col"
            :title="nombreMes(mes) + ': ' + count + ' reservas'"
          >
            <span :style="{ height: alturaBarra(count) }"></span>
            <small>{{ nombreMes(mes) }}</small>
          </div>
        </div>
        
        <div class="card-footer-metrics">
          <div><strong>{{ reservasFiltradasPorMes.filter(r => r.status === 'confirmed').length }}</strong> <span>Confirmadas</span></div>
          <div><strong>{{ reservasFiltradasPorMes.filter(r => r.status === 'cancelled').length }}</strong> <span>Canceladas</span></div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-head">
          <span class="label">Volumen de Ingresos</span>
          <div class="badge-container">
            <span :class="['chip', variacionIngresosPorc >= 0 ? 'positive' : 'negative']">{{ variacionIngresosPorc >= 0 ? '+' : '' }}{{ variacionIngresosPorc }}%</span>
            <span class="chip status-top" :title="salaMasRentable">{{ salaMasRentable.split(' ')[0] }}</span>
          </div>
        </div>
        <span class="value">{{ ingresosTotales }}€ <span class="currency">EUR</span></span>
        <span class="sub">Reservas confirmadas acumuladas</span>
        
        <div class="sala-bars">
          <div v-for="(total, sala) in prepararDatosGrafico()" :key="sala" class="sala-bar-row">
            <span class="sala-bar-name">{{ sala }}</span>
            <div class="sala-bar-track">
              <div class="sala-bar-fill" :style="{ width: anchoBarra(total) }"></div>
            </div>
            <span class="sala-bar-val">{{ Number(total).toFixed(0) }}€</span>
          </div>
        </div>

        <div class="card-footer-info">
          <span class="footer-title">Sala más rentable:</span>
          <span class="footer-highlight">{{ salaMasRentable }}</span>
        </div>
      </div>

    </div>

    <div v-if="cargando" class="estado-cargando">Cargando historial global...</div>

    <div v-else class="tabla-wrap">
      <div class="tabla-header">
        <h3>Registro de Operaciones Activas</h3>
      </div>
      <table class="tabla-admin">
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
            <td class="reserva-id">#{{ reserva.id }}</td>
            <td><strong>{{ reserva.user_name }}</strong></td>
            <td>{{ reserva.room_name }}</td>
            <td class="date-cell">{{ reserva.start_time }}</td>
            <td class="price-cell">{{ reserva.total_price }}€</td>
            <td>
              <span :class="['badge-status', reserva.status]">
                {{ reserva.status === 'confirmed' ? 'Confirmada' : 'Cancelada' }}
              </span>
            </td>
            <td>
              <button v-if="reserva.status !== 'cancelled'" 
                      @click="cancelarComoAdmin(reserva.id)" 
                      class="btn-delete">
                Anular
              </button>
              <span v-else class="text-muted">-</span>
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
        const fecha = new Date(r.start_time);
        return fecha.getMonth().toString() === this.mesSeleccionado;
      });
    },
    ingresosTotales() {
      return this.reservasFiltradasPorMes
        .filter(r => r.status === 'confirmed')
        .reduce((acc, r) => acc + Number(r.total_price || 0), 0).toFixed(2);
    },
    salaMasRentable() {
      if (this.reservasFiltradasPorMes.length === 0) return "N/A";
      const ingresosPorSala = {};
      this.reservasFiltradasPorMes.forEach(r => {
        if (r.status === 'confirmed') {
          ingresosPorSala[r.room_name] = (ingresosPorSala[r.room_name] || 0) + Number(r.total_price || 0);
        }
      });
      if (Object.keys(ingresosPorSala).length === 0) return "Ninguna";
      return Object.keys(ingresosPorSala).reduce((a, b) => 
        ingresosPorSala[a] > ingresosPorSala[b] ? a : b);
    },
    reservasHoy() {
      const ahora = new Date();
      const hoy = `${ahora.getFullYear()}-${String(ahora.getMonth()+1).padStart(2,'0')}-${String(ahora.getDate()).padStart(2,'0')}`;
      return this.reservas.filter(r => r.start_time.startsWith(hoy)).length;
    },
    variacionMes() {
      const ahora = new Date();
      const mesActual = ahora.getMonth();
      const mesAnterior = mesActual === 0 ? 11 : mesActual - 1;
      const anioActual = ahora.getFullYear();
      const anioAnterior = mesActual === 0 ? anioActual - 1 : anioActual;
      const contar = (mes, anio) => this.reservas.filter(r => {
        const f = new Date(r.start_time);
        return f.getMonth() === mes && f.getFullYear() === anio;
      }).length;
      return contar(mesActual, anioActual) - contar(mesAnterior, anioAnterior);
    },
    reservasPorMes() {
      const fuente = this.mesSeleccionado === 'todos' ? this.reservas : this.reservasFiltradasPorMes;
      const conteo = { 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0 };
      fuente.forEach(r => {
        const m = new Date(r.start_time).getMonth();
        if (!isNaN(m)) conteo[m]++;
      });
      return conteo;
    },
    ingresosPorMes() {
      const base = { 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0 };
      this.reservas.forEach(r => {
        if (r.status === 'confirmed') {
          const m = new Date(r.start_time).getMonth();
          if (!isNaN(m)) base[m] += Number(r.total_price || 0);
        }
      });
      return base;
    },
    variacionIngresosPorc() {
      const ahora = new Date();
      const mc = ahora.getMonth();
      const ma = mc === 0 ? 11 : mc - 1;
      const actual = this.ingresosPorMes[mc];
      const anterior = this.ingresosPorMes[ma];
      if (!anterior) return actual > 0 ? 100 : 0;
      return Math.round(((actual - anterior) / anterior) * 100);
    },
    svgIngresosPorc() {
      const vals = Object.values(this.ingresosPorMes);
      const maxVal = Math.max(...vals, 1);
      const step = 110 / 11;
      return vals.map((v, i) => {
        const x = i * step;
        const y = 28 - (v / maxVal) * 24;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      }).join(' ');
    }
  },
  async created() {
    try {
      const token = localStorage.getItem('user-token');
      const response = await axios.get('http://localhost:8000/api/bookings/admin/all', {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.reservas = response.data;
    } catch (error) {
      localStorage.setItem('ui-notice', JSON.stringify({
        tipo: 'warning',
        titulo: 'Acceso denegado',
        mensaje: 'No tienes permisos de administrador para ver esta pantalla.'
      }));
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
          resumen[r.room_name] = (resumen[r.room_name] || 0) + Number(r.total_price || 0);
        }
      });
      return resumen;
    },
    anchoBarra(total) {
      const base = Number(this.ingresosTotales);
      if (!base || base <= 0) return '0%';
      return `${(Number(total || 0) / base) * 100}%`;
    },
    alturaBarra(count) {
      const counts = Object.values(this.reservasPorMes);
      const maxCount = counts.length ? Math.max(...counts) : 1;
      if (maxCount <= 0) return '0%';
      return `${Math.round((count / maxCount) * 100)}%`;
    },
    nombreMes(index) {
      const nombres = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
      return nombres[Number(index)] || '';
    }
  }
}
</script>

<style scoped>
/* --- CONTENEDOR PRINCIPAL ESTILO JAPANDI --- */
.admin-container {
  color: #ffffff; /* Texto café oscuro */
  min-height: 100vh;
  padding: 2rem 4rem 4rem 4rem;
  font-family: 'Inter', sans-serif;
}

/* --- ENCABEZADO EDITORIAL --- */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4rem;
}
h1 {
  font-family: 'Playfair Display', serif;
  font-size: 3.8rem;
  font-weight: 400;
  letter-spacing: -0.02em;
}

/* --- FILTROS DE PERIODO --- */
.admin-filters {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
}
.admin-filters label {
  font-size: 1.4rem;
  font-weight: 500;
  color: #ffffff;
}
.admin-filters select {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  border: 1px solid #eaddd3;
  background: #ffffff;
  color: #2b1b17;
  outline: none;
  font-size: 1.2rem;
}

/* --- CUADRÍCULA DE TARJETAS LIMPIAS --- */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 2.5rem;
}
.stat-card {
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 8px !important;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(43, 27, 23, 0.02);
  display: flex;
  flex-direction: column;
  position: relative;
}
.stat-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.stat-card .label {
  font-size: 0.95rem;
  color: #2b1b17;
  font-weight: 600;
}
.badge-container {
  display: flex;
  gap: 0.5rem;
}
.chip {
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  border-radius: 8px;
  font-weight: 600;
}
.chip.positive { background: #e1f7e7; color: #27ae60; }
.chip.negative { background: #fdecea; color: #e74c3c; }
.chip.status-live { background: #e8edf8; color: #1b4fd6; }
.chip.status-top { background: #fff3e9; color: #e67e22; }

.stat-card .value {
  font-size: 3rem;
  font-weight: 700;
  color: #2b1b17;
  letter-spacing: -0.03em;
  line-height: 1;
}
.currency {
  font-size: 1.2rem;
  color: #6e5e58;
  font-weight: 400;
}
.stat-card .sub {
  margin-top: 0.5rem;
  color: #8c7e7a;
  font-size: 0.9rem;
}

/* Gráficos simulados idénticos a la foto */
.mock-bars {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 100px;
  margin: 1.5rem 0 0.25rem;
  border-bottom: 1px solid #f0e6df;
}
.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
}
.bar-col span {
  width: 100%;
  background: #1b4fd6;
  border-radius: 4px 4px 0 0;
  opacity: 0.85;
  min-height: 2px;
}
.bar-col small {
  display: block;
  font-size: 0.55rem;
  color: #a0887e;
  margin-top: 4px;
  text-align: center;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}
.sala-bars {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  margin: 1.25rem 0;
}
.sala-bar-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.72rem;
}
.sala-bar-name {
  width: 80px;
  flex-shrink: 0;
  color: #6b4f47;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sala-bar-track {
  flex: 1;
  background: #f0e6df;
  border-radius: 99px;
  height: 6px;
  overflow: hidden;
}
.sala-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #1b4fd6, #5b8dee);
  border-radius: 99px;
  transition: width 0.4s ease;
}
.sala-bar-val {
  width: 40px;
  text-align: right;
  flex-shrink: 0;
  color: #2b1b17;
  font-weight: 600;
}

.card-footer-metrics {
  display: flex;
  border-top: 1px solid #f0e6df;
  padding-top: 1rem;
  gap: 2rem;
}
.card-footer-metrics div { font-size: 0.9rem; }
.card-footer-metrics strong { font-size: 1.2rem; color: #2b1b17; }
.card-footer-metrics span { color: #8c7e7a; margin-left: 0.3rem; }

.card-footer-info {
  border-top: 1px solid #f0e6df;
  padding-top: 1rem;
}
.footer-title { color: #8c7e7a; font-size: 0.9rem; }
.footer-highlight { display: block; font-size: 1.3rem; font-weight: 700; color: #2b1b17; margin-top: 0.2rem; }

/* --- TABLA DE REGISTROS --- */
.tabla-wrap {
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(43, 27, 23, 0.01);
}

.tabla-wrap,
.tabla-wrap * {
  text-shadow: none !important;
}

.tabla-wrap,
.tabla-wrap th,
.tabla-wrap td,
.tabla-wrap h3,
.tabla-wrap strong,
.tabla-wrap .text-muted {
  color: #2b1b17;
}

.tabla-header { padding: 1.5rem 2rem; border-bottom: 1px solid #eaddd3; }
.tabla-header h3 { font-size: 1.1rem; font-weight: 600; }
.tabla-admin { width: 100%; border-collapse: collapse; }
.tabla-admin th, .tabla-admin td { padding: 1.2rem 2rem; text-align: left; }
.tabla-admin th {
  background: #fcfaf7;
  color: #6e5e58;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  border-bottom: 1px solid #eaddd3;
}
.tabla-admin td { border-bottom: 1px solid #f0e6df; font-size: 0.95rem; }
.reserva-id { color: #8c7e7a; font-weight: 500; }
.date-cell { color: #6e5e58; }
.price-cell { font-weight: 600; color: #2b1b17; }

/* Estados de los Badges */
.badge-status {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}
.badge-status.confirmed { background: #e1f7e7; color: #27ae60; }
.badge-status.cancelled { background: #fdf2f2; color: #e74c3c; }

/* Botón de acción minimalista */
.btn-delete {
  background: transparent;
  color: #e74c3c;
  border: 1px solid #f9d5d5;
  padding: 0.4rem 0.8rem;
  cursor: pointer;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s;
}
.btn-delete:hover { background: #e74c3c; color: white; border-color: #e74c3c; }
.text-muted { color: #bfa38f; font-style: italic; }
.estado-cargando { text-align: center; padding: 3rem; color: #6e5e58; }

@media (max-width: 960px) {
  .admin-container {
    padding: 1.25rem 1.2rem 2rem 1.2rem;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .tabla-admin th,
  .tabla-admin td {
    padding: 0.9rem 1rem;
  }
}
</style>