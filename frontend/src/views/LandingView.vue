<template>
  <div class="landing-page">
    <nav class="landing-nav">
      <div class="logo">Torik<span>.</span></div>
      <div class="nav-links">
        <router-link to="/salas">Espacios</router-link>
        <router-link to="/login">Acceso Socios</router-link>
      </div>
      <router-link to="/salas" class="btn-nav-action">Explorar Ahora</router-link>
    </nav>

    <main class="landing-main">
      <section class="hero-content">
        <h1>Curated Modern Workspaces<br>for <em>Timeless Focus</em></h1>
        <p>Creemos en entornos que no siguen tendencias, sino que las trascienden. Espacios de coworking diseñados para el día de hoy, anclados para el éxito de toda una vida.</p>
        
        <router-link to="/salas" class="btn-cta">
          Explorar Catálogo
        </router-link>
      </section>

      <div class="image-wrapper">
        <img 
          src="https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200" 
          alt="Torik Premium Coworking Space" 
          class="main-hero-img"
        />
      </div>
    </main>
  </div>
</template>

<style scoped>
/* --- ESTILOS DE LA LANDING EXPERIENCIA PREMIUM --- */
.landing-page {
  background-color: #fcfaf7;
  min-height: 100vh;
  color: #2b1b17;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

/* Navbar */
.landing-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 4rem;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.logo {
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.logo span { color: #bfa38f; }

.nav-links {
  display: flex;
  gap: 2.5rem;
}

.nav-links a {
  text-decoration: none;
  color: #6e5e58;
  font-size: 0.95rem;
  font-weight: 400;
  transition: color 0.3s;
}

.nav-links a:hover { color: #2b1b17; }

.btn-nav-action {
  text-decoration: none;
  color: #2b1b17;
  border: 1px solid #2b1b17;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.btn-nav-action:hover {
  background: #2b1b17;
  color: #fcfaf7;
}

/* Hero Section */
.landing-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
  text-align: center;
  flex-grow: 1;
}

.hero-content h1 {
  font-family: 'Playfair Display', serif;
  font-size: 3.8rem;
  font-weight: 400;
  line-height: 1.15;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
}

.hero-content h1 em {
  font-family: 'Playfair Display', serif;
  font-style: italic;
}

.hero-content p {
  font-family: 'Inter', sans-serif;
  font-size: 1.1rem;
  color: #6e5e58;
  max-width: 700px;
  margin: 0 auto 2.5rem auto;
  line-height: 1.6;
}

/* Botón Ovalado Idéntico a la Imagen */
.btn-cta {
  display: inline-block;
  text-decoration: none;
  background: #362521;
  color: #fcfaf7;
  padding: 1rem 2.5rem;
  border-radius: 30px;
  font-weight: 500;
  font-size: 1rem;
  letter-spacing: 0.02em;
  box-shadow: 0 4px 15px rgba(54, 37, 33, 0.15);
  transition: transform 0.3s, background-color 0.3s;
}

.btn-cta:hover {
  background: #4a3530;
  transform: translateY(-2px);
}

/* Envoltorio de la Imagen de Arquitectura */
.image-wrapper {
  margin-top: 4rem;
  width: 100%;
  border-radius: 0px; /* Recto e imponente estilo editorial */
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(43, 27, 23, 0.05);
}

.main-hero-img {
  width: 100%;
  height: 550px;
  object-fit: cover;
  display: block;
}
</style>