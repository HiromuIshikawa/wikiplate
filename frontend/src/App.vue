<template>
  <div id="app">
    <nav-bar class="navbar" @create="create"/>
    <b-container class="main-container">
      <b-row class="main-row">
        <b-col class="sidebar-col" cols="12" sm="2"><side-bar/></b-col>
        <b-col v-if="sharedState.loading" class="loading-col" cols="12" sm = "10">
          <sync-loader class="loader" :loading="sharedState.loading" :color="color" :size="size" :margin="margin"></sync-loader>
        </b-col>
        <b-col v-else class="main-content-col" cols="12" sm="10"><router-view/></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import store from '@/store'
import SideBar from '@/components/SideBar'
import NavBar from '@/components/NavBar'
import SyncLoader from 'vue-spinner/src/SyncLoader'
import 'normalize.css'

export default {
  name: 'App',
  components: {
    SideBar,
    NavBar,
    SyncLoader
  },
  data () {
    return {
      sharedState: store.state,
      color: '#5bc0de',
      size: '20px',
      margin: '10px',
      radius: '2px'
    }
  },
  methods: {
    create (title, keywords) {
      store.actions.getTemplate(title, keywords)
    }
  }
}
</script>

<style>
  html {
    height: 100%;
  }
  body {
    background-color: whitesmoke;
    font-size: 18px;
    height: 100%;
  }
  #app {
    height: 100%;
    background-color: whitesmoke;
  }
  .main-container {
    background-color: white;
    height: 90%;
  }
  .main-row {
    height: 100%;
  }
  div.sidebar-col {
    padding: 0;
    height: 100%;
    background-color: gray;
    box-shadow: 2px 0px 3px gray;
  }
  div.main-content-col {
    padding-top: 5px;
    height: 100%;
  }
  div.loading-col {
    height: 100%;
    background-color: #eee;
  }
  .main-content-col h1 {
    color: #666;
    font-size: 25px;
    padding-bottom: 0.3em;
    border-bottom: solid 2px #999;
  }
  .loader {
    position: absolute;
    top: 50%;
    left: 50%;
    -webkit-transform: translateY(-50%) translateX(-50%);
    transform: translateY(-50%) translateX(-50%);
  }
</style>
