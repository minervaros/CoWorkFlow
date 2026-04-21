<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/">CoWorkFlow</router-link>
      </div>
      
      <div class="nav-links">
        <router-link to="/">Inicio</router-link>

        <template v-if="estaLogueado">
          <router-link to="/mis-reservas">Mis Reservas</router-link>
          <router-link to="/reservas">Nueva Reserva</router-link>

          <div v-if="esAdmin" class="admin-section">
            <span class="admin-label">Admin:</span>
            <router-link to="/admin/salas">Salas</router-link>
            <router-link to="/admin/reservas">Reservas Globales</router-link>
          </div>
        </template>

        <router-link v-if="!estaLogueado" to="/login" class="btn-login">Entrar</router-link>
        <a v-else @click.prevent="cerrarSesion" href="#" class="btn-logout">Cerrar Sesión</a>
      </div>
    </nav>

    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    // Comprobamos si hay un token en el Store de Vuex
    estaLogueado() {
      return !!this.$store.state.token;
    },
    // Comprobamos el rol para mostrar u ocultar el menú de admin
    esAdmin() {
      return this.$store.state.role === 'admin';
    }
  },
  methods: {
    cerrarSesion() {
      if (confirm("¿Quieres cerrar sesión?")) {
        this.$store.dispatch('logout');
        this.$router.push('/login');
      }
    }
  }
}
</script>

<style lang="scss">
// Estilos básicos para que el menú se vea profesional
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;

  a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
    &.router-link-exact-active {
      color: #42b983; // Color verde para la página activa
      font-weight: bold;
    }
  }
}

.admin-section {
  display: inline-block;
  margin-left: 20px;
  padding-left: 20px;
  border-left: 1px solid #555;
  
  .admin-label {
    font-size: 0.8rem;
    color: #f1c40f; // Dorado para resaltar que es Admin
    text-transform: uppercase;
    margin-right: 10px;
  }
}

.btn-logout {
  color: #e74c3c !important;
  cursor: pointer;
}
</style>