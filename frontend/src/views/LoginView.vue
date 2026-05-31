<template>
  <div class="login-container">
    <div class="home-velo"></div>
    <div class="auth-card">
      <aside class="auth-panel">
        <div class="auth-panel-content">
          <p class="auth-kicker">CoWorkFlow</p>
        </div>
        <img :src="require('@/assets/cowork-illustration.png')" alt="Equipo en coworking" class="auth-illustration" />
      </aside>

      <form @submit.prevent="manejarLogin" class="formulario-login">
        <h3>Iniciar sesión</h3>
        <p>Introduce tus credenciales para acceder</p>

        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="ejemplo@correo.com" required />
        </div>

        <div class="form-group">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="********" required />
        </div>

        <button type="submit" class="btn-login">Entrar</button>
        
        <p v-if="error" class="error-msg">{{ error }}</p>

        <p class="enlace-registro">¿No tienes cuenta? <router-link to="/register">Regístrate</router-link></p>
      </form>
    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  mounted() {
    const sessionExpiredMessage = localStorage.getItem('session-expired-message');
    if (sessionExpiredMessage) {
      this.error = sessionExpiredMessage;
      localStorage.removeItem('session-expired-message');
      return;
    }

    if (this.$route.query.redirect) {
      this.error = 'Debes iniciar sesión para continuar con tu reserva.';
    }
  },
  methods: {
    async manejarLogin() {
      this.error = null; // Limpiamos errores previos
      
      try {
        // 1. Enviamos la petición al backend (Flask corre en el 8000)
        const respuesta = await axios.post('http://localhost:8000/api/auth/login', {
          email: this.email,
          password: this.password
        });

        // 2. Si el login es correcto, guardamos los datos en la "caja fuerte" (Vuex)
        // Usamos 'dispatch' para llamar a la acción que creamos en el Store
        await this.$store.dispatch('saveLogin', {
          token: respuesta.data.access_token,
          refreshToken: respuesta.data.refresh_token,
          user: {
            email: this.email,
            nombre_completo: respuesta.data.user.full_name || '',
            role: respuesta.data.user.role // Si tu backend lo devuelve
          }
        });

        console.log("¡Login exitoso!");

        // 3. Redirigimos al destino original (si venía de una ruta protegida)
        const redirect = this.$route.query.redirect;
        if (typeof redirect === 'string' && redirect.startsWith('/')) {
          this.$router.push(redirect);
        } else {
          this.$router.push('/');
        }

      } catch (err) {
        // 4. Si hay un error (401, 404, 500...), lo mostramos
        if (err.response && err.response.data) {
          this.error = err.response.data.message || "Credenciales incorrectas";
        } else {
          this.error = "No se pudo conectar con el servidor";
        }
        console.error("Error en el login:", err);
      }
    }
  }
}
</script>

<style lang="scss" scoped>


@media (max-width: 860px) {
  .auth-card {
    grid-template-columns: 1fr;
  }
  .auth-panel {
    display: none !important;
  }
  .login-titulo-movil {
    display: block;
  }
}
@media (max-width: 600px) {
  .formulario-login {
    padding: 1.1rem 0.7rem;
    max-width: 99vw;
    max-height: 98vh;
    min-height: 520px;
    overflow-y: visible;
  }
  .form-group input {
    padding: 0.7rem 0.7rem;
    font-size: 1.08rem;
  }
  .btn-login{
    margin-top: 30px;
  }
}
$color-primario: #362521;
$color-acento: #1b4fd6;
$color-oscuro: #2b1b17;
$color-error: #b42318;

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
  padding: 2rem 1.25rem;
  position: relative;
  z-index: 2;
}

.login-container > *:not(.home-velo) {
  position: relative;
  z-index: 2;
}

.auth-card {
  width: min(980px, 100%);
  display: grid;
  grid-template-columns: minmax(260px, 0.95fr) minmax(320px, 1fr);
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid #eaddd3;
  box-shadow: 0 20px 46px rgba(43, 27, 23, 0.12);
  text-shadow: none;
}

.auth-panel {
  background: linear-gradient(180deg, #f4ebe3 0%, #e9ded4 100%);
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 360px;

  .auth-panel-content {
    position: relative;
    z-index: 2;
    padding: 2.1rem 1.8rem;
  }

  .auth-kicker {
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.78rem;
    color: #6e5e58;
    margin: 0 0 0.6rem;
    font-weight: 700;
  }

  .auth-illustration {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center bottom;
    z-index: 1;
    opacity: 0.75;
  }
}

.formulario-login {
  background: white;
  padding: 2rem;
  text-align: left;
  text-shadow: none;

  h3 {
    color: $color-oscuro;
    margin: 0;
    font-size: 1.45rem;
  }

  > p {
    color: #6e5e58;
    margin: 0.45rem 0 1.4rem;
  }
}

.form-group {
  margin-bottom: 1.1rem;

  label {
    display: block;
    margin-bottom: 0.45rem;
    font-weight: 600;
    color: $color-oscuro;
  }

  input {
    width: 100%;
    padding: 0.82rem 0.9rem;
    border: 1px solid #e2d7cf;
    border-radius: 999px;
    box-sizing: border-box;
    color: $color-oscuro;

    &:focus {
      outline: none;
      border-color: $color-acento;
      box-shadow: 0 0 0 3px rgba(27, 79, 214, 0.14);
    }
  }
}

.btn-login {
  width: 100%;
  padding: 0.9rem;
  background-color: $color-primario;
  color: white;
  border: none;
  border-radius: 999px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;

  &:hover {
    background-color: #4a3530;
    transform: translateY(-1px);
  }
}

.error-msg {
  color: $color-error;
  margin-top: 0.9rem;
  font-size: 0.9rem;
  text-align: center;
}

.enlace-registro {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.88rem;
  color: #6e5e58;

  a {
    color: $color-acento;
    font-weight: 700;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }
}

@media (max-width: 860px) {
  .auth-card {
    grid-template-columns: 1fr;
  }

  .auth-panel {
    padding: 1.5rem;
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