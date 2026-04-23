import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: () => import('../views/LandingView.vue') // <-- Tu nueva portada estilo Torik
  },
  {
    path: '/salas',
    name: 'catalogo',
    component: () => import('../views/HomeView.vue') // <-- Tu antigua Home con el buscador y las tarjetas
  },
  {
    path: '/salas/:id',
    name: 'sala-detalle',
    component: () => import('../views/SalaDetalleView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/contacto',
    name: 'contacto',
    component: () => import('../views/ContactoView.vue')
  },
  {
    path: '/reservar-tour',
    name: 'reservar-tour',
    component: () => import('../views/ReservarTourView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/reservas',
    name: 'reservas',
    component: () => import('../views/HacerReservasView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mis-reservas',
    name: 'my-bookings',
    component: () => import('../views/UserReservasView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/favoritos',
    name: 'favoritos',
    component: () => import('../views/FavoritosView.vue')
  },
  {
    path: '/perfil',
    name: 'perfil',
    component: () => import('../views/PerfilView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/configuracion',
    name: 'configuracion',
    component: () => import('../views/ConfiguracionView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/reservas',
    name: 'admin-bookings',
    component: () => import('../views/AdminReservasView.vue'),
    meta: { requiresAuth: true, role: 'admin' } 
  },
  {
    path: '/admin/salas',
    name: 'admin-salas',
    component: () => import('../views/AdminSalasView.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/tours',
    name: 'admin-tours',
    component: () => import('../views/AdminToursView.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }

    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      };
    }

    return { top: 0 };
  }
})

export default router


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('user-token');
  const role = localStorage.getItem('user-role'); // Recuperamos el rol guardado en el login

  const rutaProtegida = to.matched.some(record => record.meta.requiresAuth);
  const soloAdmin = to.matched.some(record => record.meta.role === 'admin');
  const esRutaAdmin = to.path.startsWith('/admin');

  // Si es admin, lo mantenemos dentro del panel admin
  if (token && role === 'admin' && !esRutaAdmin) {
    next('/admin/reservas');
    return;
  }

  // 1. Si la ruta requiere autenticación y no hay token -> Login
  if (rutaProtegida && !token) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    });
  } 
  // 2. Si la ruta es solo para admin y el rol no es 'admin' -> Home
  else if (soloAdmin && role !== 'admin') {
    localStorage.setItem('ui-notice', JSON.stringify({
      tipo: 'warning',
      titulo: 'Acceso denegado',
      mensaje: 'No tienes permisos de administrador para entrar en esa sección.'
    }));
    next('/'); // Lo mandamos a la home
  } 
  // 3. En cualquier otro caso (ruta pública o tiene permisos) -> Adelante
  else {
    next();
  }
});


// // Este código se ejecuta antes de cada cambio de página
// router.beforeEach((to, from, next) => {
//   // Comprobamos si la ruta a la que va requiere estar logueado
//   const rutaProtegida = to.matched.some(record => record.meta.requiresAuth);
//   const estaLogueado = localStorage.getItem('user-token');

//   if (rutaProtegida && !estaLogueado) {
//     // Si es protegida y no hay token, al Login de cabeza
//     next('/login');
//   } else {
//     // Si todo está bien o la ruta es pública, adelante
//     next();
//   }
// });