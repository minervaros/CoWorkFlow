<template>
  <div class="admin-tours-container">
    <div class="home-velo"></div>
    <header class="header">
      <h1>Reservas de tours</h1>
      <p>Consulta todas las solicitudes de tour registradas.</p>
    </header>

    <div class="filtros">
      <label for="estado-tour">Estado</label>
      <select id="estado-tour" v-model="filtroEstado">
        <option value="todos">Todos</option>
        <option value="requested">Solicitado</option>
        <option value="cancelled">Cancelado</option>
      </select>
    </div>

    <div v-if="cargando" class="estado">Cargando tours...</div>

    <div v-else-if="toursFiltrados.length === 0" class="estado">
      No hay reservas de tours para el filtro seleccionado.
    </div>

    <div v-else class="tabla-wrap">
      <table class="tabla-tours">
        <thead>
          <tr>
            <th>ID</th>
            <th>Sede</th>
            <th>Fecha / Hora</th>
            <th>Solicitante</th>
            <th>Contacto</th>
            <th>Personas</th>
            <th>Empresa</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tour in toursFiltrados" :key="tour.id">
            <td>#{{ tour.id }}</td>
            <td>{{ tour.sede_name }}</td>
            <td>{{ tour.start_time }}</td>
            <td>
              <strong>{{ tour.full_name }}</strong>
              <div class="sub">Usuario: {{ tour.user_name || 'N/A' }}</div>
            </td>
            <td>
              <div>{{ tour.email }}</div>
              <div class="sub">{{ tour.phone }}</div>
            </td>
            <td>{{ tour.people_count }}</td>
            <td>{{ tour.company_name }}</td>
            <td>
              <span :class="['badge', tour.status]">
                {{ tour.status === 'cancelled' ? 'Cancelado' : 'Solicitado' }}
              </span>
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
  name: 'AdminToursView',
  data() {
    return {
      tours: [],
      cargando: true,
      filtroEstado: 'todos'
    };
  },
  computed: {
    toursFiltrados() {
      if (this.filtroEstado === 'todos') return this.tours;
      return this.tours.filter(t => t.status === this.filtroEstado);
    }
  },
  async created() {
    try {
      const token = localStorage.getItem('user-token');
      const response = await axios.get('http://localhost:8000/api/bookings/admin/tours', {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.tours = response.data || [];
    } catch (error) {
      localStorage.setItem('ui-notice', JSON.stringify({
        tipo: 'warning',
        titulo: 'Acceso denegado',
        mensaje: 'No tienes permisos de administrador para ver tours.'
      }));
      this.$router.push('/');
    } finally {
      this.cargando = false;
    }
  }
};
</script>

<style scoped>
.admin-tours-container {
  min-height: 100vh;
  padding: 2rem 3rem 3rem;
  color: #fff;
  position: relative;
  z-index: 2;
}

.admin-tours-container > *:not(.home-velo) {
  position: relative;
  z-index: 2;
}

.header h1 {
  margin: 0;
  font-size: 2.2rem;
}

.header p {
  margin: 0.4rem 0 1.2rem;
  color: #efe6df;
}

.filtros {
  display: flex;
  gap: 0.6rem;
  align-items: center;
  margin-bottom: 1rem;
}

.filtros select {
  border: 1px solid #e5d8cc;
  border-radius: 10px;
  padding: 0.45rem 0.7rem;
  background: #fff;
}

.estado {
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  padding: 1rem;
}

.tabla-wrap {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.2);
}

.tabla-tours {
  width: 100%;
  border-collapse: collapse;
  color: #2f221d;
  text-shadow: none;
}

.tabla-tours th,
.tabla-tours td {
  padding: 0.75rem;
  border-bottom: 1px solid #f0e6de;
  text-align: left;
  font-size: 0.9rem;
  vertical-align: top;
}

.tabla-tours th {
  background: #f8f3ee;
  font-weight: 700;
}

.sub {
  color: #7c685f;
  font-size: 0.78rem;
  margin-top: 0.15rem;
}

.badge {
  display: inline-block;
  border-radius: 999px;
  padding: 0.2rem 0.55rem;
  font-size: 0.75rem;
  font-weight: 700;
}

.badge.requested {
  background: #fff3e8;
  color: #a75915;
}

.badge.cancelled {
  background: #fdecec;
  color: #a73745;
}

@media (max-width: 980px) {
  .admin-tours-container {
    padding: 1.2rem;
  }

  .tabla-wrap {
    overflow-x: auto;
  }

  .tabla-tours {
    min-width: 960px;
  }
}

.home-velo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.25);
  z-index: 1;
  pointer-events: none;
}
</style>
