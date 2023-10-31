<script>
  // npm install svelte-spa-router
  import Router from  'svelte-spa-router'
  import Head from './components/Head.svelte'
  import Home from './routes/Home.svelte'

  const routes = {
    '/' : Home,
  }
</script>

<Head />
<Router {routes} />




