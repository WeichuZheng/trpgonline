const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterView.vue')
  },
  {
    path: '/',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', name: 'dashboard', component: () => import('@/views/DashboardView.vue') },
      { path: 'modules/:id/edit', name: 'module-edit', component: () => import('@/views/ModuleEditView.vue') },
      { path: 'modules/:id/resources', name: 'module-resources', component: () => import('@/views/ModuleResourcesView.vue') },
      { path: 'rooms', name: 'room-list', component: () => import('@/views/RoomListView.vue') },
      { path: 'gm/rooms', name: 'gm-room-list', component: () => import('@/views/GmRoomListView.vue') },
      { path: 'rooms/:id/game', name: 'game-room', component: () => import('@/views/GameRoomView.vue') },
      { path: 'admin', name: 'admin', component: () => import('@/views/AdminView.vue') }
    ]
  }
]

export default routes
