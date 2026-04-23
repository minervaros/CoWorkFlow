<template>
  <div class="contenedor-registro">
    <div class="tarjeta-registro">
      <aside class="registro-panel">
        <div class="registro-panel-content">
          <p class="registro-kicker">Comunidad CoWorkFlow</p>
          <h2>Crea tu cuenta</h2>
          <p>Empieza a reservar salas y gestionar tu actividad desde un panel único.</p>
        </div>
        <img :src="require('@/assets/cowork-illustration.png')" alt="Equipo en coworking" class="registro-illustration" />
      </aside>

      <div class="registro-form-area">
        <h3>Alta de usuario</h3>
        <p class="subtitulo">Únete a la comunidad de CoWorkFlow</p>

        <form @submit.prevent="manejarRegistro" class="formulario-registro">
          <div class="campo">
            <label>Nombre completo</label>
            <input v-model="nombre" type="text" placeholder="Tu nombre" required>
          </div>

          <div class="campo">
            <label>Email</label>
            <input v-model="email" type="email" placeholder="email@ejemplo.com" required>
          </div>

          <div class="campo">
            <label>Contraseña</label>
            <input v-model="password" type="password" placeholder="••••••••" required>
          </div>

          <button type="submit" class="boton-registro">Registrarse</button>
        </form>

        <p v-if="error" class="mensaje-error">{{ error }}</p>
        
        <p class="enlace-login">
          ¿Ya tienes cuenta? <router-link to="/login">Inicia sesión aquí</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterView',
  data() {
    return {
      nombre: '',
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async manejarRegistro() {
      this.error = null;
      try {
        // Llamada a la ruta que definiste en tu Blueprint de Flask
        await axios.post('http://localhost:8000/api/auth/register', {
          full_name: this.nombre,
          email: this.email,
          password: this.password
        });

        // Guardamos un mensaje personalizado en localStorage
        localStorage.setItem('ui-notice', JSON.stringify({
          tipo: 'success',
          titulo: '¡Cuenta creada con éxito!',
          mensaje: 'Ahora puedes iniciar sesión con tus credenciales.'
        }));

        // Redirigimos al login
        this.$router.push('/login');

      } catch (err) {
        if (err.response && err.response.data) {
          this.error = err.response.data.message || "Error al registrarse";
        } else {
          this.error = "No se pudo conectar con el servidor";
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
$color-primario: #362521;
$color-acento: #1b4fd6;
$color-oscuro: #2b1b17;
$color-error: #ff5252;

.contenedor-registro {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
  padding: 2rem 1.25rem;
}

.tarjeta-registro {
  display: grid;
  grid-template-columns: minmax(260px, 0.95fr) minmax(340px, 1fr);
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid #eaddd3;
  box-shadow: 0 20px 46px rgba(43, 27, 23, 0.12);
  width: 100%;
  max-width: 980px;
  text-shadow: none;
}

.registro-panel {
  background: linear-gradient(180deg, #f4ebe3 0%, #e9ded4 100%);
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
  min-height: 360px;

  .registro-panel-content {
    position: relative;
    z-index: 2;
    padding: 2.1rem 1.8rem;
  }

  .registro-kicker {
    margin: 0 0 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.78rem;
    color: #f6ece4;
    font-weight: 700;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
  }

  h2 {
    margin: 0;
    color: #ffffff;
    font-size: 2rem;
    line-height: 1.12;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.45);
  }

  p {
    color: #f5ebe4;
    margin: 0.75rem 0 0;
    line-height: 1.5;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
  }

  .registro-illustration {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    z-index: 1;
    opacity: 0.78;
  }
}

.registro-form-area {
  background: white;
  padding: 2rem;
  text-align: left;

  h3 {
    margin: 0;
    color: $color-oscuro;
    font-size: 1.45rem;
  }
}

.subtitulo {
  margin: 0.45rem 0 1.2rem;
  color: #6e5e58;
}

.campo {
  margin-bottom: 1.05rem;
  text-align: left;

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
    color: $color-oscuro;

    &:focus {
      outline: none;
      border-color: $color-acento;
      box-shadow: 0 0 0 3px rgba(27, 79, 214, 0.14);
    }
  }
}

.boton-registro {
  width: 100%;
  padding: 0.9rem;
  background-color: $color-primario;
  color: white;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  transition: background 0.3s, transform 0.2s;

  &:hover {
    background-color: #4a3530;
    transform: translateY(-1px);
  }
}

.mensaje-error {
  color: $color-error;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.enlace-login {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #6e5e58;
  text-align: center;

  a {
    color: $color-acento;
    text-decoration: none;
    font-weight: 700;
  }

  a:hover {
    text-decoration: underline;
  }
}

@media (max-width: 860px) {
  .tarjeta-registro {
    grid-template-columns: 1fr;
  }

  .registro-panel {
    padding: 1.5rem;
  }
}
</style>