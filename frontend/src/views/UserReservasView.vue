<template>
  <div class="mis-reservas-container">
    <h1>Mis Reservas</h1>
    <p class="descripcion">Aquí puedes consultar y gestionar tus próximos espacios.</p>

    <div v-if="cargando" class="estado">Cargando tus datos...</div>

    <div v-else-if="reservas.length === 0" class="estado-vacio">
      <p>No tienes reservas registradas.</p>
      <router-link to="/" class="btn-enlace">Explorar salas ahora</router-link>
    </div>

    <div v-else class="reservas-grid">
      <article v-for="reserva in reservas" :key="reserva.id" class="reserva-card">
        <img :src="getRoomImage(reserva.room_name)" :alt="`Imagen de ${reserva.room_name}`" class="card-image" />

        <div class="card-body">
          <div class="card-header">
            <h3 class="nombre-sala">{{ reserva.room_name }}</h3>
            <span :class="['badge', reserva.status]">
              {{ reserva.status === 'confirmed' ? 'Confirmada' : 'Cancelada' }}
            </span>
          </div>

          <div class="card-info">
            <p><strong>Inicio:</strong> {{ reserva.start_time }}</p>
            <p><strong>Fin:</strong> {{ reserva.end_time }}</p>
            <p><strong>Total:</strong> {{ reserva.total_price }}€</p>
          </div>

          <button 
            v-if="reserva.status === 'confirmed'" 
            @click="abrirModalCancelacion(reserva)"
            class="btn-cancelar"
          >
            Cancelar reserva
          </button>
        </div>
      </article>
    </div>

    <div v-if="mostrarModalCancelacion" class="modal-overlay" @click.self="cerrarModalCancelacion">
      <div class="modal-confirmacion">
        <h3>¿Cancelar reserva?</h3>
        <p>
          Vas a cancelar
          <strong>{{ reservaACancelar?.room_name || 'esta reserva' }}</strong>.
          Esta acción no se puede deshacer.
        </p>

        <div class="modal-acciones">
          <button type="button" class="btn-modal-secundario" :disabled="cancelando" @click="cerrarModalCancelacion">
            Volver
          </button>
          <button type="button" class="btn-modal-peligro" :disabled="cancelando" @click="confirmarCancelacion">
            {{ cancelando ? 'Cancelando...' : 'Sí, cancelar' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="mensaje" :class="['toast-msg', esError ? 'error' : 'ok']">
      {{ mensaje }}
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
      cargando: true,
      mostrarModalCancelacion: false,
      reservaACancelar: null,
      cancelando: false,
      mensaje: '',
      esError: false,
      mensajeTimer: null
    };
  },
  async created() {
    this.obtenerReservas();
  },
  methods: {
    mostrarMensajeTemporal(texto, esError = false) {
      this.mensaje = texto;
      this.esError = esError;

      if (this.mensajeTimer) {
        clearTimeout(this.mensajeTimer);
      }

      this.mensajeTimer = setTimeout(() => {
        this.mensaje = '';
      }, 4000);
    },
    getRoomImage(roomName) {
      const gallery = [
        'https://images.unsplash.com/photo-1497366811353-6870744d04b2?q=80&w=1200&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1497366754035-f200968a6e72?q=80&w=1200&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=1200&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?q=80&w=1200&auto=format&fit=crop'
      ];

      const key = (roomName || '').split('').reduce((acc, ch) => acc + ch.charCodeAt(0), 0);
      return gallery[key % gallery.length];
    },
    async obtenerReservas() {
      try {
        const token = localStorage.getItem('user-token');
        const response = await axios.get('http://localhost:8000/api/bookings/my-bookings', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.reservas = (response.data || []).filter(reserva => reserva.status === 'confirmed');
      } catch (error) {
        console.error("Error al cargar reservas:", error);
      } finally {
        this.cargando = false;
      }
    },
    abrirModalCancelacion(reserva) {
      this.mensaje = '';
      this.esError = false;
      this.reservaACancelar = reserva;
      this.mostrarModalCancelacion = true;
    },
    cerrarModalCancelacion(forzar = false) {
      if (this.cancelando && !forzar) return;
      this.mostrarModalCancelacion = false;
      this.reservaACancelar = null;
    },
    async confirmarCancelacion() {
      if (!this.reservaACancelar?.id) return;

      const id = this.reservaACancelar.id;
      this.cancelando = true;
      
      // Cerrar el modal inmediatamente
      this.cerrarModalCancelacion(true);

      try {
        const token = localStorage.getItem('user-token');
        await axios.patch(`http://localhost:8000/api/bookings/${id}/cancel`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });

        this.reservas = this.reservas.filter(r => r.id !== id);

        this.mostrarMensajeTemporal('Reserva cancelada con éxito.', false);
      } catch (error) {
        this.mostrarMensajeTemporal(error.response?.data?.message || 'No se pudo cancelar la reserva.', true);
      } finally {
        this.cancelando = false;
      }
    }
  },
  beforeUnmount() {
    if (this.mensajeTimer) {
      clearTimeout(this.mensajeTimer);
    }
  }
};
</script>

<style scoped>
.mis-reservas-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  color: #fcfaf7;
}

.mis-reservas-container h1 {
  font-size: 2.2rem;
  margin-bottom: 0.5rem;
}

.descripcion {
  color: #f2e7de;
  margin-bottom: 2rem;
  font-size: 1.05rem;
}

.estado,
.estado-vacio {
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 16px;
  padding: 1.25rem;
  backdrop-filter: blur(3px);
}

.reservas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 1.4rem;
}

.reserva-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  text-shadow: none;
}

.card-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.card-body {
  padding: 1rem;
  color: #2f221d;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.6rem;
  margin-bottom: 0.8rem;
}

.nombre-sala {
  font-weight: 700;
  margin: 0;
  color: #2f221d;
}

.card-info p {
  margin: 0.35rem 0;
  color: #5b4a44;
  font-size: 0.95rem;
}

.badge {
  padding: 0.35rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
}

.badge.confirmed {
  background-color: #e8f6ee;
  color: #1f7a4f;
}

.badge.cancelled {
  background-color: #fdecee;
  color: #a73745;
}

.btn-cancelar {
  margin-top: 0.9rem;
  width: 100%;
  background: transparent;
  border: 1px solid #a73745;
  color: #a73745;
  padding: 0.65rem 0.9rem;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.25s;
}

.btn-cancelar:hover {
  background: #a73745;
  color: #ffffff;
}

.btn-enlace {
  display: inline-block;
  margin-top: 1rem;
  color: #ffffff;
  text-decoration: none;
  font-weight: 700;
  border-bottom: 1px solid rgba(255, 255, 255, 0.75);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
}

.modal-confirmacion {
  width: min(460px, 92vw);
  background: #fff;
  color: #2f221d;
  border-radius: 14px;
  border: 1px solid #eadfd8;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.25);
  padding: 1rem;
  text-shadow: none;
}

.modal-confirmacion h3 {
  margin: 0;
}

.modal-confirmacion p {
  margin: 0.7rem 0 0;
  color: #5f4b43;
  line-height: 1.5;
}

.modal-acciones {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.6rem;
}

.btn-modal-secundario,
.btn-modal-peligro {
  border: none;
  border-radius: 999px;
  padding: 0.56rem 0.9rem;
  cursor: pointer;
  font-weight: 700;
}

.btn-modal-secundario {
  background: #f1e5da;
  color: #564038;
}

.btn-modal-peligro {
  background: #a73745;
  color: #fff;
}

.btn-modal-secundario:disabled,
.btn-modal-peligro:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.toast-msg {
  position: fixed;
  right: 1rem;
  bottom: 1rem;
  border-radius: 10px;
  padding: 0.65rem 0.8rem;
  z-index: 1300;
  font-weight: 600;
  text-shadow: none;
}

.toast-msg.ok {
  background: #e8f6ee;
  color: #1f7a4f;
  border: 1px solid #bde7ca;
}

.toast-msg.error {
  background: #fdecee;
  color: #a73745;
  border: 1px solid #f6c7cf;
}
</style>