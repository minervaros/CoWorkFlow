<template>
  <div class="config-view">
    <section class="config-card">
      <h1>Configuración</h1>
      <p class="sub">Ajustes básicos de tu cuenta para esta aplicación.</p>

      <label class="opcion">
        <input type="checkbox" v-model="notificacionesEmail" />
        <span>Recibir notificaciones por email</span>
      </label>

      <label class="opcion">
        <input type="checkbox" v-model="recordarPreferencias" />
        <span>Recordar preferencias en este dispositivo</span>
      </label>

      <div class="acciones">
        <button type="button" @click="guardarConfiguracion">Guardar cambios</button>
      </div>
    </section>
  </div>
</template>

<script>
const STORAGE_KEY = 'user-settings';

export default {
  name: 'ConfiguracionView',
  data() {
    return {
      notificacionesEmail: true,
      recordarPreferencias: true
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
        if (typeof raw.recordarPreferencias === 'boolean') {
          this.recordarPreferencias = raw.recordarPreferencias;
        }
      } catch (error) {
        // Si falla el parseo mantenemos valores por defecto
      }
    },
    guardarConfiguracion() {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          notificacionesEmail: this.notificacionesEmail,
          recordarPreferencias: this.recordarPreferencias
        })
      );

      localStorage.setItem('ui-notice', JSON.stringify({
        tipo: 'success',
        titulo: 'Configuración guardada',
        mensaje: 'Tus preferencias se han actualizado correctamente.'
      }));

      this.$router.push('/perfil');
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
</style>
