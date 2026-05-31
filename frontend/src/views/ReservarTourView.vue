<template>
  <div class="reservar-tour-view">
    <div class="home-velo"></div>
    <div class="tour-wrap">
      <div class="tour-card">
        <aside class="tour-panel">
          <div class="tour-panel-content">
            <p class="tour-kicker">Visitas guiadas CoWorkFlow</p>
            <h1>Reservar Tour</h1>
            <p>
              Completa el formulario para visitar {{ nombreSedeSeleccionada }}.
              Te confirmaremos por correo lo antes posible.
            </p>
          </div>
          <img :src="require('@/assets/imagen-tour.png')" alt="Visita guiada en coworking" class="tour-illustration" />
        </aside>

        <form class="tour-form" @submit.prevent="enviarFormulario">
          <div class="tour-titulo-movil">Reservar Tour <span v-if="nombreSedeSeleccionada">- {{ nombreSedeSeleccionada }}</span></div>
          <div class="campo">
            <label for="tour-nombre">Nombre completo</label>
            <input id="tour-nombre" v-model.trim="form.nombreCompleto" type="text" placeholder="Ej: Nombre Apellido" required maxlength="120" />
          </div>

          <div class="campo">
            <label for="tour-correo">Correo</label>
            <input id="tour-correo" v-model.trim="form.correo" type="email" placeholder="Ej: ana@correo.com" required maxlength="180" />
          </div>

          <div class="campo">
            <label for="tour-telefono">Num. teléfono</label>
            <input id="tour-telefono" v-model.trim="form.telefono" type="tel" placeholder="Ej: 600 123 456" required maxlength="30" />
          </div>

          <div class="campo campo-duo">
            <div>
              <label for="tour-fecha">Fecha</label>
              <input id="tour-fecha" v-model="form.fecha" type="date" required />
            </div>
            <div>
              <label for="tour-hora">Hora</label>
              <input id="tour-hora" v-model="form.hora" type="time" required />
            </div>
          </div>

          <div class="campo campo-duo">
            <div>
              <label for="tour-personas">Número de personas</label>
              <input id="tour-personas" v-model.number="form.personas" type="number" min="1" max="40" required />
            </div>
            <div>
              <label for="tour-empresa">Nombre de la empresa/autónomo</label>
              <input id="tour-empresa" v-model.trim="form.empresa" type="text" placeholder="Ej: Crea Studio" required maxlength="160" />
            </div>
          </div>

          <div class="acciones">
            <button class="btn-principal" type="submit" :disabled="enviando">
              {{ enviando ? 'Enviando...' : 'Solicitar tour' }}
            </button>
          </div>

          <p v-if="estado.mensaje" :class="['feedback', estado.tipo]">{{ estado.mensaje }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ReservarTourView',
  data() {
    return {
      enviando: false,
      form: {
        nombreCompleto: '',
        correo: '',
        telefono: '',
        fecha: '',
        hora: '',
        personas: 1,
        empresa: ''
      },
      sedesDisponibles: {
        ruzafa: 'Crea. Ruzafa',
        'el-carmen': 'Crea. El Carmen',
        eixample: 'Crea. Eixample',
        'el-cabanyal': 'Crea. El Cabanyal'
      },
      estado: {
        tipo: '',
        mensaje: ''
      }
    };
  },
  computed: {
    sedeSlug() {
      return (this.$route?.query?.sede || '').toString().trim().toLowerCase();
    },
    nombreSedeSeleccionada() {
      const sede = this.sedeSlug;
      if (!sede) return 'la sede seleccionada';
      return this.sedesDisponibles[sede] || 'la sede seleccionada';
    }
  },
  created() {
    const user = this.$store?.state?.user;
    if (user?.full_name) this.form.nombreCompleto = user.full_name;
    if (user?.email) this.form.correo = user.email;
  },
  methods: {
    async validarDisponibilidadTour(token) {
      if (!this.sedeSlug) {
        this.estado = {
          tipo: 'error',
          mensaje: 'Selecciona una sede desde el botón de Reservar Tour.'
        };
        return false;
      }

      try {
        const response = await axios.post(
          'http://localhost:8000/api/bookings/tour-availability',
          {
            sede: this.sedeSlug,
            fecha: this.form.fecha,
            hora: this.form.hora
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        return !!response.data?.available;
      } catch (error) {
        if (error?.response?.status === 409) {
          const conflict = error.response.data?.conflict;
          this.estado = {
            tipo: 'error',
            mensaje: conflict
              ? `Ese horario ya está ocupado (${conflict.room_name}: ${conflict.start} - ${conflict.end}).`
              : (error.response.data?.message || 'Ese horario ya está ocupado para la sede seleccionada.')
          };
          return false;
        }

        this.estado = {
          tipo: 'error',
          mensaje: error?.response?.data?.message || 'No se pudo validar la disponibilidad del tour.'
        };
        return false;
      }
    },
    async enviarFormulario() {
      this.estado = { tipo: '', mensaje: '' };
      this.enviando = true;

      try {
        const token = localStorage.getItem('user-token');
        if (!token) {
          this.estado = {
            tipo: 'error',
            mensaje: 'Debes iniciar sesión para reservar un tour.'
          };
          return;
        }

        const disponible = await this.validarDisponibilidadTour(token);
        if (!disponible) return;

        const payload = {
          sede: this.sedeSlug,
          nombre_completo: this.form.nombreCompleto,
          correo: this.form.correo,
          telefono: this.form.telefono,
          fecha: this.form.fecha,
          hora: this.form.hora,
          personas: this.form.personas,
          empresa: this.form.empresa
        };

        const response = await axios.post(
          'http://localhost:8000/api/bookings/tour-reservations',
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.estado = {
          tipo: 'ok',
          mensaje: response.data?.message || 'Tour reservado correctamente.'
        };

        this.form.telefono = '';
        this.form.fecha = '';
        this.form.hora = '';
        this.form.personas = 1;
        this.form.empresa = '';
      } catch (error) {
        this.estado = {
          tipo: 'error',
          mensaje: error?.response?.data?.message || 'No se pudo enviar la solicitud de tour.'
        };
      } finally {
        this.enviando = false;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.reservar-tour-view {
  min-height: 100vh;
  padding: 7.5rem 1.25rem 2rem;
  background: transparent;
  position: relative;
  z-index: 2;
}

.reservar-tour-view > *:not(.home-velo) {
  position: relative;
  z-index: 2;
}

.tour-wrap {
  max-width: 980px;
  margin: 0 auto;
}

.tour-card {
  display: grid;
  grid-template-columns: minmax(260px, 0.92fr) minmax(340px, 1fr);
  border-radius: 28px;
  overflow: hidden;
  border: 16px solid #ffffff;
  box-shadow: 0 20px 46px rgba(43, 27, 23, 0.12);
  text-shadow: none;
}


.tour-panel {
  background: linear-gradient(180deg, #f4ebe3 0%, #e9ded4 100%);
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  overflow: hidden;
  min-height: 360px;

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(66, 41, 33, 0.62);
    z-index: 2;
    pointer-events: none;
  }

  .tour-panel-content {
    position: relative;
    z-index: 3;
    display: flex;
    flex-direction: column;
    gap: 1.35rem;
    width: 100%;
    padding: 1.1rem 1.8rem 2rem;
  }

  .tour-kicker {
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.78rem;
    color: #ffffff;
    font-weight: 700;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
  }

  h1 {
    margin: 0;
    color: #ffffff;
    font-size: 2.5rem;
    line-height: 1.12;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.45);
    margin-top: 60px;
  }

  p {
    margin: 0;
    color: #ffffff;
    line-height: 1.5;
    font-weight: 500;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.85);
  }

  .tour-illustration {
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

.tour-form {
  background: #fff6ee;
  padding: 1.7rem;
  min-width: 0;
  text-shadow: none;
}

.campo {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  margin-bottom: 0.85rem;
}

.campo-duo {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;

  > div {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    min-width: 0;
  }

  label {
    min-height: 2.75rem;
    display: flex;
    align-items: flex-end;
    line-height: 1.2;
  }
}

.campo label {
  color: #5a3f37;
  font-weight: 600;
}

.campo input {
  border: 1px solid #e1d2c6;
  background: #fffaf6;
  border-radius: 999px;
  box-shadow: 1px 1px 5px rgba(169, 135, 126, 0.12);
  width: 100%;
  min-height: 3rem;
  padding: 0.7rem 0.8rem;
  font: inherit;
  color: #2b1b17;
  box-sizing: border-box;
}

.campo input::placeholder {
  color: #bda79b;
  opacity: 0.8;
}

.campo input:focus {
  outline: 2px solid rgba(27, 79, 214, 0.25);
  border-color: #1b4fd6;
}

.acciones {
  margin-top: 0.8rem;
}

.btn-principal {
  border: none;
  border-radius: 999px;
  background: #6d534d;
  color: #fff;
  padding: 0.8rem 1.2rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-principal:disabled {
  background: #b9aaa1;
  cursor: not-allowed;
}

.btn-principal:hover:not(:disabled) {
  background: #4a3530;
}

.feedback {
  margin: 0.9rem 0 0;
  border-radius: 10px;
  padding: 0.7rem 0.85rem;
  font-weight: 600;
  text-align: center;
}

.feedback.ok {
  background: #ecfdf3;
  color: #05603a;
  border: 1px solid #a6f4c5;
}

.feedback.error {
  background: #fef3f2;
  color: #b42318;
  border: 1px solid #fecdca;
}

@media (max-width: 860px) {
  .tour-card {
    grid-template-columns: 1fr;
  }
  .tour-panel {
    display: none !important;
  }
  .tour-titulo-movil {
    display: block;
  }
  .campo-duo {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 600px) {
  .tour-form {
    padding: 1.1rem 0.7rem 4.5rem 0.7rem;
    max-width: 99vw;
    min-height: 100vh;
    box-sizing: border-box;
    overflow-y: auto;
  }
  .campo input {
    padding: 0.7rem 0.7rem;
    font-size: 1.08rem;
    max-width: 340px;
    width: 92%;
    margin: 0 auto;
    display: block;
  }
  .campo label {
    max-width: 340px;
    width: 92%;
    margin: 0 auto 0.25rem auto;
    display: block;
    text-align: left;
  }
  .reservar-tour-view{
    padding-top: 2rem;
  }
}
// Título pequeño solo para móvil
.tour-titulo-movil {
  display: none;
  text-align: center;
  font-size: 1.18rem;
  color: #6d534d;
  font-weight: 700;
  letter-spacing: 0.04em;
  margin-bottom: 1.9rem;
  margin-top: -0.2rem;
  padding-top: 20px;
}
@media (max-width: 860px) {
  .tour-titulo-movil {
    display: block;
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
