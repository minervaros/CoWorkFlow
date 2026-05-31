<template>
  <div class="about">
    <h1>This is an about page</h1>
      <div class="home-velo"></div>
  </div>
</template>
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
  position: relative;
  z-index: 2;
}

.about > *:not(.home-velo) {
  position: relative;
  z-index: 2;
}
