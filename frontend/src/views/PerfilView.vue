<template>
  <div class="perfil-view">
    <div class="home-velo"></div>
    <section class="perfil-card">
      <h1>Mi perfil</h1>
      <p class="sub">Aquí puedes ver la información básica de tu cuenta.</p>

      <div class="fila">
        <span class="label">Email</span>
        <span class="valor">{{ emailUsuario }}</span>
      </div>

      <div class="acciones">
        <router-link to="/configuracion" class="btn-config">Ir a configuración</router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'PerfilView',
  computed: {
    emailUsuario() {
      if (this.$store.state.user?.email) {
        return this.$store.state.user.email;
      }

      const emailGuardado = localStorage.getItem('user-email');
      if (emailGuardado) return emailGuardado;

      const token = localStorage.getItem('user-token');
      if (!token) return 'No disponible';

      const payload = this.parseJwt(token);
      return payload?.email || payload?.sub || payload?.identity || 'No disponible';
    }
  },
  methods: {
    parseJwt(token) {
      try {
        const payload = token.split('.')[1];
        return JSON.parse(atob(payload));
      } catch (error) {
        return null;
      }
    }
  }
};
</script>

<style scoped>
.perfil-view {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 7rem 1rem 2rem;
  position: relative;
  z-index: 2;
}

.perfil-view > *:not(.home-velo) {
  position: relative;
  z-index: 2;
}

.perfil-card {
  width: min(92vw, 680px);
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 16px;
  box-shadow: 0 12px 26px rgba(43, 27, 23, 0.1);
  padding: 1.4rem;
  text-shadow: none;
}

.perfil-card h1 {
  margin: 0;
  color: #2b1b17;
}

.sub {
  color: #6e5e58;
  margin: 0.35rem 0 1.1rem;
}

.fila {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 0.6rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f3e9e2;
}

.label {
  color: #8c7a72;
  font-weight: 600;
}

.valor {
  color: #2b1b17;
  word-break: break-word;
}

.acciones {
  margin-top: 1.1rem;
}

.btn-config {
  display: inline-block;
  background: #1b4fd6;
  color: #ffffff;
  text-decoration: none;
  padding: 0.65rem 1rem;
  border-radius: 10px;
}
/* Velo oscuro global como en HomeView */
.home-velo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.55);
  z-index: 1;
  pointer-events: none;
}
</style>
