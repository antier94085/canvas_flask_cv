import StickerMakerView from '@/views/StickerMakerView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/stickermaker',
      name: 'stickerMaker',
      component: StickerMakerView
    },
    {
      path: '/',
      redirect: '/stickermaker'
    }
  ]
})

export default router
