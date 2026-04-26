<template>
  <div class="config-view">
    <section class="config-card">
      <h1>Configuración</h1>
      <p class="sub">Ajustes básicos de tu cuenta para esta aplicación.</p>

      <label class="opcion">
        <input type="checkbox" v-model="notificacionesEmail" />
        <span>Recibir notificaciones por email</span>
      </label>

      <div class="acciones">
        <button type="button" @click="guardarConfiguracion">Guardar cambios</button>
      </div>

      <div class="opcion-password">
        <h3>Seguridad</h3>
        <p class="sub-sec">Actualiza la contraseña de acceso a tu cuenta.</p>
        <button type="button" class="btn-password" @click="mostrarModalPassword = true">Cambiar contraseña</button>
      </div>
    </section>

    <!-- Modal Cambiar Contraseña -->
    <transition name="modal-fade">
      <div v-if="mostrarModalPassword" class="ui-modal-overlay" @click.self="cerrarModalPassword">
        <div class="ui-modal">
          <h3 class="modal-title">Cambiar contraseña</h3>
          <p class="sub-modal">Introduce tu contraseña actual y la nueva contraseña.</p>
          
          <div class="form-group">
            <label for="current-password">Contraseña actual</label>
            <input 
              id="current-password" 
              type="password" 
              v-model="currentPassword" 
              placeholder="Contraseña actual"
              @keyup.enter="confirmarCambiarPassword"
            />
          </div>
          
          <div class="form-group">
            <label for="new-password">Nueva contraseña</label>
            <input 
              id="new-password" 
              type="password" 
              v-model="newPassword" 
              placeholder="Nueva contraseña"
              @keyup.enter="confirmarCambiarPassword"
            />
          </div>

          <div class="form-group">
            <label for="confirm-password">Confirmar nueva contraseña</label>
            <input 
              id="confirm-password" 
              type="password" 
              v-model="confirmPassword" 
              placeholder="Confirmar nueva contraseña"
              @keyup.enter="confirmarCambiarPassword"
            />
          </div>

          <p v-if="errorPassword" class="error-msg">{{ errorPassword }}</p>
          
          <div class="ui-modal-actions">
            <button class="ui-btn ui-btn-secondary" @click="cerrarModalPassword" :disabled="guardandoPassword">Cancelar</button>
            <button class="ui-btn ui-btn-primary" @click="confirmarCambiarPassword" :disabled="guardandoPassword || !currentPassword || !newPassword || !confirmPassword">
              {{ guardandoPassword ? 'Cambiando...' : 'Cambiar contraseña' }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';

const STORAGE_KEY = 'user-settings';

export default {
  name: 'ConfiguracionView',
  data() {
    return {
      notificacionesEmail: true,
      mostrarModalPassword: false,
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
      errorPassword: '',
      guardandoPassword: false
    };
  },
  created() {
    this.cargarConfiguracion();
  },
  methods: {
    cargarConfiguracion() {
      try {
        const raw = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
        if (typeof raw.notificacionesEmail === 'boolean') {
          this.notificacionesEmail = raw.notificacionesEmail;
        }
      } catch (error) {
        // Si falla el parseo mantenemos valores por defecto
      }
    },
    guardarConfiguracion() {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          notificacionesEmail: this.notificacionesEmail
        })
      );

      localStorage.setItem('ui-notice', JSON.stringify({
        tipo: 'success',
        titulo: 'Configuración guardada',
        mensaje: 'Tus preferencias se han actualizado correctamente.'
      }));

      this.$router.push('/');
    },
    cerrarModalPassword() {
      this.mostrarModalPassword = false;
      this.currentPassword = '';
      this.newPassword = '';
      this.confirmPassword = '';
      this.errorPassword = '';
    },
    async confirmarCambiarPassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.errorPassword = 'Las contraseñas nuevas no coinciden.';
        return;
      }
      if (this.newPassword.length < 6) {
        this.errorPassword = 'La nueva contraseña debe tener al menos 6 caracteres.';
        return;
      }
      this.guardandoPassword = true;
      this.errorPassword = '';
      try {
        await axios.post('http://localhost:8000/api/auth/change-password', {
          current_password: this.currentPassword,
          new_password: this.newPassword
        });
        
        this.cerrarModalPassword();
        
        if (typeof this.$root.mostrarNotificacion === 'function') {
          this.$root.mostrarNotificacion({
            tipo: 'success',
            titulo: 'Contraseña cambiada',
            mensaje: 'Tu contraseña se ha actualizado correctamente.'
          });
        }
      } catch (error) {
        this.errorPassword = error.response?.data?.message || 'Error al cambiar la contraseña.';
      } finally {
        this.guardandoPassword = false;
      }
    }
  }
};
</script>

<style scoped>
.config-view {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 7rem 1rem 2rem;
}

.config-card {
  width: min(92vw, 680px);
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 16px;
  box-shadow: 0 12px 26px rgba(43, 27, 23, 0.1);
  padding: 1.4rem;
  text-shadow: none;
}

.config-card h1 {
  margin: 0;
  color: #2b1b17;
}

.sub {
  color: #6e5e58;
  margin: 0.35rem 0 1.1rem;
}

.opcion {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: #2b1b17;
  padding: 0.55rem 0;
}

.acciones {
  margin-top: 1.1rem;
}

.acciones button {
  border: none;
  background: #1b4fd6;
  color: #ffffff;
  padding: 0.65rem 1rem;
  border-radius: 10px;
  cursor: pointer;
}

.btn-password {
  border: 1px solid #1b4fd6;
  background: transparent;
  color: #1b4fd6;
  padding: 0.65rem 1rem;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-password:hover {
  background: #1b4fd6;
  color: #ffffff;
}

.sub-modal {
  font-size: 0.88rem;
  color: #6e5e58;
  margin: 0.25rem 0 1rem;
  text-align: left;
}

.form-group {
  margin-bottom: 1rem;
  text-align: left;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 500;
  color: #2b1b17;
  margin-bottom: 0.35rem;
}

.form-group input {
  width: 100%;
  padding: 0.65rem 0.9rem;
  border: 1px solid #eadfd8;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  color: #2b1b17;
  background: #ffffff;
}

.error-msg {
  color: #9d2030;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  font-weight: 500;
  text-align: left;
}

.opcion-password {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eadfd8;
  text-align: left;
}

.opcion-password h3 {
  color: #2b1b17;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.sub-sec {
  margin-bottom: 0.8rem;
  color: #6e5e58;
  font-size: 0.9rem;
}

.modal-title {
  color: #2b1b17;
}
</style>
