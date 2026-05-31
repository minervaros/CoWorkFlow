<template>
  <div class="admin-salas">
    <div class="home-velo"></div>
    <div class="header-panel">
      <div>
        <h1>Control de Salas</h1>
        <p>Gestiona disponibilidad, precios e información de cada espacio.</p>
      </div>
      <button @click="abrirModalCrear" class="btn-nuevo">+ Nueva Sala</button>
    </div>

    <div class="kpi-grid">
      <article class="kpi-card">
        <span>Total</span>
        <strong>{{ totalSalas }}</strong>
      </article>
      <article class="kpi-card">
        <span>Activas</span>
        <strong>{{ totalActivas }}</strong>
      </article>
      <article class="kpi-card">
        <span>Inactivas</span>
        <strong>{{ totalInactivas }}</strong>
      </article>
      <article class="kpi-card">
        <span>Precio promedio</span>
        <strong>{{ precioPromedio }}€/h</strong>
      </article>
    </div>

    <div v-if="mostrarModal" class="modal-overlay">
      <div class="modal">
        <h2>{{ editando ? 'Editar Sala' : 'Nueva Sala' }}</h2>
        <form @submit.prevent="guardarSala" class="form-sala-layout">
          <div class="form-col-main">
            <div class="grupo-form">
              <label>Nombre de la sala</label>
              <input v-model.trim="form.name" placeholder="Ej: Sala Ágora" required />
            </div>

            <div class="grupo-form">
              <label>Sede</label>
              <select v-model="form.location" required>
                <option disabled value="">Selecciona una sede</option>
                <option v-for="sede in sedesDisponibles" :key="sede" :value="sede">{{ sede }}</option>
              </select>
              <small class="helper-text">Esta sede se usa en catálogo, detalle y reservas.</small>
            </div>

            <div class="grupo-form grupo-cols">
              <div>
                <label>Capacidad</label>
                <input v-model.number="form.capacity" type="number" min="1" step="1" placeholder="Ej: 8" required />
              </div>
              <div>
                <label>Precio por hora (€)</label>
                <input v-model.number="form.price_per_hour" type="number" min="1" step="0.01" placeholder="Ej: 24" required />
              </div>
            </div>

            <div class="grupo-form">
              <label>Descripción</label>
              <textarea v-model.trim="form.description" placeholder="Describe la sala, usos recomendados y ambiente"></textarea>
            </div>

            <div class="grupo-form">
              <label>URL de imagen</label>
              <input v-model.trim="form.image_url" type="url" placeholder="https://..." />
            </div>

            <div class="grupo-form estado-switch">
              <label>
                <input v-model="form.is_active" type="checkbox" />
                Sala activa y visible para reservas
              </label>
            </div>
          </div>

          <div class="form-col-side">
            <div class="grupo-form grupo-equipacion">
              <label>🧰 Equipación</label>
              <div class="equipamiento-grid">
                <label v-for="opcion in opcionesEquipamientoDisponibles" :key="opcion" class="equipamiento-opcion">
                  <input v-model="form.equipamiento" type="checkbox" :value="opcion" />
                  <span>{{ opcion }}</span>
                </label>
              </div>
            </div>
          </div>

          <p v-if="errorFormulario" class="form-error">{{ errorFormulario }}</p>

          <div class="modal-btns">
            <button type="button" @click="mostrarModal = false">Cancelar</button>
            <button type="submit" class="btn-save">Guardar Cambios</button>
          </div>
        </form>
      </div>
    </div>

    <div class="filtros">
      <button
        class="filtro-btn"
        :class="{ activo: filtroEstado === 'todas' }"
        @click="filtroEstado = 'todas'"
      >
        Todas
      </button>
      <button
        class="filtro-btn"
        :class="{ activo: filtroEstado === 'activas' }"
        @click="filtroEstado = 'activas'"
      >
        Activas
      </button>
      <button
        class="filtro-btn"
        :class="{ activo: filtroEstado === 'inactivas' }"
        @click="filtroEstado = 'inactivas'"
      >
        Inactivas
      </button>
      <button
        class="filtro-btn"
        :class="{ activo: filtroEstado === 'eliminadas' }"
        @click="filtroEstado = 'eliminadas'"
      >
        Eliminadas
      </button>
    </div>

    <div v-if="mensajeAccion" :class="['admin-notice', esErrorAccion ? 'error' : 'success']">
      {{ mensajeAccion }}
    </div>

    <div v-if="salasFiltradas.length" class="salas-grid">
      <article v-for="sala in salasFiltradas" :key="sala.id" class="sala-card">
        <img
          :src="sala.image_url || defaultRoomImage"
          :alt="`Imagen de ${sala.name}`"
          class="sala-img"
          @error="handleRoomImageError"
        />

        <div class="sala-body">
          <div class="sala-top">
            <h3>{{ sala.name }}</h3>
            <span 
              v-if="sala.is_deleted" 
              class="status-pill eliminada"
              title="Esta sala ha sido eliminada"
            >
              🗑️ Eliminada
            </span>
            <span v-else :class="['status-pill', sala.is_active ? 'activo' : 'inactivo']">
              {{ sala.is_active ? 'Activa' : 'Fuera de servicio' }}
            </span>
          </div>

          <p class="sala-desc">{{ sala.description || 'Sin descripción todavía.' }}</p>
          <p class="sala-ubicacion">📍 {{ sala.location || 'Ubicación no definida' }}</p>

          <div v-if="(sala.equipamiento || []).length" class="sala-equipamiento">
            <span v-for="item in sala.equipamiento" :key="`${sala.id}-${item}`" class="equipamiento-pill">{{ item }}</span>
          </div>

          <div class="sala-meta">
            <span>👥 {{ sala.capacity }} personas</span>
            <span>💶 {{ sala.price_per_hour }}€/h</span>
          </div>

          <div class="acciones">
            <button @click="abrirModalEditar(sala)" class="btn-edit">Editar</button>
            <button @click="alternarEstado(sala)" class="btn-toggle">
              {{ sala.is_active ? 'Desactivar' : 'Activar' }}
            </button>
            <button @click="abrirModalEliminar(sala)" class="btn-delete">Eliminar</button>
          </div>
        </div>
      </article>
    </div>

    <div v-else class="empty-state">
      No hay salas para este filtro.
    </div>

    <div v-if="mostrarModalEliminar" class="modal-overlay" @click.self="cerrarModalEliminar">
      <div class="modal modal-confirm-delete">
        <h2>Eliminar sala</h2>
        <p class="delete-copy">
          Vas a eliminar <strong>{{ salaAEliminar?.name || 'esta sala' }}</strong>.
          Si tiene reservas asociadas, el sistema bloqueará el borrado y deberás desactivarla.
        </p>
        <div class="modal-btns solo-confirmacion">
          <button type="button" @click="cerrarModalEliminar" :disabled="eliminandoSala">Cancelar</button>
          <button type="button" class="btn-delete-confirm" @click="eliminarSala" :disabled="eliminandoSala">
            {{ eliminandoSala ? 'Eliminando...' : 'Sí, eliminar' }}
          </button>
        </div>
      </div>
    </div>

    
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      salas: [],
      mostrarModal: false,
      mostrarModalEliminar: false,
      editando: false,
      eliminandoSala: false,
      salaAEliminar: null,
      filtroEstado: 'todas',
      errorFormulario: '',
      mensajeAccion: '',
      esErrorAccion: false,
      avisoTimer: null,
      defaultRoomImage: 'https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200&auto=format&fit=crop',
      sedesDisponibles: ['Sede Ruzafa', 'Sede El Carmen', 'Sede Eixample', 'Sede Cabanyal'],
      equipamientoBase: [
        'Wifi premium',
        'Aire acondicionado',
        'Calefacción',
        'Pantalla 4K',
        'Pantalla táctil',
        'Monitor 32"',
        'Monitor ultrapanorámico',
        'Proyector',
        'Apple TV',
        'Pizarra',
        'Mesa modular',
        'Videoconferencia',
        'Videollamada',
        'Equipo de sonido',
        'Sonido envolvente',
        'Cabina acústica cercana',
        'Iluminación regulable',
        'Luz natural',
        'Café incluido'
      ],
      form: { id: null, name: '', location: '', equipamiento: [], capacity: null, price_per_hour: null, description: '', image_url: '', is_active: true }
    };
  },
  async created() {
    this.cargarSalas();
  },
  computed: {
    salasFiltradas() {
      if (this.filtroEstado === 'activas') return this.salas.filter(s => !s.is_deleted && s.is_active);
      if (this.filtroEstado === 'inactivas') return this.salas.filter(s => !s.is_deleted && !s.is_active);
      if (this.filtroEstado === 'eliminadas') return this.salas.filter(s => s.is_deleted);
      return this.salas.filter(s => !s.is_deleted);
    },
    totalSalas() {
      return this.salas.filter(s => !s.is_deleted).length;
    },
    totalActivas() {
      return this.salas.filter(s => !s.is_deleted && s.is_active).length;
    },
    totalInactivas() {
      return this.salas.filter(s => !s.is_deleted && !s.is_active).length;
    },
    precioPromedio() {
      const salasActivas = this.salas.filter(s => !s.is_deleted);
      if (!salasActivas.length) return '0.00';
      const total = salasActivas.reduce((acc, s) => acc + Number(s.price_per_hour || 0), 0);
      return (total / salasActivas.length).toFixed(2);
    },
    opcionesEquipamientoDisponibles() {
      const equipamientoExistente = this.salas.flatMap(s => Array.isArray(s.equipamiento) ? s.equipamiento : []);
      return [...new Set([...this.equipamientoBase, ...equipamientoExistente])]
        .map(item => String(item || '').trim())
        .filter(Boolean)
        .sort((a, b) => a.localeCompare(b, 'es'));
    }
  },
  methods: {
    mostrarAviso(texto, esError = false) {
      this.mensajeAccion = texto;
      this.esErrorAccion = esError;
      if (this.avisoTimer) clearTimeout(this.avisoTimer);
      this.avisoTimer = setTimeout(() => {
        this.mensajeAccion = '';
      }, 4500);
    },
    handleRoomImageError(event) {
      const img = event?.target;
      if (!img) return;
      if (img.dataset.fallbackApplied === '1') return;

      img.dataset.fallbackApplied = '1';
      img.src = this.defaultRoomImage;
    },
    async cargarSalas() {
      const token = localStorage.getItem('user-token');
      try {
        // Admin ve todas las salas, incluyendo eliminadas
        const res = await axios.get('http://localhost:8000/api/rooms/?active_only=false&include_deleted=true', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.salas = res.data;
      } catch (e) {
        console.error("Error al cargar salas en admin", e);
      }
    },
    abrirModalCrear() {
      this.editando = false;
      this.errorFormulario = '';
      this.form = { id: null, name: '', location: '', equipamiento: [], capacity: null, price_per_hour: null, description: '', image_url: '', is_active: true };
      this.mostrarModal = true;
    },
    abrirModalEditar(sala) {
      this.editando = true;
      this.errorFormulario = '';
      if (sala.location && !this.sedesDisponibles.includes(sala.location)) {
        this.sedesDisponibles = [...this.sedesDisponibles, sala.location];
      }
      this.form = {
        ...sala,
        equipamiento: Array.isArray(sala.equipamiento) ? sala.equipamiento : [],
        is_active: Boolean(sala.is_active)
      };
      this.mostrarModal = true;
    },
    async guardarSala() {
      const token = localStorage.getItem('user-token');
      this.errorFormulario = '';

      if (!this.form.name?.trim()) {
        this.errorFormulario = 'El nombre de la sala es obligatorio.';
        return;
      }
      if (!this.form.location?.trim()) {
        this.errorFormulario = 'Debes seleccionar una sede.';
        return;
      }
      if (!Number.isFinite(Number(this.form.capacity)) || Number(this.form.capacity) < 1) {
        this.errorFormulario = 'La capacidad debe ser mayor que 0.';
        return;
      }
      if (!Number.isFinite(Number(this.form.price_per_hour)) || Number(this.form.price_per_hour) <= 0) {
        this.errorFormulario = 'El precio por hora debe ser mayor que 0.';
        return;
      }

      const payload = {
        ...this.form,
        name: this.form.name.trim(),
        location: this.form.location.trim(),
        description: (this.form.description || '').trim(),
        image_url: (this.form.image_url || '').trim(),
        capacity: Number(this.form.capacity),
        price_per_hour: Number(this.form.price_per_hour),
        equipamiento: Array.isArray(this.form.equipamiento) ? this.form.equipamiento : [],
        is_active: Boolean(this.form.is_active)
      };

      try {
        if (this.editando) {
          await axios.put(`http://localhost:8000/api/rooms/${this.form.id}`, payload, {
            headers: { Authorization: `Bearer ${token}` }
          });
        } else {
          await axios.post('http://localhost:8000/api/rooms/', payload, {
            headers: { Authorization: `Bearer ${token}` }
          });
        }
        this.mostrarModal = false;
        this.cargarSalas();
      } catch (e) { alert("Error al guardar la sala"); }
    },
    async alternarEstado(sala) {
      const nuevoEstado = !sala.is_active;
      const token = localStorage.getItem('user-token');
      try {
        await axios.put(`http://localhost:8000/api/rooms/${sala.id}`, { is_active: nuevoEstado }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        sala.is_active = nuevoEstado;
        this.mostrarAviso(`Sala ${nuevoEstado ? 'activada' : 'desactivada'} correctamente.`);
      } catch (e) {
        this.mostrarAviso('Error al cambiar el estado de la sala.', true);
      }
    },
    abrirModalEliminar(sala) {
      this.salaAEliminar = sala;
      this.mostrarModalEliminar = true;
    },
    cerrarModalEliminar(forzar = false) {
      if (this.eliminandoSala && !forzar) return;
      this.mostrarModalEliminar = false;
      this.salaAEliminar = null;
    },
    async eliminarSala() {
      if (!this.salaAEliminar?.id) return;
      this.eliminandoSala = true;
      const token = localStorage.getItem('user-token');

      try {
        await axios.delete(`http://localhost:8000/api/rooms/${this.salaAEliminar.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.salas = this.salas.filter(s => s.id !== this.salaAEliminar.id);
        this.cerrarModalEliminar(true);
        this.mostrarAviso('Sala eliminada correctamente.');
      } catch (e) {
        this.mostrarAviso(e.response?.data?.message || 'No se pudo eliminar la sala.', true);
      } finally {
        this.eliminandoSala = false;
      }
    }
  },
  beforeUnmount() {
    if (this.avisoTimer) clearTimeout(this.avisoTimer);
  }
};
</script>

<style scoped>
.admin-salas {
  padding: 2rem;
  max-width: 1300px;
  margin: 0 auto;
  color: #f7f3ef;
  position: relative;
  z-index: 2;
}

.admin-salas > *:not(.home-velo) {
  position: relative;
  z-index: 2;
}

.header-panel {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.header-panel h1 {
  margin: 0;
  font-size: 2rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 600px) {
  .header-panel h1 {
    font-size: 1.15rem;
  }
  .header-panel {
    flex-direction: column;
    align-items: flex-start; 
    gap: 1.25rem;           
    margin-bottom: 2rem;     
  }

 
  .header-panel p {
    font-size: 0.95rem;
    line-height: 1.45;       
    max-width: 280px;       
    color: #eadfd7;
  }

  
  .btn-nuevo {
    width: 100%;           
    padding: 0.85rem 1.2rem; 
    text-align: center;
  }
}

.header-panel p {
  margin: 0.35rem 0 0;
  color: #eadfd7;
}

.btn-nuevo {
  background: linear-gradient(135deg, #ffc67a, #ff9f68);
  color: #3b261f;
  border: none;
  padding: 0.7rem 1.1rem;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 0.9rem;
  margin-bottom: 1rem;
}

.kpi-card {
  background: rgba(16, 12, 10, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 14px;
  padding: 0.9rem;
  backdrop-filter: blur(5px);
}

.kpi-card span {
  font-size: 0.8rem;
  color: #d8cbc3;
}

.kpi-card strong {
  display: block;
  margin-top: 0.2rem;
  font-size: 1.25rem;
}

.filtros {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  margin-bottom: 1.2rem;
}

.filtro-btn {
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.06);
  color: #fcfaf7;
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
  cursor: pointer;
}

.filtro-btn.activo {
  background: #fcfaf7;
  color: #3b261f;
  border-color: #fcfaf7;
}

.admin-notice {
  margin-bottom: 1rem;
  border-radius: 12px;
  padding: 0.8rem 1rem;
  text-shadow: none;
  font-weight: 600;
}

.admin-notice.success {
  background: #e8f6ee;
  color: #1f7a4f;
  border: 1px solid #bfe6cb;
}

.admin-notice.error {
  background: #fdecee;
  color: #a73745;
  border: 1px solid #f2c5ce;
}

.salas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 1rem;
}

.sala-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.22);
  text-shadow: none;
}

.sala-img {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.sala-body {
  padding: 0.95rem;
  color: #2f221d;
}

.sala-ubicacion {
  margin: 0.35rem 0 0.7rem;
  color: #6f5c55;
  font-size: 0.9rem;
}

.sala-equipamiento {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin: 0 0 0.75rem;
}

.equipamiento-pill {
  background: #f6efe9;
  border: 1px solid #eadfd8;
  color: #5a463f;
  border-radius: 999px;
  padding: 0.2rem 0.55rem;
  font-size: 0.75rem;
}

.sala-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.6rem;
}

.sala-top h3 {
  margin: 0;
  font-size: 1.08rem;
}

.sala-desc {
  margin: 0.6rem 0;
  font-size: 0.9rem;
  color: #65524c;
  min-height: 38px;
}

.sala-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.88rem;
  color: #4e3e38;
  margin-bottom: 0.8rem;
}

.status-pill {
  padding: 0.25rem 0.55rem;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
}

.status-pill.activo {
  background: #e5f8ee;
  color: #2b8f62;
}

.status-pill.inactivo {
  background: #fdecee;
  color: #bf4b58;
}

.status-pill.eliminada {
  background: #e8e8e8;
  color: #666666;
}

.acciones {
  display: flex;
  gap: 0.55rem;
}

.btn-edit,
.btn-toggle,
.btn-delete {
  flex: 1;
  border: none;
  border-radius: 10px;
  padding: 0.55rem;
  cursor: pointer;
  font-weight: 600;
}

.btn-edit {
  background: #4a3530;
  color: #ffffff;
}

.btn-toggle {
  background: #f5ede7;
  color: #4a3530;
}

.btn-delete {
  background: #fdecee;
  color: #a73745;
}

.empty-state {
  border: 1px dashed rgba(255, 255, 255, 0.35);
  border-radius: 14px;
  padding: 1rem;
  color: #f2e6de;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 50px 0;
}

.modal {
  background: linear-gradient(180deg, #fffefd 0%, #fffbf7 100%);
  color: #2f221d;
  padding: 1.35rem;
  border-radius: 20px;
  border: 1px solid #ecdccf;
  width: min(1040px, 95vw);
  max-height: 92vh;
  overflow: auto;
  display: flex;
  flex-direction: column;
  gap: 0.95rem;
  text-shadow: none;
  box-shadow: 0 30px 80px rgba(19, 11, 8, 0.45);
}

.modal h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2f221d;
  letter-spacing: -0.01em;
}

.modal-confirm-delete {
  width: min(480px, 92vw);
}

.delete-copy {
  margin: 0;
  color: #5f4b43;
  line-height: 1.5;
}

.form-sala-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
  gap: 0.9rem;
  align-items: start;
}

.form-col-main,
.form-col-side {
  background: #ffffff;
  border: 1px solid #efe3d8;
  border-radius: 16px;
  padding: 0.95rem;
  display: flex;
  flex-direction: column;
  gap: 0.72rem;
}

.form-col-side {
  background: linear-gradient(180deg, #fffaf4 0%, #f8eee5 100%);
}

.modal input,
.modal textarea,
.modal select {
  width: 100%;
  padding: 0.72rem 0.76rem;
  border: 1px solid #dfd1c6;
  border-radius: 12px;
  background: #fffdfb;
  color: #2b1f1a;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
}

.modal textarea {
  min-height: 110px;
  resize: vertical;
}

.modal input:focus,
.modal textarea:focus,
.modal select:focus {
  border-color: #9d7766;
  box-shadow: 0 0 0 3px rgba(157, 119, 102, 0.16);
  background: #ffffff;
}

.grupo-cols {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.65rem;
}

.helper-text {
  margin-top: 0.3rem;
  display: block;
  color: #7a655b;
  font-size: 0.78rem;
}

.grupo-form.estado-switch label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0;
}

.grupo-form.estado-switch input[type='checkbox'] {
  width: 16px;
  height: 16px;
  accent-color: #5d4035;
}

.form-error {
  margin: 0;
  padding: 0.55rem 0.65rem;
  border-radius: 8px;
  background: #fdecec;
  color: #b42318;
  border: 1px solid #f5c8c8;
  font-size: 0.88rem;
}

.grupo-form label {
  display: block;
  margin-bottom: 0.35rem;
  font-weight: 700;
  color: #4c3932;
  font-size: 0.9rem;
}

.equipamiento-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.45rem;
  max-height: 340px;
  overflow: auto;
  padding-right: 0.35rem;
}

.equipamiento-opcion {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  font-size: 0.88rem;
  color: #4b3a34;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid #e8d8cb;
  border-radius: 12px;
  padding: 0.5rem 0.6rem;
  transition: border-color 0.18s ease, background-color 0.18s ease;
}

.equipamiento-opcion:hover {
  border-color: #cfb6a8;
  background: #fffdf9;
}

.equipamiento-opcion input {
  width: 16px;
  height: 16px;
  accent-color: #5d4035;
}

.modal-btns {
  display: flex;
  justify-content: end;
  gap: 0.55rem;
  grid-column: 1 / -1;
}

.form-error {
  grid-column: 1 / -1;
}

.modal-btns button {
  border: none;
  border-radius: 999px;
  padding: 0.66rem 1.05rem;
  cursor: pointer;
  font-weight: 700;
  transition: transform 0.18s ease, box-shadow 0.18s ease, background-color 0.18s ease;
}

.modal-btns button:first-child {
  background: #f1e5da;
  color: #5a443b;
}

.btn-save {
  background: linear-gradient(135deg, #4a3530, #2c1f1b);
  color: #ffffff;
  box-shadow: 0 8px 18px rgba(47, 34, 29, 0.28);
}

.btn-delete-confirm {
  background: #a73745 !important;
  color: #ffffff !important;
}

.solo-confirmacion {
  margin-top: 1rem;
}

.modal-btns button:hover {
  transform: translateY(-1px);
}

.modal-btns button:first-child:hover {
  background: #ebddcf;
}

.btn-save:hover {
  background: linear-gradient(135deg, #5c433c, #31221d);
  box-shadow: 0 10px 22px rgba(47, 34, 29, 0.32);
}

@media (max-width: 920px) {
  .form-sala-layout {
    grid-template-columns: 1fr;
  }

  .equipamiento-grid {
    max-height: 240px;
  }
}

.home-velo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(255, 255, 255, 0.25);
  z-index: 1;
  pointer-events: none;
}


@media (max-width: 600px) {
  .kpi-grid {
    
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 0.75rem; 
  }

  .kpi-card {
   
    padding: 0.8rem; 
  }

  .kpi-card strong {
    font-size: 1.15rem; 
  }
}
</style>