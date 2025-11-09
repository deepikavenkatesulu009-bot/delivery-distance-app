import adapter from '@sveltejs/adapter-static';
import preprocess from 'svelte-preprocess';

const dev = process.env.NODE_ENV === 'development';

export default {
  preprocess: preprocess(),
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: 'index.html' // SPA fallback for client-side routing
    }),
    // prerender all discovered routes (useful for simple SPA)
    prerender: {
      entries: ['*']
    }
  }
};
