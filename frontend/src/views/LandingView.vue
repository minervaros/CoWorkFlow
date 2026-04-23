<template>
  <div class="landing-page">
    <section class="hero-stage">
      <div class="destello-interfaz"></div>

      <div class="capsula-flotante top-left">
        <span class="icono">🕒</span> Horas Flexible (Ruzafa)
      </div>
      
      <div class="capsula-flotante top-right">
        <span class="icono">🪑</span> Puesto Flexible
      </div>

      <div class="capsula-flotante bottom-left-badge">
        <span class="icono">🕒</span> Horas Flexible (Ruzafa)
      </div>

      <div class="capsula-flotante bottom-right-badge">
        <span class="icono">📱</span> PHONE BOOTHS
      </div>

      <main class="landing-main">
        <section class="hero-content">
          <h1>Encuentra tu Espacio <em>Crea.</em><br>en Valencia.</h1>
          <p>
            Descubre nodos urbanos de coworking de alta gama. 
            Desconecta, trabaja y reconecta en nuestros espacios premium distribuidos en Ruzafa, El Carmen, Eixample y El Cabanyal.
          </p>
          
          <router-link to="/salas" class="btn-cta">
            Explorar Catálogo
          </router-link>



        </section>
      </main>

      <div class="mapa-flotante-wrap">
        <div class="mapa-circular">
          <img
            :src="mapaImagenUrl"
            @error="manejarErrorMapa"
            alt="Mapa circular"
          />
        </div>
      </div>
    </section>

    <section class="inspira-section">
      <div class="inspira-inner">
        <p class="kicker">Mensajes que mueven equipos</p>
        <h2>Tu mejor trabajo empieza en el entorno correcto</h2>
        <p>
          Diseñamos espacios para que cada reunión tenga foco, cada idea tenga ritmo y cada día de trabajo tenga propósito.
        </p>
      </div>
    </section>

    <section id="servicios" class="opciones-section">
      <div class="opciones-inner">
        <h3>Opciones para todo tipo de coworker</h3>

        <div class="opciones-grid">
          <article class="opcion-card">
            <div class="icono">⏱️</div>
            <h4>Coworking por horas</h4>
            <p>Paga solo por el tiempo que necesitas. Sin contratos eternos.</p>
          </article>

          <article class="opcion-card">
            <div class="icono">🪑</div>
            <h4>Puestos fijos 24/7</h4>
            <p>Tu mesa y tu espacio, siempre disponible para mantener el ritmo.</p>
          </article>

          <article class="opcion-card">
            <div class="icono">💬</div>
            <h4>Salas de reuniones</h4>
            <p>Espacios para presentar, negociar y cerrar acuerdos importantes.</p>
          </article>

          <article class="opcion-card">
            <div class="icono">🏠</div>
            <h4>Oficina virtual</h4>
            <p>Impulsa tu marca con dirección profesional sin perder flexibilidad.</p>
          </article>

          <article class="opcion-card">
            <div class="icono">🔇</div>
            <h4>Cabina insonorizada</h4>
            <p>Ideal para videollamadas, grabaciones o trabajo de concentración total.</p>
          </article>

          <article class="opcion-card">
            <div class="icono">🏢</div>
            <h4>Despachos privados</h4>
            <p>Privacidad, imagen y comodidad para equipos y profesionales premium.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="seccion-metricas">
      <div class="mosaico-metricas">
        <div class="caja-metrica c-superficie">
          <span class="numero">3.200</span>
          <span class="concepto">m² de superficie</span>
        </div>
        <div class="caja-metrica c-sedes">
          <span class="numero">4</span>
          <span class="concepto">sedes urbanas</span>
        </div>
        <div class="caja-metrica c-puestos">
          <span class="numero">320</span>
          <span class="concepto">puestos de trabajo</span>
        </div>
        <div class="caja-metrica c-salas">
          <span class="numero">24</span>
          <span class="concepto">salas de reuniones</span>
        </div>
        <div class="caja-metrica c-oficinas">
          <span class="numero">16</span>
          <span class="concepto">oficinas privadas</span>
        </div>
      </div>

      <div class="contenido-metricas">
        <h2>Coworking <br>en Valencia</h2>
        <p>
          Adéntrate en nuestros 3.200 m² de zonas de trabajo compartidas, oficinas privadas,
          modernas salas de reuniones y espacios sorprendentes para eventos. Los nodos de
          coworking Crea., ubicados en los barrios clave de Valencia, son el punto de
          encuentro para profesionales, equipos y empresas que buscan tanto flexibilidad
          como una nueva forma de trabajar y relacionarse. ¡Ven a conocernos!
        </p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'LandingView',
  data() {
    return {
      mapaImagenUrl: 'https://static-maps.yandex.ru/1.x/?lang=es_ES&ll=-0.3763,39.4699&z=12&l=map&size=300,300&pt=-0.3763,39.4699,pm2rdm',
      mapaImagenFallback: 'https://maps.wikimedia.org/img/osm-intl,12,39.4699,-0.3763,320x320.png'
    };
  },
  methods: {
    manejarErrorMapa(evento) {
      if (this.mapaImagenUrl !== this.mapaImagenFallback) {
        this.mapaImagenUrl = this.mapaImagenFallback;
        return;
      }

      // Último fallback visual para evitar mostrar texto alternativo roto
      evento.target.style.display = 'none';
      evento.target.parentElement.style.background = 'linear-gradient(135deg, #e6ece7, #d6ddd6)';
    }
  }
}
</script>

<style lang="scss" scoped>
/* --- CONFIGURACIÓN BASE DE CONTENEDOR INMERSIVO --- */
.landing-page {
  background: transparent;
  min-height: 100vh;
  width: 100%;
  max-width: 100%;
  color: #2b1b17; /* Tipografía en tono café oscuro premium */
  overflow: visible;
  overflow-x: hidden;
  position: relative;
  box-sizing: border-box;
}

.hero-stage {
  position: relative;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* --- EL MARCO BLANCO CON DESTELLO INTERACTIVO --- */
.hero-stage::after {
  content: "";
  position: absolute;
  top: 68px;
  left: 68px;
  right: 68px;
  bottom: 68px;
  border: 4px solid rgba(255, 255, 255, 0.94); 
  border-radius: 40px; 
  pointer-events: none; 
  z-index: 10;
}



/* --- HÉROE CENTRAL EDITORIAL --- */
.landing-main {
  max-width: 1200px;
  width: 100%;
  padding: 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 5;
}

.hero-content {
  h1 {
    font-family: 'Playfair Display', serif;
    font-size: 4.6rem;
    font-weight: 500;
    line-height: 1.15;
    letter-spacing: -0.01em;
    color: #ffffff;
    margin: 0 0 1.5rem 0;
    opacity: 0;
    animation: sutilReveal 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;

    em {
      font-style: italic;
      font-weight: 400;
    }
  }

  p {
    font-family: 'Inter', sans-serif;
    font-size: 1.25rem;
    color: #ffffff;
    max-width: 720px;
    margin: 0 auto 2.5rem auto;
    line-height: 1.6;
    font-weight: 400;
    opacity: 0;
    animation: sutilReveal 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
  }
}

.btn-cta {
  display: inline-block;
  text-decoration: none;
  background: #fbf7f2;
  color: #2b1b17;
  border: 1px solid #eaddd3;
  padding: 1rem 2.8rem;
  border-radius: 999px;
  font-weight: 500;
  font-size: 1rem;
  letter-spacing: 0.02em;
  box-shadow: 0 8px 24px rgba(43, 27, 23, 0.08);
  transition: transform 0.25s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.25s, box-shadow 0.25s;
  text-shadow: none !important;
  opacity: 0;
  animation: sutilReveal 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.4s forwards;

  &:hover {
    background: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(43, 27, 23, 0.14);
    text-shadow: none !important;
  }
}

/* --- CÁPSULAS FLOTANTES (GLASSMORPHISM PREMIUM) --- */
.capsula-flotante {
  position: absolute;
  z-index: 6;
  padding: 0.75rem 1.4rem;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 999px;
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  color: #ffffff;
  box-shadow: 0 8px 32px 0 rgba(43, 27, 23, 0.06);
  /* Propiedad clave: difumina el fondo de la foto de la oficina */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  pointer-events: none;
  opacity: 0;

  .icono {
    font-size: 1.1rem;
    opacity: 0.85;
  }
}

/* Coordenadas de posicionamiento según esquema Harmont/Crea */
.top-left {
  top: 18%;
  left: 12%;
  animation: sutilReveal 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.5s forwards;
}

.top-right {
  top: 20%;
  right: 14%;
  animation: sutilReveal 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.6s forwards;
}

.bottom-left-badge {
  bottom: 24%;
  left: 10%;
  animation: sutilReveal 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.7s forwards;
}

.bottom-right-badge { 
  bottom: 24%; right: 12%; 
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.06em;
  animation: sutilReveal 1.4s cubic-bezier(0.16, 1, 0.3, 1) 0.8s forwards;
}

/* --- CAPA DEL MAPA CIRCULAR INFERIOR --- */
.mapa-flotante-wrap {
  position: absolute;
  bottom: 11%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 6;
}

.mapa-circular {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 2px solid #ffffff;
  box-shadow: 0 10px 24px rgba(43, 27, 23, 0.15);
  position: relative;
  overflow: hidden;
  opacity: 0;
  animation: sutilReveal 1.6s cubic-bezier(0.16, 1, 0.3, 1) 0.6s forwards;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
}

/* --- ANIMACIONES DE ENTRADA --- */
@keyframes sutilReveal {
  from {
    opacity: 0;
    transform: translateY(24px);
    filter: blur(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

/* --- BLOQUES BAJO EL HÉROE (SCROLL) --- */
.inspira-section {
  background: linear-gradient(180deg, #f7f1eb 0%, #f2e8df 100%);
  padding: 6rem 1.4rem;
  position: relative;
  overflow: hidden;

  &::before,
  &::after {
    content: "";
    position: absolute;
    border-radius: 999px;
    pointer-events: none;
  }

  &::before {
    width: 420px;
    height: 420px;
    right: -120px;
    top: -180px;
    background: radial-gradient(circle, rgba(169, 118, 88, 0.22) 0%, rgba(169, 118, 88, 0) 68%);
    animation: derivaLenta 12s ease-in-out infinite;
  }

  &::after {
    width: 360px;
    height: 360px;
    left: -120px;
    bottom: -190px;
    background: radial-gradient(circle, rgba(104, 71, 53, 0.18) 0%, rgba(104, 71, 53, 0) 68%);
    animation: derivaLenta 16s ease-in-out infinite reverse;
  }
}

.inspira-inner {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  text-shadow: none;
  position: relative;
  z-index: 1;
  animation: entradaSuave 0.9s ease-out both;

  .kicker {
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.78rem;
    color: #7a6458;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
  }

  h2 {
    margin: 0.95rem 0 1.1rem;
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.1rem, 4vw, 3.35rem);
    line-height: 1.08;
    letter-spacing: -0.01em;
    color: #2f221d;
    font-weight: 500;
    text-shadow: none;
  }

  > p {
    margin: 0;
    color: #6e5b50;
    font-size: 1.04rem;
    line-height: 1.82;
    font-weight: 400;
    font-family: 'Inter', sans-serif;
    text-shadow: none;
  }
}

.opciones-section {
  background: linear-gradient(180deg, #f7f3ee 0%, #f4eee8 100%);
  padding: 4rem 1.2rem 5rem;
}

.opciones-inner {
  max-width: 1300px;
  margin: 0 auto;
  text-shadow: none;

  h3 {
    margin: 0 0 1.3rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 1.02rem;
    color: #6f5a4f;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
  }
}

.opciones-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
}

.opcion-card {
  border: 1px solid #dccfc4;
  background: linear-gradient(165deg, rgba(255, 253, 251, 1) 0%, rgba(250, 244, 238, 1) 100%);
  padding: 1.7rem;
  min-height: 210px;
  text-shadow: none;
  transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease, background 0.28s ease;
  position: relative;
  overflow: hidden;
  opacity: 0;
  animation: entradaSuave 0.75s ease-out both;

  &::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(120deg, rgba(161, 108, 77, 0.07) 0%, rgba(161, 108, 77, 0) 45%);
    opacity: 0.9;
    pointer-events: none;
  }

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 30px rgba(43, 27, 23, 0.11);
    border-color: #ceb9ab;
    background: linear-gradient(165deg, rgba(255, 253, 251, 1) 0%, rgba(246, 236, 226, 1) 100%);
  }

  .icono {
    font-size: 1.6rem;
    margin-bottom: 0.75rem;
    opacity: 0.72;
    position: relative;
    z-index: 1;
  }

  h4 {
    margin: 0;
    font-family: 'Playfair Display', serif;
    font-size: 1.78rem;
    line-height: 1.12;
    color: #2f221d;
    font-weight: 500;
    position: relative;
    z-index: 1;
  }

  p {
    margin: 0.85rem 0 0;
    color: #6f5f56;
    line-height: 1.62;
    font-size: 0.98rem;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    position: relative;
    z-index: 1;
  }
}

.opcion-card:nth-child(1) { animation-delay: 0.05s; }
.opcion-card:nth-child(2) { animation-delay: 0.12s; }
.opcion-card:nth-child(3) { animation-delay: 0.19s; }
.opcion-card:nth-child(4) { animation-delay: 0.26s; }
.opcion-card:nth-child(5) { animation-delay: 0.33s; }
.opcion-card:nth-child(6) { animation-delay: 0.40s; }

.seccion-metricas {
  background: transparent;
  padding: 5rem 1.6rem 6rem;
  display: grid;
  grid-template-columns: minmax(540px, 1.05fr) minmax(0, 1fr);
  gap: 3rem;
  align-items: center;
  position: relative;
  isolation: isolate;
  overflow: hidden;
}

.mosaico-metricas {
  position: relative;
  height: 560px;
  max-width: 560px;
}

.caja-metrica {
  position: absolute;
  padding: 1.35rem;
  border: 1px solid rgba(43, 27, 23, 0.7);
  background: rgba(248, 243, 106, 0.96);
  min-height: 130px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 10px 10px 0 rgba(43, 27, 23, 0.05);
  transition: transform 0.25s ease, box-shadow 0.25s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 14px 14px 26px rgba(43, 27, 23, 0.12);
    z-index: 7;
  }

  .numero {
    font-family: 'Inter', sans-serif;
    font-size: clamp(2.1rem, 3vw, 3rem);
    line-height: 1;
    color: #14110f;
    font-weight: 500;
    text-align: center;
  }

  .concepto {
    margin-top: 0.55rem;
    font-family: 'Inter', sans-serif;
    color: #171310;
    font-size: 0.86rem;
    line-height: 1.18;
    text-align: center;
    letter-spacing: -0.01em;
  }
}

.c-superficie { width: 330px; height: 200px; top: 10px; left: 20px; z-index: 2; }
.c-sedes { width: 230px; height: 185px; top: -18px; left: 380px; z-index: 3; }
.c-salas { width: 260px; height: 205px; top: 210px; left: 0; z-index: 2; }
.c-puestos { width: 300px; height: 240px; top: 165px; left: 300px; z-index: 4; }
.c-oficinas { width: 300px; height: 185px; top: 400px; left: 95px; z-index: 5; }

.contenido-metricas {
  max-width: 640px;
  align-self: center;

  h2 {
    margin: 0;
    font-family: 'Inter', sans-serif;
    font-size: clamp(3rem, 5.4vw, 5.1rem);
    line-height: 0.98;
    letter-spacing: -0.01em;
    color: #12100e;
    font-weight: 600;
  }

  p {
    margin: 2rem 0 0;
    font-family: 'Inter', sans-serif;
    color: #191612;
    line-height: 1.5;
    font-size: 1.02rem;
    max-width: 640px;
  }
}

@keyframes derivaLenta {
  0%,
  100% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
  50% {
    transform: translateY(8px) scale(1.04);
    opacity: 0.88;
  }
}

@keyframes entradaSuave {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* --- RESPONSIVE / ADAPTACIÓN DE INTERFAZ --- */
@media (max-width: 900px) {
  .hero-content h1 { font-size: 3.2rem; }
  .capsula-flotante { display: none; } /* Limpieza visual en tablets */
  .mapa-flotante-wrap { bottom: 8%; }

  .opciones-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .seccion-metricas {
    grid-template-columns: 1fr;
    padding: 4rem 1.1rem 5rem;
  }

  .mosaico-metricas {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
    height: auto;
    max-width: 100%;
  }

  .caja-metrica {
    position: relative;
    inset: auto;
    width: 100%;
    height: 130px;
    min-height: 130px;
    box-shadow: none;

    &:hover {
      transform: none;
      box-shadow: none;
    }
  }

  .contenido-metricas {
    max-width: 100%;

    h2 {
      font-size: clamp(2.4rem, 9vw, 3.4rem);
    }

    p {
      margin-top: 1.2rem;
    }
  }
}

@media (max-width: 768px) {
  .hero-stage::after {
    top: 36px; left: 36px; right: 36px; bottom: 36px;
    border-width: 3px;
    border-radius: 24px;
  }
  .destello-interfaz { display: none; }
  .hero-content h1 { font-size: 2.5rem; }
  .hero-content p { font-size: 1.05rem; }

  .opciones-grid {
    grid-template-columns: 1fr;
  }

  .opcion-card h4 {
    font-size: 1.55rem;
  }

  .mosaico-metricas {
    grid-template-columns: 1fr;
  }

  .caja-metrica {
    height: 115px;
    min-height: 115px;
  }
}
</style>