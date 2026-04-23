<template>
  <div id="app">
    <nav class="navbar" :class="{ 'is-landing': $route.name === 'landing' && !esAdmin, 'is-admin': esAdmin }">
      <div class="nav-brand">
        <router-link :to="esAdmin ? '/admin/reservas' : '/'">CoWorkFlow</router-link>
      </div>

      <div v-if="esAdmin" class="nav-links nav-links-admin">
        <span class="admin-label">Panel Admin</span>
        <router-link to="/admin/reservas">Reservas</router-link>
        <router-link to="/admin/tours">Tours</router-link>
        <router-link to="/admin/salas">Salas</router-link>
        <button type="button" class="nav-link-btn" @click="confirmarCerrarSesion">Cerrar sesión</button>
      </div>

      <div v-else class="nav-links">
        <router-link to="/">Inicio</router-link>
        <router-link :to="{ path: '/', hash: '#servicios' }">Servicios</router-link>
        <router-link to="/salas">Catálogo</router-link>
        <button type="button" class="nav-link-btn" @click="abrirModalContacto">Contacto</button>

        <div class="tour-menu" @keyup.esc="cerrarMenuTour">
          <button
            type="button"
            class="btn-reservar-tour"
            :class="{ activo: mostrarMenuTour }"
            :aria-expanded="mostrarMenuTour ? 'true' : 'false'"
            @click="toggleMenuTour"
          >
            Reservar Tour
            <svg class="tour-chevron" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>

          <transition name="tour-fade">
            <div v-if="mostrarMenuTour" class="tour-dropdown">
              <p class="tour-dropdown-label">Elige tu sede</p>
              <router-link
                v-for="sede in sedes"
                :key="sede.slug"
                :to="{ path: '/reservar-tour', query: { sede: sede.slug } }"
                class="tour-sede-item"
                @click="cerrarMenuTour"
              >
                <span class="tour-sede-nombre">{{ sede.nombre }}</span>
                <span class="tour-sede-barrio">{{ sede.barrio }}</span>
              </router-link>
            </div>
          </transition>
        </div>

        <template v-if="estaLogueado">
          <div v-if="estaLogueado && esAdmin" class="admin-section">
            <span class="admin-label">Admin:</span>
            <router-link to="/admin/salas">Salas</router-link>
            <router-link to="/admin/reservas">Reservas Globales</router-link>
            <router-link to="/admin/tours">Tours</router-link>
          </div>
        </template>

        <div class="auth-actions">
          <router-link v-if="!estaLogueado" to="/login" class="btn-login">Entrar</router-link>

          <div v-else class="profile-menu" @keyup.esc="cerrarMenuPerfil">
            <button
              class="profile-btn"
              type="button"
              aria-label="Abrir menú de perfil"
              :aria-expanded="mostrarMenuPerfil ? 'true' : 'false'"
              @click="toggleMenuPerfil"
            >
              <svg viewBox="0 0 24 24" role="img" aria-hidden="true">
                <path d="M12 2a5.5 5.5 0 1 1 0 11 5.5 5.5 0 0 1 0-11zm0 12.5c4.53 0 8.2 2.76 8.2 6.17a.75.75 0 0 1-.75.75H4.55a.75.75 0 0 1-.75-.75c0-3.41 3.67-6.17 8.2-6.17z"/>
              </svg>
            </button>

            <transition name="profile-fade">
              <div v-if="mostrarMenuPerfil" class="profile-dropdown">
                <div class="profile-summary">
                  <strong>{{ usuarioEmailMostrado }}</strong>
                </div>

                <router-link to="/perfil" @click="cerrarMenuPerfil">Mi perfil</router-link>
                <router-link to="/mis-reservas" @click="cerrarMenuPerfil">Mis reservas</router-link>
                <router-link to="/favoritos" @click="cerrarMenuPerfil">Favoritos</router-link>
                <router-link to="/configuracion" @click="cerrarMenuPerfil">Configuración</router-link>

                <button type="button" class="profile-logout" @click="abrirModalCerrarSesionDesdePerfil">
                  Cerrar sesión
                </button>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </nav>

    <router-view/>

    <footer class="site-footer">
      <div class="site-footer-inner">
        <div class="footer-brand">
          <strong>CoWorkFlow</strong>
          <p>Espacios de trabajo premium en Valencia.</p>
        </div>

        <div class="footer-contact">
          <a href="tel:+34960000000">+34 960 000 000</a>
          <a href="mailto:coworkflowvalencia@gmail.com">coworkflowvalencia@gmail.com</a>
        </div>

        <div class="footer-social" aria-label="Redes sociales">
          <div class="footer-social-item" aria-label="Instagram">
            <svg viewBox="0 0 24 24" role="img" aria-hidden="true">
              <path d="M7.75 2h8.5A5.75 5.75 0 0 1 22 7.75v8.5A5.75 5.75 0 0 1 16.25 22h-8.5A5.75 5.75 0 0 1 2 16.25v-8.5A5.75 5.75 0 0 1 7.75 2zm0 1.5A4.25 4.25 0 0 0 3.5 7.75v8.5a4.25 4.25 0 0 0 4.25 4.25h8.5a4.25 4.25 0 0 0 4.25-4.25v-8.5a4.25 4.25 0 0 0-4.25-4.25h-8.5zm8.9 1.95a1.15 1.15 0 1 1 0 2.3 1.15 1.15 0 0 1 0-2.3zM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7z"/>
            </svg>
            <span>@crea.valencia</span>
          </div>
          <div class="footer-social-item" aria-label="LinkedIn">
            <svg viewBox="0 0 24 24" role="img" aria-hidden="true">
              <path d="M6.75 8.25a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zM5.5 9.75h2.5V19h-2.5V9.75zM10 9.75h2.4V11h.03c.34-.64 1.17-1.31 2.41-1.31 2.58 0 3.06 1.7 3.06 3.91V19h-2.5v-4.78c0-1.14-.02-2.6-1.58-2.6-1.58 0-1.82 1.23-1.82 2.51V19H10V9.75z"/>
            </svg>
            <span>Crea Valencia Hub</span>
          </div>
          <div class="footer-social-item" aria-label="Facebook">
            <svg viewBox="0 0 24 24" role="img" aria-hidden="true">
              <path d="M13.5 21v-7h2.35l.35-2.73H13.5v-1.74c0-.79.22-1.33 1.35-1.33h1.44V5.77c-.7-.08-1.4-.12-2.1-.12-2.08 0-3.5 1.27-3.5 3.6v2.02H8.35V14h2.34v7h2.81z"/>
            </svg>
            <span>CoworkFlow Valencia</span>
          </div>
        </div>
      </div>
    </footer>

    <transition name="toast-fade">
      <div v-if="notificacion.visible" :class="['ui-toast', notificacion.tipo, { 'is-prominent': notificacion.tipo === 'warning' }]">
        <div v-if="notificacion.tipo === 'warning'" class="ui-toast-icon" aria-hidden="true">⚠️</div>
        <div class="ui-toast-title">{{ notificacion.titulo }}</div>
        <div class="ui-toast-message">{{ notificacion.mensaje }}</div>
      </div>
    </transition>

    <transition name="modal-fade">
      <div v-if="mostrarModalContacto" class="ui-modal-overlay" @click.self="cerrarModalContacto">
        <div class="ui-modal ui-modal-contacto" role="dialog" aria-modal="true" aria-label="Formulario de contacto">
          <button type="button" class="ui-modal-close" aria-label="Cerrar formulario de contacto" @click="cerrarModalContacto">×</button>
          <ContactoView :enModal="true" />
        </div>
      </div>
    </transition>

    <transition name="modal-fade">
      <div v-if="mostrarModalLogout" class="ui-modal-overlay" @click.self="mostrarModalLogout = false">
        <div class="ui-modal">
          <h3>¿Quieres cerrar sesión?</h3>
          <p>Tu sesión actual se cerrará y volverás a la pantalla de login.</p>
          <div class="ui-modal-actions">
            <button class="ui-btn ui-btn-secondary" @click="mostrarModalLogout = false">Cancelar</button>
            <button class="ui-btn ui-btn-primary" @click="confirmarCerrarSesion">Cerrar sesión</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import ContactoView from './views/ContactoView.vue';

export default {
  name: 'App',
  components: {
    ContactoView
  },
  data() {
    return {
      mostrarModalContacto: false,
      mostrarModalLogout: false,
      notificacion: {
        visible: false,
        tipo: 'info',
        titulo: '',
        mensaje: ''
      },
      notificacionTimer: null,
      mostrarMenuPerfil: false,
      mostrarMenuTour: false,
      sedes: [
        { nombre: 'Crea. Ruzafa', barrio: 'Ruzafa', slug: 'ruzafa' },
        { nombre: 'Crea. El Carmen', barrio: 'El Carmen', slug: 'el-carmen' },
        { nombre: 'Crea. Eixample', barrio: 'Eixample', slug: 'eixample' },
        { nombre: 'Crea. El Cabanyal', barrio: 'El Cabanyal', slug: 'el-cabanyal' }
      ]
    };
  },
  computed: {
    esRutaAdmin() {
      return this.$route.path.startsWith('/admin');
    },
    // Comprobamos si hay un token en el Store de Vuex
    estaLogueado() {
      return !!this.$store.state.token;
    },
    // Comprobamos el rol para mostrar u ocultar el menú de admin
    esAdmin() {
      return this.estaLogueado && this.$store.state.role === 'admin';
    },
    usuarioEmailMostrado() {
      if (this.$store.state.user?.email) {
        return this.$store.state.user.email;
      }

      const emailGuardado = localStorage.getItem('user-email');
      if (emailGuardado) return emailGuardado;

      const token = localStorage.getItem('user-token');
      if (!token) return 'Usuario';

      const payload = this.parseJwt(token);
      return payload?.email || payload?.sub || payload?.identity || 'Usuario';
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
    },
    toggleMenuPerfil() {
      this.mostrarMenuPerfil = !this.mostrarMenuPerfil;
    },
    cerrarMenuPerfil() {
      this.mostrarMenuPerfil = false;
    },
    toggleMenuTour() {
      this.mostrarMenuTour = !this.mostrarMenuTour;
    },
    cerrarMenuTour() {
      this.mostrarMenuTour = false;
    },
    handleClickFueraTour(event) {
      if (!this.mostrarMenuTour) return;
      const contenedor = this.$el.querySelector('.tour-menu');
      if (contenedor && !contenedor.contains(event.target)) {
        this.cerrarMenuTour();
      }
    },
    handleClickFueraPerfil(event) {
      if (!this.mostrarMenuPerfil) return;
      const contenedorPerfil = this.$el.querySelector('.profile-menu');
      if (contenedorPerfil && !contenedorPerfil.contains(event.target)) {
        this.cerrarMenuPerfil();
      this.cerrarMenuTour();
      }
    },
    abrirModalCerrarSesion() {
      this.cerrarMenuPerfil();
      this.mostrarModalLogout = true;
    },
    abrirModalCerrarSesionDesdePerfil() {
      this.abrirModalCerrarSesion();
    },
    abrirModalContacto() {
      this.mostrarModalContacto = true;
      this.cerrarMenuPerfil();
    },
    cerrarModalContacto() {
      this.mostrarModalContacto = false;
    },
    handleGlobalKeydown(event) {
      if (event.key !== 'Escape') return;
      if (this.mostrarModalContacto) this.cerrarModalContacto();
      if (this.mostrarModalLogout) this.mostrarModalLogout = false;
    },
    confirmarCerrarSesion() {
      this.mostrarModalLogout = false;
      this.cerrarMenuPerfil();
      this.$store.dispatch('logout');
      this.$router.push('/login');
      this.mostrarNotificacion({
        tipo: 'success',
        titulo: 'Sesión cerrada',
        mensaje: 'Has cerrado sesión correctamente.'
      });
    },
    mostrarNotificacion({ tipo = 'info', titulo = '', mensaje = '' }) {
      if (this.notificacionTimer) {
        clearTimeout(this.notificacionTimer);
      }

      this.notificacion = {
        visible: true,
        tipo,
        titulo,
        mensaje
      };

      const duracion = tipo === 'warning' ? 8000 : 3600;
      this.notificacionTimer = setTimeout(() => {
        this.notificacion.visible = false;
      }, duracion);
    },
    consumirNotificacionPendiente() {
      try {
        const raw = localStorage.getItem('ui-notice');
        if (!raw) return;
        const payload = JSON.parse(raw);
        localStorage.removeItem('ui-notice');
        this.mostrarNotificacion(payload);
      } catch (error) {
        localStorage.removeItem('ui-notice');
      }
    }
  },
  mounted() {
    this.consumirNotificacionPendiente();
    document.addEventListener('click', this.handleClickFueraPerfil);
    document.addEventListener('click', this.handleClickFueraTour);
    document.addEventListener('keydown', this.handleGlobalKeydown);
  },
  watch: {
    $route() {
      this.consumirNotificacionPendiente();
      this.cerrarMenuPerfil();
      this.cerrarModalContacto();
    }
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickFueraPerfil);
    document.removeEventListener('click', this.handleClickFueraTour);
    document.removeEventListener('keydown', this.handleGlobalKeydown);
    if (this.notificacionTimer) {
      clearTimeout(this.notificacionTimer);
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
  background-image: url('https://images.unsplash.com/photo-1497366754035-f200968a6e72?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  background-repeat: no-repeat;
  color: #fcfaf7;
  font-family: 'Inter', sans-serif;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
}

/* --- TARJETAS ESTILO GALERÍA DE ARTE --- */
.stat-card, .dashboard-visual, .tabla-contenedor {
  text-shadow: none !important;
  background: #ffffff !important;
  border: 1px solid #eaddd3 !important; /* Borde sutil color arena */
  border-radius: 0px !important; /* Acabado recto y minimalista, o muy ligeramente redondeado (max 4px) */
  box-shadow: 0 4px 20px rgba(43, 27, 23, 0.02) !important; /* Sombra ultra ligera */
  transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1) !important;
}

// Navbar transparente con paleta editorial
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 3rem;
  font-size: 1.1rem;
  background: transparent;
  color: #fcfaf7;

  a,
  .nav-link-btn {
    color: #fcfaf7;
    text-decoration: none;
    margin: 0 10px;
    font-size: 1.05rem;
    font-weight: 500;
    letter-spacing: 0.01em;
    transition: color 0.25s ease;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.75);
    background: transparent;
    border: none;
    cursor: pointer;
    font-family: inherit;
    padding: 0;

    &:hover {
      color: #ffffff;
    }

    &.router-link-exact-active {
      color: #ffffff;
      font-weight: 600;
      border-bottom: 1px solid #ffffff;
      padding-bottom: 2px;
    }
  }
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.nav-links-admin {
  gap: 0.55rem;
}

.navbar.is-admin {
  position: sticky;
  top: 0;
  z-index: 30;
  background: rgba(25, 16, 13, 0.92);
  border-bottom: 1px solid rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(8px);
}

.navbar.is-admin .admin-label {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #f1dfd1;
  margin-right: 0.25rem;
}

.navbar.is-landing {
  position: absolute;
  top: 90px;
  left: 86px;
  right: 86px;
  width: auto;
  padding: 0.95rem 1.6rem;
  z-index: 8;
}

@media (max-width: 768px) {
  .navbar.is-landing {
    top: 52px;
    left: 48px;
    right: 48px;
    padding: 0.75rem 1rem;
  }
}

.admin-section {
  display: inline-block;
  margin-left: 20px;
  padding-left: 20px;
  border-left: 1px solid rgba(252, 250, 247, 0.5);
  
  .admin-label {
    font-size: 0.8rem;
    color: #fcfaf7;
    text-transform: uppercase;
    margin-right: 10px;
  }
}

.btn-logout {
  color: #fcfaf7 !important;
  cursor: pointer;
}

.auth-actions {
  display: inline-flex;
  align-items: center;
  margin-left: 0.35rem;
}

.profile-menu {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.profile-btn {
  width: 2.35rem;
  height: 2.35rem;
  border-radius: 999px;
  border: 1px solid rgba(252, 250, 247, 0.62);
  background: rgba(255, 255, 255, 0.08);
  color: #fcfaf7;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-left: 0.35rem;
}

.profile-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #ffffff;
}

.profile-btn svg {
  width: 1.18rem;
  height: 1.18rem;
  fill: currentColor;
}

.profile-dropdown {
  position: absolute;
  top: calc(100% + 0.55rem);
  right: 0;
  min-width: 240px;
  background: #ffffff;
  border: 1px solid #eadfd8;
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(30, 20, 16, 0.18);
  padding: 0.6rem;
  z-index: 40;
  text-shadow: none;
}

.profile-summary {
  padding: 0.35rem 0.5rem 0.6rem;
  border-bottom: 1px solid #f0e5dd;
  margin-bottom: 0.35rem;
}

.profile-summary strong {
  display: block;
  color: #2b1b17;
  font-size: 0.9rem;
  line-height: 1.2;
  word-break: break-word;
}

.profile-summary small {
  color: #7b6b64;
  font-size: 0.78rem;
}

.profile-dropdown a,
.profile-logout {
  display: block;
  width: 100%;
  text-align: left;
  text-decoration: none;
  color: #2b1b17 !important;
  border: none;
  background: transparent;
  border-radius: 8px;
  padding: 0.55rem 0.55rem;
  margin: 0;
  font-size: 0.93rem;
  font-weight: 500;
  text-shadow: none;
  cursor: pointer;
}

.profile-dropdown a:hover,
.profile-logout:hover {
  background: #f8f3ef;
}

.profile-logout {
  color: #9d2030 !important;
}

.btn-login {
  border: 1px solid #fcfaf7;
  padding: 0.45rem 0.9rem;
  border-radius: 999px;
}

.btn-login:hover,
.btn-logout:hover {
  color: #ffffff !important;
}

.tour-menu {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.btn-reservar-tour {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.45rem 0.9rem;
  border-radius: 999px;
  background: transparent;
  color: #fcfaf7 !important;
  font-weight: 500;
  font-size: inherit;
  letter-spacing: inherit;
  border: 1px solid #fcfaf7;
  cursor: pointer;
  font-family: inherit;
  text-shadow: none !important;
  transition: background 0.2s, color 0.2s;

  .tour-chevron {
    width: 0.9rem;
    height: 0.9rem;
    stroke: currentColor;
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
    transition: transform 0.22s ease;
  }

  &.activo .tour-chevron,
  &:hover .tour-chevron {
    transform: rotate(180deg);
  }

  &:hover,
  &.activo {
    background: rgba(255, 255, 255, 0.12);
    color: #ffffff !important;
  }
}

.tour-dropdown {
  position: absolute;
  top: calc(100% + 0.55rem);
  left: 50%;
  transform: translateX(-50%);
  min-width: 240px;
  background: #ffffff;
  border: 1px solid #eadfd8;
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(30, 20, 16, 0.18);
  padding: 0.55rem;
  z-index: 40;
  text-shadow: none;
}

.tour-dropdown-label {
  margin: 0 0 0.35rem;
  padding: 0.25rem 0.55rem 0.55rem;
  border-bottom: 1px solid #f0e5dd;
  font-size: 0.72rem;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: #9b8478;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
}

.tour-sede-item {
  display: flex;
  flex-direction: column;
  text-decoration: none !important;
  color: #2b1b17 !important;
  border-radius: 8px;
  padding: 0.5rem 0.55rem;
  transition: background 0.18s;
  text-shadow: none;

  &:hover {
    background: #f8f3ef;
  }
}

.tour-sede-nombre {
  font-size: 0.93rem;
  font-weight: 600;
  color: #2b1b17;
  font-family: 'Inter', sans-serif;
}

.tour-sede-barrio {
  font-size: 0.78rem;
  color: #8c7060;
  font-family: 'Inter', sans-serif;
  margin-top: 0.05rem;
}

.tour-fade-enter-active,
.tour-fade-leave-active {
  transition: opacity 0.16s ease, transform 0.16s ease;
}
.tour-fade-enter-from,
.tour-fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-6px);
}

.site-footer {
  margin-top: 2.2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.28);
  background: rgba(255, 255, 255, 0.42);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  text-shadow: none;
}

.site-footer-inner {
  max-width: 1240px;
  margin: 0 auto;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.footer-brand strong {
  font-size: 1rem;
  letter-spacing: 0.01em;
  color: #111111;
}

.footer-brand p {
  margin-top: 0.2rem;
  color: #111111;
  font-size: 0.88rem;
}

.footer-contact {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.footer-contact a {
  color: #111111;
  text-decoration: none;
  font-size: 0.9rem;
}

.footer-social {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.45rem;
}

.footer-social-item {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  color: #111111;
  font-size: 0.9rem;
}

.footer-social-item span {
  color: #111111;
}

.footer-social svg {
  width: 1rem;
  height: 1rem;
  fill: currentColor;
  flex-shrink: 0;
}

@media (max-width: 900px) {
  .site-footer-inner {
    flex-direction: column;
    align-items: flex-start;
  }
}

.ui-toast {
  position: fixed;
  right: 1.25rem;
  bottom: 1.25rem;
  z-index: 60;
  max-width: 360px;
  background: #ffffff;
  border: 1px solid #eadfd8;
  border-left: 4px solid #1b4fd6;
  border-radius: 12px;
  box-shadow: 0 12px 28px rgba(28, 19, 16, 0.15);
  padding: 0.9rem 1rem;
  text-shadow: none;
}

.ui-toast.success { border-left-color: #1b7a3d; }
.ui-toast.warning { border-left-color: #b54708; }
.ui-toast.error { border-left-color: #b42318; }

.ui-toast.is-prominent {
  top: 1.1rem;
  left: 50%;
  right: auto;
  bottom: auto;
  transform: translateX(-50%);
  width: min(92vw, 540px);
  max-width: 540px;
  border: 2px solid #f79009;
  border-left: 8px solid #b54708;
  box-shadow: 0 18px 45px rgba(181, 71, 8, 0.34);
  padding: 1rem 1.1rem 1rem 3rem;
}

.ui-toast-icon {
  position: absolute;
  left: 1rem;
  top: 0.95rem;
  font-size: 1.15rem;
}

.ui-toast-title {
  color: #2b1b17;
  font-weight: 700;
  font-size: 0.95rem;
}

.ui-toast.is-prominent .ui-toast-title {
  font-size: 1.06rem;
}

.ui-toast-message {
  margin-top: 0.2rem;
  color: #6e5e58;
  font-size: 0.9rem;
  line-height: 1.4;
}

.ui-toast.is-prominent .ui-toast-message {
  font-size: 0.98rem;
  color: #5b3b1b;
}

.ui-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 70;
}

.ui-modal {
  width: min(92vw, 460px);
  background: #ffffff;
  border: 1px solid #eadfd8;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  padding: 1.25rem;
  text-shadow: none;
}

.ui-modal-contacto {
  width: min(92vw, 760px);
  position: relative;
  padding: 1.1rem;
}

.ui-modal-close {
  position: absolute;
  top: 0.55rem;
  right: 0.7rem;
  width: 2rem;
  height: 2rem;
  border: none;
  border-radius: 999px;
  background: #f5ede7;
  color: #5a3f37;
  font-size: 1.15rem;
  line-height: 1;
  cursor: pointer;
}

.ui-modal h3 {
  margin: 0;
  color: #2b1b17;
}

.ui-modal p {
  margin: 0.55rem 0 0;
  color: #6e5e58;
  line-height: 1.5;
}

.ui-modal-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.6rem;
}

.ui-btn {
  border: none;
  border-radius: 999px;
  padding: 0.6rem 1rem;
  font-weight: 600;
  cursor: pointer;
}

.ui-btn-secondary {
  background: #f6efe9;
  color: #5a3f37;
}

.ui-btn-primary {
  background: #1b4fd6;
  color: #ffffff;
}

.toast-fade-enter-active,
.toast-fade-leave-active,
.modal-fade-enter-active,
.modal-fade-leave-active,
.profile-fade-enter-active,
.profile-fade-leave-active {
  transition: all 0.2s ease;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(-14px);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.profile-fade-enter-from,
.profile-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>