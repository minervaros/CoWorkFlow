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

/* --- FUENTES DE ESTUDIO DE DISEÑO --- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  -webkit-font-smoothing: antialiased;
}

body {
  background-color: #fcfaf7; /* Fondo hueso/crema idéntico a la imagen */
  color: #2b1b17; /* Marrón oscuro casi negro para los textos, mucho más cálido */
  font-family: 'Inter', sans-serif;
}

/* --- TARJETAS ESTILO GALERÍA DE ARTE --- */
.tarjeta-sala, .stat-card, .dashboard-visual, .tabla-contenedor {
  background: #ffffff !important;
  border: 1px solid #eaddd3 !important; /* Borde sutil color arena */
  border-radius: 0px !important; /* Acabado recto y minimalista, o muy ligeramente redondeado (max 4px) */
  box-shadow: 0 4px 20px rgba(43, 27, 23, 0.02) !important; /* Sombra ultra ligera */
  transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1) !important;
}

.tarjeta-sala:hover {
  transform: translateY(-4px);
  border-color: #bfa38f !important; /* El borde se oscurece al pasar el ratón */
}

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