<template>
  <div class="contenedor-verificacion">
    <div class="tarjeta-verificacion">
      <!-- Icono animado o ilustrativo superior -->
      <div class="header-icono" :class="estado">
        <span v-if="estado === 'cargando'" class="spinner"></span>
        <span v-else-if="estado === 'exito'" class="icono-check">✓</span>
        <span v-else class="icono-error">✗</span>
      </div>

      <div class="contenido-verificacion">
        <h2>{{ titulo }}</h2>
        <p class="mensaje">{{ mensaje }}</p>

        <!-- Botón de acción dependiendo del estado -->
        <button 
          v-if="estado === 'exito'" 
          @click="$router.push('/login')" 
          class="boton-accion"
        >
          Iniciar sesión
        </button>
        <button 
          v-else-if="estado === 'error'" 
          @click="$router.push('/register')" 
          class="boton-accion"
        >
          Volver a registrarse
        </button>
        <button 
          v-else 
          disabled 
          class="boton-accion inactivo"
        >
          Espera un momento...
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VerificarCuentaView',
  data() {
    return {
      estado: 'cargando', // 'cargando', 'exito', 'error'
      titulo: 'Verificando tu cuenta',
      mensaje: 'Estamos procesando tu enlace de verificación. Por favor, no cierres esta ventana.'
    };
  },
  async mounted() {
    const token = this.$route.query.token;

    if (!token) {
      this.estado = 'error';
      this.titulo = 'Enlace inválido';
      this.mensaje = 'No se ha proporcionado ningún token de verificación. Comprueba el enlace de tu correo electrónico.';
      return;
    }

    try {
      // Llamada al endpoint en español
      const respuesta = await axios.get(`http://localhost:8000/api/auth/verificar-cuenta?token=${token}`);
      
      this.estado = 'exito';
      this.titulo = '¡Cuenta verificada!';
      this.mensaje = respuesta.data.message || 'Tu correo electrónico ha sido validado correctamente. Ya puedes acceder al sistema.';
    } catch (error) {
      this.estado = 'error';
      this.titulo = 'Error de verificación';
      if (error.response && error.response.data) {
        this.mensaje = error.response.data.message || 'El token es inválido o ha expirado.';
      } else {
        this.mensaje = 'No se pudo conectar con el servidor para verificar tu cuenta. Inténtalo de nuevo más tarde.';
      }
    }
  }
};
</script>

<style lang="scss" scoped>
$color-primario: #362521;
$color-acento: #1b4fd6;
$color-oscuro: #2b1b17;
$color-exito: #2e7d32;
$color-error: #c62828;
$color-fondo: #fbf8f5;

.contenedor-verificacion {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
  background-color: $color-fondo;
  padding: 2rem 1.25rem;
}

.tarjeta-verificacion {
  background: white;
  border-radius: 24px;
  border: 1px solid #eaddd3;
  box-shadow: 0 20px 46px rgba(43, 27, 23, 0.08);
  width: 100%;
  max-width: 480px;
  text-align: center;
  padding: 3rem 2rem;
  transition: all 0.3s ease;
}

.header-icono {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin: 0 auto 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2.5rem;
  font-weight: bold;
  transition: all 0.4s ease;

  &.cargando {
    background-color: rgba($color-acento, 0.1);
  }

  &.exito {
    background-color: rgba($color-exito, 0.1);
    color: $color-exito;
    border: 2px solid $color-exito;
    animation: scaleIn 0.5s ease-out;
  }

  &.error {
    background-color: rgba($color-error, 0.1);
    color: $color-error;
    border: 2px solid $color-error;
    animation: scaleIn 0.5s ease-out;
  }
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba($color-acento, 0.2);
  border-top-color: $color-acento;
  border-radius: 50%;
  animation: girar 1s linear infinite;
}

h2 {
  color: $color-oscuro;
  font-size: 1.8rem;
  margin: 0 0 1rem;
}

.mensaje {
  color: #6e5e58;
  font-size: 1rem;
  line-height: 1.6;
  margin: 0 0 2.5rem;
}

.boton-accion {
  width: 100%;
  padding: 0.95rem;
  background-color: $color-primario;
  color: white;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  font-size: 1rem;
  transition: background-color 0.3s, transform 0.2s;

  &:hover:not(.inactivo) {
    background-color: #4a3530;
    transform: translateY(-1px);
  }

  &.inactivo {
    background-color: #cccccc;
    cursor: not-allowed;
  }
}

@keyframes girar {
  to {
    transform: rotate(360deg);
  }
}

@keyframes scaleIn {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
